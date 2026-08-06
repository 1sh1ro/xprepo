#!/usr/bin/env python3
"""Validate a return-blind autonomous-factor mechanism seed library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ID = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
FORBIDDEN_SEED_KEYS = {
    "formula", "expression", "window", "lookback", "threshold", "weight",
    "return", "returns", "backtest_result", "ic", "sharpe", "performance_rank",
}
SOURCE_FIELDS = {"id", "name", "url", "license", "reuse_boundary"}
SEED_FIELDS = {
    "id", "family", "source_id", "source_terms", "mechanism", "prediction",
    "required_observables", "point_in_time_constraints", "token_transfer",
    "nearest_rejected_families", "novelty_requirement", "data_status",
    "forbidden_mutations",
}


class ValidationError(ValueError):
    pass


def required(mapping: dict[str, Any], fields: set[str], where: str) -> None:
    missing = sorted(field for field in fields if field not in mapping or mapping[field] in ("", [], None))
    if missing:
        raise ValidationError(f"{where} missing {missing}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.library.read_text())
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ValidationError("schema_version must equal 1")
        if payload.get("returns_visible") is not False:
            raise ValidationError("returns_visible must be false")
        if not ID.fullmatch(str(payload.get("library_id", ""))):
            raise ValidationError("library_id is invalid")
        sources = payload.get("sources")
        seeds = payload.get("seeds")
        if not isinstance(sources, list) or not sources or not isinstance(seeds, list) or not seeds:
            raise ValidationError("sources and seeds must be non-empty lists")
        source_ids: set[str] = set()
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                raise ValidationError(f"sources[{index}] must be an object")
            required(source, SOURCE_FIELDS, f"sources[{index}]")
            if not ID.fullmatch(str(source["id"])) or source["id"] in source_ids:
                raise ValidationError("source IDs must be unique and valid")
            if not str(source["url"]).startswith(("https://", "http://")):
                raise ValidationError(f"sources[{index}].url must be http(s)")
            source_ids.add(source["id"])
        seed_ids: set[str] = set()
        for index, seed in enumerate(seeds):
            if not isinstance(seed, dict):
                raise ValidationError(f"seeds[{index}] must be an object")
            required(seed, SEED_FIELDS, f"seeds[{index}]")
            bad = sorted(FORBIDDEN_SEED_KEYS.intersection(seed))
            if bad:
                raise ValidationError(f"seeds[{index}] includes forbidden keys {bad}")
            if not ID.fullmatch(str(seed["id"])) or seed["id"] in seed_ids:
                raise ValidationError("seed IDs must be unique and valid")
            if seed["source_id"] not in source_ids:
                raise ValidationError(f"seeds[{index}] has unknown source_id")
            if not isinstance(seed["forbidden_mutations"], list) or not seed["forbidden_mutations"]:
                raise ValidationError(f"seeds[{index}].forbidden_mutations must be non-empty")
            seed_ids.add(seed["id"])
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1) from exc
    print(json.dumps({"status": "valid", "library_id": payload["library_id"],
                      "source_count": len(sources), "seed_count": len(seeds)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
