# BTC 10m Event Model Run

- Product: `btcusd`
- Horizon: `10 minutes`
- Model: `logistic`
- Train rows: `129593` from `2026-02-10T17:01:00+00:00` to `2026-05-11T16:53:00+00:00`
- Fit rows: `103674`
- Validation rows: `25919`
- Test rows: `43198` from `2026-05-11T16:54:00+00:00` to `2026-06-10T16:51:00+00:00`
- Test up rate: `0.4839`
- Accuracy all: `0.5141`
- AUC: `0.5235`
- Brier score: `0.2498`
- Average confidence: `0.5242`
- Selected threshold: `0.50`
- Selected rows: `43198` (`100.00%` coverage)
- Selected accuracy: `0.5141`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 43198 | 100.00% | 0.5141 | 0.5242 |
| 0.52 | 22316 | 51.66% | 0.5240 | 0.5376 |
| 0.55 | 3638 | 8.42% | 0.5330 | 0.5659 |
| 0.58 | 558 | 1.29% | 0.5824 | 0.5984 |
| 0.60 | 170 | 0.39% | 0.6529 | 0.6228 |
| 0.65 | 17 | 0.04% | 0.4706 | 0.6725 |
| 0.70 | 1 | 0.00% | 1.0000 | 0.7135 |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.20-0.30 | 1 | 0.2865 | 0.0000 |
| 0.30-0.40 | 29 | 0.3545 | 0.5517 |
| 0.40-0.50 | 19207 | 0.4786 | 0.4660 |
| 0.50-0.60 | 23821 | 0.5257 | 0.4970 |
| 0.60-0.70 | 140 | 0.6174 | 0.6929 |
