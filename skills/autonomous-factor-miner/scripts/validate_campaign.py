#!/usr/bin/env python3
"""Validate and freeze an autonomous factor campaign manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ID = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
BLOCKED = {"blocked_prior_failure", "blocked_data"}


class ValidationError(ValueError):
    pass


def require(obj: dict[str, Any], key: str, where: str) -> Any:
    value = obj.get(key)
    if value is None or value == "" or value == []:
        raise ValidationError(f"missing {where}.{key}")
    return value


def payload_for_hash(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "lock"}


def digest(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload_for_hash(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def has_placeholder(value: Any) -> bool:
    if isinstance(value, dict):
        return any(has_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(has_placeholder(item) for item in value)
    return isinstance(value, str) and ("replace-with" in value.lower() or "replace_with" in value.lower())


def validate(payload: dict[str, Any], frozen: bool) -> None:
    if payload.get("schema_version") != 1:
        raise ValidationError("schema_version must equal 1")
    for key in ("campaign", "seed_lineage", "mechanism", "registry_screen", "data_contract",
                "candidate_variants", "evaluation", "falsification", "governance",
                "forward_tracking", "lock"):
        require(payload, key, "root")

    campaign = payload["campaign"]
    if not isinstance(campaign, dict) or not ID.fullmatch(str(require(campaign, "id", "campaign"))):
        raise ValidationError("campaign.id must use lowercase letters, digits, dot, underscore, or hyphen")
    if campaign.get("timezone") != "Asia/Shanghai":
        raise ValidationError("campaign.timezone must equal Asia/Shanghai")
    if campaign.get("mode") not in {"ideas", "campaign", "evaluate", "forward"}:
        raise ValidationError("campaign.mode is invalid")

    lineage = payload["seed_lineage"]
    if not isinstance(lineage, dict) or lineage.get("returns_visible") is not False:
        raise ValidationError("seed_lineage.returns_visible must be false")
    for key in ("source_id", "seed_id", "selection_reason"):
        require(lineage, key, "seed_lineage")

    mechanism = payload["mechanism"]
    for key in ("family", "market_failure", "causal_chain", "falsifiable_prediction",
                "expected_direction", "alternative_explanations"):
        require(mechanism, key, "mechanism")
    if mechanism["expected_direction"] not in {"positive", "negative"}:
        raise ValidationError("mechanism.expected_direction must be positive or negative")

    registry = payload["registry_screen"]
    if registry.get("decision") not in {"new_mechanism", "allowed_retest", *BLOCKED}:
        raise ValidationError("registry_screen.decision is invalid")
    if registry.get("decision") == "allowed_retest":
        require(registry, "allowed_retest_condition", "registry_screen")

    contract = payload["data_contract"]
    for key in ("universe", "identity_rule", "bar_interval", "sources", "signal_time_rule",
                "entry_rule", "exit_rule", "minimum_assets"):
        require(contract, key, "data_contract")
    for source in contract["sources"]:
        for key in ("name", "fields", "event_time_field", "availability_time_field", "point_in_time_rule"):
            require(source, key, "data_contract.sources[]")

    variants = payload["candidate_variants"]
    max_variants = payload["governance"].get("max_variants")
    if not isinstance(max_variants, int) or not 1 <= len(variants) <= max_variants <= 5:
        raise ValidationError("candidate variants must be 1–5 and within max_variants")
    factor_ids: set[str] = set()
    for variant in variants:
        factor_id = str(require(variant, "id", "candidate_variants[]"))
        if not ID.fullmatch(factor_id) or factor_id in factor_ids:
            raise ValidationError("candidate factor IDs must be unique and valid")
        factor_ids.add(factor_id)
        for key in ("expression", "direction", "robustness_reason", "rebalance_rule",
                    "signal_delay_bars", "holding_period"):
            require(variant, key, "candidate_variants[]")
        if variant["direction"] not in {"positive", "negative"} or variant["signal_delay_bars"] < 1:
            raise ValidationError("candidate direction or delay is invalid")

    evaluation = payload["evaluation"]
    if evaluation.get("split_method") not in {"chronological", "chronological_walk_forward"}:
        raise ValidationError("evaluation.split_method is invalid")
    for period in ("train", "validation", "test"):
        bounds = require(evaluation, period, "evaluation")
        for key in ("start", "end"):
            datetime.fromisoformat(require(bounds, key, f"evaluation.{period}"))
    if not (evaluation["train"]["end"] < evaluation["validation"]["start"] < evaluation["test"]["start"]):
        raise ValidationError("evaluation periods must be chronological")
    if evaluation["stress_one_way_cost_bps"] < evaluation["baseline_one_way_cost_bps"]:
        raise ValidationError("stress cost must be at least baseline cost")

    governance = payload["governance"]
    if governance.get("test_feedback_policy") != "no_revision_same_campaign":
        raise ValidationError("test feedback policy must prohibit same-campaign revision")
    if governance.get("live_trading_allowed") is not False or governance.get("publish_allowed") is not False:
        raise ValidationError("live trading and publishing must both be false")
    for key in ("reject_if", "retest_only_if"):
        require(payload["falsification"], key, "falsification")
    if payload["forward_tracking"].get("historical_rows_excluded") is not True:
        raise ValidationError("forward tracking must exclude historical rows")

    lock = payload["lock"]
    if frozen:
        if campaign.get("stage") != "preregistered" or lock.get("status") != "frozen":
            raise ValidationError("frozen campaign needs preregistered stage and frozen lock")
        datetime.fromisoformat(str(require(lock, "frozen_at", "lock")))
        if lock.get("proposal_sha256") != digest(payload):
            raise ValidationError("frozen proposal hash does not match")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--write-lock", action="store_true")
    parser.add_argument("--require-frozen", action="store_true")
    args = parser.parse_args()
    if args.write_lock and args.require_frozen:
        parser.error("choose only one lock mode")
    try:
        payload = json.loads(args.manifest.read_text())
        validate(payload, frozen=False)
        if args.write_lock:
            if has_placeholder(payload_for_hash(payload)):
                raise ValidationError("replace template placeholders before freezing")
            if payload["registry_screen"]["decision"] in BLOCKED:
                raise ValidationError("blocked registry decision cannot be frozen")
            payload["campaign"]["stage"] = "preregistered"
            payload["lock"] = {
                "status": "frozen",
                "frozen_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
                "proposal_sha256": digest(payload),
            }
            args.manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            validate(payload, frozen=True)
        elif args.require_frozen:
            validate(payload, frozen=True)
    except (OSError, ValueError, ValidationError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1) from exc
    print(json.dumps({"status": "valid", "campaign_id": payload["campaign"]["id"],
                      "proposal_sha256": digest(payload)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
