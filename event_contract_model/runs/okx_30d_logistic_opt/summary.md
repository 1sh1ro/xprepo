# BTC 10m Event Model Run

- Product: `BTC-USDT-SWAP`
- Horizon: `10 minutes`
- Model: `logistic`
- Train rows: `30233` from `2026-05-11T16:13:00+00:00` to `2026-06-01T16:05:00+00:00`
- Fit rows: `22674`
- Validation rows: `7559`
- Test rows: `12958` from `2026-06-01T16:06:00+00:00` to `2026-06-10T16:03:00+00:00`
- Test up rate: `0.4691`
- Accuracy all: `0.5392`
- AUC: `0.5332`
- Brier score: `0.2486`
- Average confidence: `0.5217`
- Selected threshold: `0.51`
- Selected rows: `8973` (`69.25%` coverage)
- Selected accuracy: `0.5501`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 12958 | 100.00% | 0.5392 | 0.5217 |
| 0.52 | 5670 | 43.76% | 0.5556 | 0.5376 |
| 0.55 | 1000 | 7.72% | 0.5610 | 0.5672 |
| 0.58 | 177 | 1.37% | 0.6215 | 0.5972 |
| 0.60 | 59 | 0.46% | 0.7458 | 0.6164 |
| 0.65 | 2 | 0.02% | 1.0000 | 0.6563 |
| 0.70 | 0 | 0.00% | N/A | N/A |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.30-0.40 | 37 | 0.3844 | 0.2973 |
| 0.40-0.50 | 9338 | 0.4767 | 0.4521 |
| 0.50-0.60 | 3561 | 0.5161 | 0.5131 |
| 0.60-0.70 | 22 | 0.6177 | 0.8182 |
