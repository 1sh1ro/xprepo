# BTC 10m Event Model Run

- Product: `BTC-USDT-SWAP`
- Horizon: `10 minutes`
- Model: `extra_trees`
- Train rows: `30233` from `2026-05-11T16:13:00+00:00` to `2026-06-01T16:05:00+00:00`
- Fit rows: `22674`
- Validation rows: `7559`
- Test rows: `12958` from `2026-06-01T16:06:00+00:00` to `2026-06-10T16:03:00+00:00`
- Test up rate: `0.4691`
- Accuracy all: `0.5191`
- AUC: `0.5193`
- Brier score: `0.2543`
- Average confidence: `0.5645`
- Selected threshold: `0.52`
- Selected rows: `9895` (`76.36%` coverage)
- Selected accuracy: `0.5187`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 12958 | 100.00% | 0.5191 | 0.5645 |
| 0.52 | 9895 | 76.36% | 0.5187 | 0.5815 |
| 0.55 | 6204 | 47.88% | 0.5230 | 0.6097 |
| 0.58 | 4047 | 31.23% | 0.5357 | 0.6344 |
| 0.60 | 3113 | 24.02% | 0.5271 | 0.6478 |
| 0.65 | 1374 | 10.60% | 0.5124 | 0.6784 |
| 0.70 | 242 | 1.87% | 0.4711 | 0.7178 |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.20-0.30 | 1 | 0.2992 | 0.0000 |
| 0.30-0.40 | 1465 | 0.3598 | 0.4485 |
| 0.40-0.50 | 5822 | 0.4614 | 0.4574 |
| 0.50-0.60 | 4023 | 0.5375 | 0.4787 |
| 0.60-0.70 | 1406 | 0.6436 | 0.5114 |
| 0.70-0.80 | 241 | 0.7178 | 0.4689 |
