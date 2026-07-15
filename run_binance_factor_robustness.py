#!/usr/bin/env python3
"""Run overlapping-window and permutation checks on the Binance RWA sample."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import math
import random
import statistics
from datetime import datetime, timezone

from audit_binance_data_and_factor import fetch_asset, universe


def max_drawdown(returns):
    equity = peak = 1.0
    drawdown = 0.0
    for value in returns:
        equity *= 1 + value
        peak = max(peak, equity)
        drawdown = min(drawdown, equity / peak - 1)
    return drawdown


def summary(values):
    if not values:
        return {"n": 0}
    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else None
    return {
        "n": len(values),
        "mean_pct": mean * 100,
        "median_pct": statistics.median(values) * 100,
        "hit_rate_pct": sum(v > 0 for v in values) / len(values) * 100,
        "stdev_pct": stdev * 100 if stdev is not None else None,
        "t_stat_vs_zero": mean / (stdev / math.sqrt(len(values))) if stdev else None,
        "max_drawdown_pct": max_drawdown(values) * 100,
    }


def test(candles, holding, cost_bps, seed=7, permutations=4000):
    maps = [({c["openTime"]: c for c in item["candles"]}, item["asset"]["symbol"]) for item in candles]
    common = sorted(set.intersection(*(set(price_map) for price_map, _ in maps)))
    lookback = 12
    selected, median_base, random_base, active_spread = [], [], [], []
    choices = []
    for index in range(lookback, len(common) - holding):
        entry_time = common[index]
        exit_time = common[index + holding]
        candidates = []
        for price_map, symbol in maps:
            past = price_map[common[index - lookback]]["close"]
            entry = price_map[entry_time]["close"]
            exit_price = price_map[exit_time]["close"]
            candidates.append((entry / past - 1, exit_price / entry - 1, symbol))
        candidates.sort(key=lambda value: value[0])
        selected_return = candidates[0][1] - cost_bps / 10000
        all_returns = [value[1] - cost_bps / 10000 for value in candidates]
        median_return = statistics.median(all_returns)
        selected.append(selected_return)
        median_base.append(median_return)
        random_base.append(all_returns[0])
        active_spread.append(selected_return - median_return)
        choices.append(all_returns)

    split = max(1, int(len(selected) * 0.7))
    rng = random.Random(seed)
    perm_means = []
    for _ in range(permutations):
        perm_means.append(statistics.mean(rng.choice(row) for row in choices))
    observed = statistics.mean(selected)
    p_value = (1 + sum(value >= observed for value in perm_means)) / (permutations + 1)
    observed_spread = statistics.mean(active_spread)
    perm_spreads = []
    for _ in range(permutations):
        perm_spreads.append(statistics.mean(rng.choice(row) - statistics.median(row) for row in choices))
    spread_p = (1 + sum(value >= observed_spread for value in perm_spreads)) / (permutations + 1)

    return {
        "holding_hours": holding,
        "cost_bps": cost_bps,
        "common_1h_timestamps": len(common),
        "overlapping": {
            "selected_lowest_12h": summary(selected),
            "cross_sectional_median": summary(median_base),
            "first_asset_control": summary(random_base),
            "selected_minus_median": summary(active_spread),
            "permutation_p_selected_mean_ge_observed": p_value,
            "permutation_p_active_spread_ge_observed": spread_p,
        },
        "walk_forward": {
            "train": summary(selected[:split]),
            "validation": summary(selected[split:]),
            "validation_selected_minus_median": summary(active_spread[split:]),
        },
    }


def main():
    assets, universe_errors = universe()
    selected_assets = assets[:15]
    fetched, errors = [], []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_asset, asset): asset for asset in selected_assets}
        for future in as_completed(futures):
            asset = futures[future]
            try:
                fetched.append(future.result())
            except Exception as exc:
                errors.append({"symbol": asset.get("symbol"), "error": str(exc)})
    fetched.sort(key=lambda item: item["asset"]["symbol"])
    usable = [item for item in fetched if len(item["candles"]) >= 60]
    tests = [test(usable, holding, cost) for holding in (24, 36, 48) for cost in (0, 30, 60)]
    print(json.dumps({
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "sample": {
            "universe_assets": len(assets),
            "audited_assets": len(usable),
            "symbols": [item["asset"]["symbol"] for item in usable],
            "universe_errors": universe_errors,
            "fetch_errors": errors,
        },
        "tests": tests,
        "caveat": "Overlapping windows are not independent observations; p-values are a screening diagnostic, not proof of tradable alpha.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
