# BTC 10m Event Model Run

- Product: `BTC-USDT-SWAP`
- Horizon: `10 minutes`
- Train rows: `14105` from `2026-05-27T16:12:00+00:00` to `2026-06-06T11:16:00+00:00`
- Test rows: `6046` from `2026-06-06T11:17:00+00:00` to `2026-06-10T16:02:00+00:00`
- Test up rate: `0.4977`
- Accuracy all: `0.5020`
- AUC: `0.4988`
- Brier score: `0.2521`
- Average confidence: `0.5424`
- Selected threshold: `0.55`
- Selected rows: `1816` (`30.04%` coverage)
- Selected accuracy: `0.4862`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 6046 | 100.00% | 0.5020 | 0.5424 |
| 0.52 | 5378 | 88.95% | 0.5054 | 0.5461 |
| 0.55 | 1816 | 30.04% | 0.4862 | 0.5649 |
| 0.58 | 206 | 3.41% | 0.5340 | 0.6030 |
| 0.60 | 67 | 1.11% | 0.4776 | 0.6360 |
| 0.65 | 19 | 0.31% | 0.2632 | 0.6921 |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.20-0.30 | 6 | 0.2853 | 1.0000 |
| 0.30-0.40 | 59 | 0.3712 | 0.4576 |
| 0.40-0.50 | 5881 | 0.4582 | 0.4977 |
| 0.50-0.60 | 98 | 0.5133 | 0.5000 |
| 0.60-0.70 | 2 | 0.6134 | 0.0000 |
