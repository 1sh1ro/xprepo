# BTC 10m Event Model Run

- Product: `BTC-USDT-SWAP`
- Horizon: `10 minutes`
- Train rows: `30233` from `2026-05-11T16:13:00+00:00` to `2026-06-01T16:05:00+00:00`
- Test rows: `12958` from `2026-06-01T16:06:00+00:00` to `2026-06-10T16:03:00+00:00`
- Test up rate: `0.4691`
- Accuracy all: `0.5302`
- AUC: `0.5243`
- Brier score: `0.2495`
- Average confidence: `0.5298`
- Selected threshold: `0.55`
- Selected rows: `2223` (`17.16%` coverage)
- Selected accuracy: `0.5385`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 12958 | 100.00% | 0.5302 | 0.5298 |
| 0.52 | 7094 | 54.75% | 0.5368 | 0.5465 |
| 0.55 | 2223 | 17.16% | 0.5385 | 0.5772 |
| 0.58 | 707 | 5.46% | 0.5304 | 0.6104 |
| 0.60 | 370 | 2.86% | 0.5486 | 0.6297 |
| 0.65 | 66 | 0.51% | 0.6212 | 0.6817 |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.10-0.20 | 1 | 0.1450 | 0.0000 |
| 0.20-0.30 | 8 | 0.2859 | 0.3750 |
| 0.30-0.40 | 265 | 0.3742 | 0.4906 |
| 0.40-0.50 | 7880 | 0.4711 | 0.4503 |
| 0.50-0.60 | 4708 | 0.5234 | 0.4960 |
| 0.60-0.70 | 92 | 0.6279 | 0.6304 |
| 0.70-0.80 | 4 | 0.7072 | 1.0000 |
