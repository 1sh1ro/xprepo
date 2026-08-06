# Tokenized-stock project adapter

Use this adapter only after verifying the paths still exist.

## Research root

    /Users/my/xp/tokenized-stock-factor-research

## Existing control surfaces

| Purpose | Path or command |
| --- | --- |
| Unified point-in-time research runner | `run_worldquant_backtest.py` |
| Factor construction | `factor_backtest/factors.py` |
| Portfolio and walk-forward engine | `factor_backtest/engine.py` |
| Data joins and audits | `factor_backtest/data.py` |
| Rejected registry | `config/rejected_factor_registry.json` |
| Registry CLI | `rejected_factor_registry.py` |
| Frozen forward watch | `config/prospective_factor_watchlist_20260713.json` |

Inspect current code and config before assuming these interfaces remain unchanged.

## Required pre-search check

Run from the research root:

    python3 rejected_factor_registry.py check FACTOR_ID --scope DATA_SCOPE
    python3 rejected_factor_registry.py filter FACTOR_A FACTOR_B --scope DATA_SCOPE

Do not probe `collect_*` scripts with `--help`; some collectors execute work when invoked. Inspect their source to learn arguments.

## Local defaults to preserve

- Use contract-verified token/underlying identity, not symbol-only matching.
- Require point-in-time joins and zero future underlying joins.
- Use at least one-bar signal delay.
- Evaluate configured baseline and stress one-way costs.
- Prefer non-overlapping observations for short-horizon event rules.
- Apply BH-FDR to every candidate actually tried.
- Treat signal correlation at or above the configured limit as duplicate unless incremental value is proven.
- Run a long-only diagnostic when shorts are unavailable.
- Keep historical discoveries `exploratory` until independent-venue or post-freeze evidence exists.

## Safe integration pattern

1. Create a new campaign configuration; never overwrite a frozen one.
2. Add only preregistered factors and focused tests.
3. Run targeted tests, then relevant full tests.
4. Run the frozen campaign once and save raw metrics, correlations, config, commit/hash provenance, and report.
5. Register failures; place survivors only in a new forward-only watch configuration.
6. Do not deploy a site unless explicitly requested.
