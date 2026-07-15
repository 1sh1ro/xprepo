# BTC 10m Event Model Run

- Product: `btcusd`
- Horizon: `10 minutes`
- Model: `extra_trees`
- Train rows: `129593` from `2026-02-10T17:01:00+00:00` to `2026-05-11T16:53:00+00:00`
- Fit rows: `103674`
- Validation rows: `25919`
- Test rows: `43198` from `2026-05-11T16:54:00+00:00` to `2026-06-10T16:51:00+00:00`
- Test up rate: `0.4839`
- Accuracy all: `0.5156`
- AUC: `0.5218`
- Brier score: `0.2499`
- Average confidence: `0.5261`
- Selected threshold: `0.58`
- Selected rows: `1203` (`2.78%` coverage)
- Selected accuracy: `0.5195`

## Threshold Slices

| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |
|---:|---:|---:|---:|---:|
| 0.50 | 43198 | 100.00% | 0.5156 | 0.5261 |
| 0.52 | 22891 | 52.99% | 0.5220 | 0.5402 |
| 0.55 | 4979 | 11.53% | 0.5403 | 0.5702 |
| 0.58 | 1203 | 2.78% | 0.5195 | 0.5994 |
| 0.60 | 473 | 1.09% | 0.5581 | 0.6155 |
| 0.65 | 8 | 0.02% | 0.8750 | 0.6577 |
| 0.70 | 0 | 0.00% | N/A | N/A |

## Calibration Buckets

| P(up) bucket | Rows | Avg predicted up | Actual up rate |
|---:|---:|---:|---:|
| 0.30-0.40 | 51 | 0.3904 | 0.3922 |
| 0.40-0.50 | 21472 | 0.4766 | 0.4683 |
| 0.50-0.60 | 21253 | 0.5268 | 0.4985 |
| 0.60-0.70 | 422 | 0.6163 | 0.5521 |
