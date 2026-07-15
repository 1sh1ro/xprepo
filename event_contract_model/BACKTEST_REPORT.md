# BTC 10 Minute Event Contract Backtest

Run date: 2026-06-11 Asia/Shanghai.

This report summarizes the baseline model implemented in `btc_10m_event_model.py`. It predicts whether OKX `BTC-USDT-SWAP` will be higher 10 minutes after each 1 minute candle close.

## Model

- Data source: OKX public `market/history-candles`.
- Bar size: 1 minute.
- Horizon: 10 minutes.
- Label: `future_close[t+10m] > close[t]`.
- Features: recent log returns, realized volatility ratios, EMA gaps, rolling z-scores, range position, drawdown/rebound, RSI, candle shape, volume ratios/z-scores, and intraday time cycles.
- Main model: calibrated logistic regression with median imputation, standard scaling, balanced class weights, and sigmoid probability calibration.
- Experimental models tested: ExtraTrees and HistGradientBoosting.
- Split: chronological fit / validation / holdout. No random shuffle.
- Threshold: selected on the validation slice, then evaluated once on the holdout slice.

## Backtest Results

| Window | Train rows | Test rows | Test period UTC | Up rate | Accuracy | AUC | Brier | Confidence >= 0.55 accuracy | Coverage |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 7d | 7,049 | 3,022 | 2026-06-08 13:39 to 2026-06-10 16:00 | 48.38% | 50.23% | 0.503 | 0.2500 | 60.81% | 2.45% |
| 14d | 14,105 | 6,046 | 2026-06-06 11:17 to 2026-06-10 16:02 | 49.77% | 50.20% | 0.499 | 0.2521 | 48.62% | 30.04% |
| 30d | 30,233 | 12,958 | 2026-06-01 16:06 to 2026-06-10 16:03 | 46.91% | 53.02% | 0.524 | 0.2495 | 53.85% | 17.16% |

## Optimized 30 Day Result

The optimized run uses the same 30 day OKX data, richer features, logistic regression, and validation-tuned threshold.

| Run | Model | Threshold | Test rows | Accuracy | AUC | Brier | Selected accuracy | Selected coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Original baseline | Logistic | 0.55 fixed | 12,958 | 53.02% | 0.524 | 0.2495 | 53.85% | 17.16% |
| Optimized main | Logistic | 0.51 validation-tuned | 12,958 | 53.92% | 0.533 | 0.2486 | 55.01% | 69.25% |
| Optimized at 0.55 slice | Logistic | 0.55 slice | 1,000 | N/A | N/A | N/A | 56.10% | 7.72% |
| ExtraTrees experiment | ExtraTrees | 0.52 validation-tuned | 12,958 | 51.91% | 0.519 | 0.2543 | 51.87% | 76.36% |
| HGB experiment | HGB | 0.50 validation-tuned | 12,958 | 50.08% | 0.502 | 0.2798 | 50.08% | 100.00% |

The optimized main artifact is:

- Raw data: `event_contract_model/runs/okx_30d_logistic_opt/data/btc_usd_1m.csv`
- Features: `event_contract_model/runs/okx_30d_logistic_opt/features/features.csv`
- Predictions: `event_contract_model/runs/okx_30d_logistic_opt/backtest/predictions.csv`
- Metrics: `event_contract_model/runs/okx_30d_logistic_opt/backtest/metrics.json`
- Model: `event_contract_model/runs/okx_30d_logistic_opt/model/model.joblib`
- Summary: `event_contract_model/runs/okx_30d_logistic_opt/summary.md`

The original 30 day baseline artifact is retained for comparison:

- Raw data: `event_contract_model/runs/okx_30d/data/btc_usd_1m.csv`
- Features: `event_contract_model/runs/okx_30d/features/features.csv`
- Predictions: `event_contract_model/runs/okx_30d/backtest/predictions.csv`
- Metrics: `event_contract_model/runs/okx_30d/backtest/metrics.json`
- Model: `event_contract_model/runs/okx_30d/model/model.joblib`
- Summary: `event_contract_model/runs/okx_30d/summary.md`

## Interpretation

The baseline is functional but not yet strong enough to treat as a production trading edge.

The optimized 30 day holdout improves the original baseline to 53.92% accuracy and 0.533 AUC. The validation-tuned threshold selects 69.25% of opportunities with 55.01% accuracy. The fixed 0.55 slice is more selective at 7.72% coverage and 56.10% accuracy.

That is directionally interesting, but still thin for event contracts once fees, spread, latency, settlement mechanics, and adverse selection are included.

The 7 day and 14 day windows are unstable. The 7 day high-confidence slice looks good but has only 74 rows; the 14 day high-confidence slice underperforms. This instability is the main warning sign.

The `auto` model selector chose HGB on validation, but HGB failed on the next holdout period. For that reason the script now defaults to `--model logistic`; `--model auto` remains available for research only.

## Latest Prediction Smoke Test

Command:

```bash
python3 event_contract_model/btc_10m_event_model.py predict \
  --model-dir event_contract_model/runs/okx_30d_logistic_opt \
  --recent-minutes 240
```

Observed output:

```json
{
  "timestamp_utc": "2026-06-10T16:24:00+00:00",
  "product": "BTC-USDT-SWAP",
  "source": "okx",
  "last_close": 62199.6,
  "horizon_minutes": 10,
  "p_up": 0.49930897554478654,
  "direction": "DOWN",
  "confidence": 0.5006910244552134
}
```

This is below the validation-tuned 0.51 confidence threshold, so the optimized model would abstain.

## Next Improvements

1. Add rolling walk-forward retraining windows instead of one holdout split.
2. Add exchange microstructure features: bid/ask spread, order book imbalance, taker buy/sell volume, and liquidation bursts.
3. Add derivatives features from the existing report code: funding, basis, OI, and DVOL.
4. Tune the abstention threshold against event-contract payout odds, not just accuracy.
5. Add fee/spread/settlement backtest assumptions before any live usage.
