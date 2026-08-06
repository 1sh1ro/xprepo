# Autonomous factor research contract

## Separation rules

Use this state sequence:

    mechanism_draft -> registry_screened -> preregistered -> development_checked
    -> validation_selected -> final_test_exposed
    -> rejected | redundant | data_invalid | exploratory | paper_candidate
    -> prospective_watch

Never move backward from `final_test_exposed` to change a frozen field. A revised formula, direction, window, threshold, cost, universe, entry rule, or holding period requires a new campaign ID and multiplicity entry.

## Mechanism brief

A valid brief identifies a market failure; gives at least two causal links; states asset subset, signal time, direction, and horizon; names alternative explanations; maps each field to its availability time; and states a falsifier.

Mechanism sources are clues, not evidence. Record source URL, publication/access dates, original market, and exact transfer argument. Prefer primary papers, official exchange or issuer documents, and first-party field definitions.

## Variant budget

Allow 1–5 variants. Each must be a robustness implementation of the same prediction: an adjacent economically meaningful horizon, a specified residualization, volatility scaling, or one pre-existing execution-quality confirmation are permissible.

Exhaustive windows, sign flips, threshold sweeps, test-Sharpe transformations, and renaming a rejected rule are not permissible.

## Data contract

Distinguish `event_time`, `published_at`, `available_at`, `signal_time`, `entry_time`, and `exit_time`. Require:

    available_at <= signal_time < entry_time

Document revisions, corporate actions, delayed bars, and identity mapping. Treat identity mismatch, stale joins, partial event bars, survivorship leakage, and same-bar execution as `data_invalid`.

## Minimum evaluation surface

Choose statistics suitable to the strategy, but do not omit execution and concentration:

- cross-sectional: Rank IC, quantile spread/monotonicity, turnover, correlation;
- event: non-overlapping event portfolios, median, hit rate, same-time null;
- time-series: regime coverage, serial dependence, overlap, capacity;
- all: chronological splits, purge/embargo where appropriate, baseline/stress cost, asset/period concentration, and multiple-testing correction.

No backtest-only status implies a live or profitable strategy.
