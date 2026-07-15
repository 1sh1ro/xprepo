# BTC 10m Event Model Run

- Product: `btcusd`
- Horizon: `10 minutes`
- Model: `logistic_raw`
- Train rows: `129593` from `2026-02-10T17:01:00+00:00` to `2026-05-11T16:53:00+00:00`
- Fit rows: `103674`
- Validation rows: `25919`
- Test rows: `43198` from `2026-05-11T16:54:00+00:00` to `2026-06-10T16:51:00+00:00`
- Test up rate: `0.4839`
- Accuracy all: `0.5148`
- AUC: `0.5230`
- Brier score: `0.2502`
- Average confidence: `0.5326`
- Selected threshold: `0.55`
- Selected rows: `9025` (`20.89%` coverage)
- Selected accuracy: `0.5323`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 43198 | 100.00% | 0.5148 | 0.5326 |
| 0.52 | 27469 | 63.59% | 0.5199 | 0.5456 |
| 0.55 | 9025 | 20.89% | 0.5323 | 0.5702 |
| 0.58 | 1951 | 4.52% | 0.5356 | 0.6022 |
| 0.60 | 757 | 1.75% | 0.5627 | 0.6242 |
| 0.65 | 94 | 0.22% | 0.7128 | 0.6827 |
| 0.70 | 21 | 0.05% | 0.4762 | 0.7247 |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.20-0.30 | 15 | 0.2715 | 0.6667 |
| 0.30-0.40 | 56 | 0.3754 | 0.5000 |
| 0.40-0.50 | 19148 | 0.4714 | 0.4650 |
| 0.50-0.60 | 23293 | 0.5330 | 0.4966 |
| 0.60-0.70 | 680 | 0.6210 | 0.5706 |
| 0.70-0.80 | 6 | 0.7151 | 0.8333 |
