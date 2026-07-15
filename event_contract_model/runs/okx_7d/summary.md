# BTC 10m Event Model Run

- Product: `BTC-USDT-SWAP`
- Horizon: `10 minutes`
- Train rows: `7049` from `2026-06-03T16:10:00+00:00` to `2026-06-08T13:38:00+00:00`
- Test rows: `3022` from `2026-06-08T13:39:00+00:00` to `2026-06-10T16:00:00+00:00`
- Test up rate: `0.4838`
- Accuracy all: `0.5023`
- AUC: `0.5025`
- Brier score: `0.2500`
- Average confidence: `0.5177`
- Selected threshold: `0.55`
- Selected rows: `74` (`2.45%` coverage)
- Selected accuracy: `0.6081`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 3022 | 100.00% | 0.5023 | 0.5177 |
| 0.52 | 1104 | 36.53% | 0.5109 | 0.5320 |
| 0.55 | 74 | 2.45% | 0.6081 | 0.5583 |
| 0.58 | 1 | 0.03% | 1.0000 | 0.5807 |
| 0.60 | 0 | 0.00% | N/A | N/A |
| 0.65 | 0 | 0.00% | N/A | N/A |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.40-0.50 | 2038 | 0.4801 | 0.4863 |
| 0.50-0.60 | 984 | 0.5130 | 0.4787 |
