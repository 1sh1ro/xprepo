# BTC 10 Minute Event Contract 120 Day Backtest

Run date: 2026-06-11 Asia/Shanghai.

This report summarizes the 120 day BTC/USD 1 minute backtest. The goal is to predict whether BTC will be higher or lower 10 minutes after the current candle.

## Data

- Source: Bitstamp public BTC/USD OHLC endpoint.
- Bar size: 1 minute.
- Rows fetched: 172,801.
- Data range UTC: 2026-02-10 17:01 to 2026-06-10 17:01.
- Label: `future_close[t+10m] > close[t]`.
- Holdout split: chronological, last 25%.
- Test rows: 43,198.
- Test period UTC: 2026-05-11 16:54 to 2026-06-10 16:51.

Bitstamp was used for the 120 day run because OKX and Coinbase TLS connections were unstable from this environment, while Binance futures historical-window requests returned HTTP 451.

## Implemented Improvements

- Added resumable/checkpointed candle fetching so long historical pulls survive transient network failures.
- Added Bitstamp and Binance source support alongside OKX and Coinbase.
- Added `logistic_raw`, an uncalibrated strongly regularized logistic model for higher signal coverage.
- Ran 120 day model comparison across calibrated logistic, raw logistic, ExtraTrees, and auto selection.
- Saved a logistic parameter sweep to `runs/bitstamp_120d_logistic_sweep.csv`.

## Main Results

| Run | Model | Threshold | Test accuracy | AUC | Selected rows | Coverage | Selected accuracy |
|---|---|---:|---:|---:|---:|---:|---:|
| `bitstamp_120d_logistic_v1` | logistic | 0.50 | 51.41% | 0.5235 | 43,198 | 100.00% | 51.41% |
| `bitstamp_120d_logistic_thr058` | logistic | 0.58 | 51.41% | 0.5235 | 558 | 1.29% | 58.24% |
| `bitstamp_120d_logistic_raw_thr055` | logistic_raw | 0.55 | 51.48% | 0.5230 | 9,025 | 20.89% | 53.23% |
| `bitstamp_120d_extra_trees_v1` | extra_trees | 0.58 | 51.56% | 0.5218 | 1,203 | 2.78% | 51.95% |
| `bitstamp_120d_auto_v1` | auto chose logistic | 0.50 | 51.41% | 0.5235 | 43,198 | 100.00% | 51.41% |

## Logistic Threshold Curve

The calibrated logistic model is weak as an always-on predictor, but its highest-confidence slice is meaningfully better.

| Confidence >= | Rows | Coverage | Accuracy |
|---:|---:|---:|---:|
| 0.50 | 43,198 | 100.00% | 51.41% |
| 0.52 | 22,316 | 51.66% | 52.40% |
| 0.55 | 3,638 | 8.42% | 53.30% |
| 0.58 | 558 | 1.29% | 58.24% |
| 0.60 | 170 | 0.39% | 65.29% |

## Recommendation

Use `runs/bitstamp_120d_logistic_thr058` as the conservative event-contract model. It outputs direction and confidence, but should only be treated as a trade candidate when confidence is at least `0.58`.

Use `runs/bitstamp_120d_logistic_raw_thr055` only when higher signal frequency is needed. It produces many more signals, but the selected accuracy is much closer to random and will be more sensitive to fees, spread, and settlement edge.

This is still a research model, not a production edge. The next useful optimization is a rolling walk-forward backtest and payout-aware thresholding, because event-contract profitability depends on entry odds, fees, slippage, and settlement latency, not accuracy alone.
