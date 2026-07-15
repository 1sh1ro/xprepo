# BTC 10 Minute Event Contract Model

Baseline pipeline for predicting whether BTC will be higher or lower 10 minutes from now.

The implementation supports public OKX, Bitstamp, Binance, and Coinbase 1 minute candles. For the 120 day backtest, Bitstamp BTC/USD was used because OKX and Coinbase TLS connections were unstable from this environment and Binance futures historical windows returned a regional 451 response. The model is intentionally simple and auditable: it builds lagged price/volume features, trains a logistic-style classifier, tunes or fixes a confidence threshold, and runs a chronological holdout backtest.

## Quick Start

Fetch 1 minute candles, train, and backtest:

```bash
python3 event_contract_model/btc_10m_event_model.py run \
  --source bitstamp \
  --model logistic \
  --threshold-mode fixed \
  --probability-threshold 0.58 \
  --days 120 \
  --outdir event_contract_model/runs/btc_10m_120d
```

Use an existing CSV instead of fetching:

```bash
python3 event_contract_model/btc_10m_event_model.py run \
  --input-csv event_contract_model/runs/btc_10m_30d/data/btc_usd_1m.csv \
  --outdir event_contract_model/runs/replay
```

Generate a latest prediction from saved artifacts:

```bash
python3 event_contract_model/btc_10m_event_model.py predict \
  --model-dir event_contract_model/runs/btc_10m_30d \
  --source bitstamp \
  --recent-minutes 240
```

## Outputs

- `data/btc_usd_1m.csv`: raw minute candles.
- `features/features.csv`: engineered features and labels.
- `backtest/predictions.csv`: chronological holdout predictions.
- `backtest/metrics.json`: accuracy, AUC, Brier score, calibration buckets, and threshold slices.
- `model/model.joblib`: trained calibrated model bundle.
- `summary.md`: human-readable run summary.

## Model Options

- `--model logistic`: calibrated logistic model; best conservative high-confidence 120 day result.
- `--model logistic_raw`: uncalibrated, strongly regularized logistic model; useful when higher signal coverage is preferred.
- `--model extra_trees`: experimental tree ensemble.
- `--model hgb`: experimental histogram gradient boosting.
- `--model auto`: selects on the validation slice, useful for research but not the current default because validation winners can overfit the next holdout window.
- `--threshold-mode auto`: chooses a confidence threshold on the validation slice.
- `--threshold-mode fixed`: uses `--probability-threshold` directly.

## Current 120 Day Recommendation

- Conservative mode: `runs/bitstamp_120d_logistic_thr058`, `logistic`, threshold `0.58`. Holdout selected accuracy `58.24%` at `1.29%` coverage.
- Higher-frequency mode: `runs/bitstamp_120d_logistic_raw_thr055`, `logistic_raw`, threshold `0.55`. Holdout selected accuracy `53.23%` at `20.89%` coverage.

For an event-contract bot, start with conservative mode and abstain when confidence is below the artifact threshold.

## Label

`target_up = 1` when:

```text
close[t + 10 minutes] > close[t]
```

The confidence is the calibrated predicted probability for the chosen direction:

```text
UP confidence = P(target_up = 1)
DOWN confidence = 1 - P(target_up = 1)
```

This is a research baseline, not trading advice. Event contracts need separate handling for fees, spread, oracle settlement, latency, and position sizing.
