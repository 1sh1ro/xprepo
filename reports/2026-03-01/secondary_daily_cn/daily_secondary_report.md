# 二级市场日报（2026-03-01）

## 关键结论
- 全市场市值 $2.30T（24h +1.41%），成交额 $102.41B（24h +5.23%）。
- BTC 主导率 58.15%（+0.17pct），Top10 外占比 8.22% 。
- Top10 资产上涨 8 / 下跌 2，平均涨跌幅 +2.91%，首尾分化 7.79pct。
- 衍生品：BTC/ETH funding 分别为 -0.39bps / +0.00bps，DVOL 收盘 54.69 / 72.42。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)
截至 2026-03-01，全市场市值 $2.30T，24h 成交额 $102.41B，BTC 主导率 58.15%。
数据来源：CMC `global-metrics/quotes/historical`

![全市场当日变化](charts/chart_market_daily_change.png)
相对前日，市值 +1.41%、成交 +5.23%、BTC.D +0.17pct。
数据来源：CMC `global-metrics/quotes/historical`

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)
当前结构为 BTC 58.15% / Top2-10 33.64% / Top10 外 8.22%。长尾占比仍偏低，广度修复还未形成持续趋势。
数据来源：CMC 全市场 + CoinGecko Top10 市值聚合

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)
Top10 中领涨 SOL（+6.87%），尾部 FIGR_HELOC（-0.92%），均值 +2.91%。分化 7.79pct，结构性交易仍是主导。
数据来源：CoinGecko `coins/markets`

![前排交易所24h变化](charts/chart_exchange_24h_change.png)
前排样本上涨 1 家、下跌 9 家，均值 -8.07%。KuCoin 最强（+2.56%），MEXC 最弱（-20.93%）。
数据来源：CMC `exchange/quotes/latest`

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)
样本内衍生品成交占比 84.65%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
数据来源：CMC `exchange/quotes/latest`（spotVolumeUsd / derivativeVolumeUsd）

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)
Funding 仍在中性附近，BTC/ETH 分别 -0.39bps / +0.00bps；Perp OI 为 $1.06B / $343.37M；DVOL 位于 Neutral（中性波动定价） / Panic（高波动溢价）。
数据来源：Deribit `public/ticker`、`public/get_volatility_index_data`

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)
F&G 当日 14（较前日 +3）；配合 BTC/ETH DVOL 54.69/72.42，当前更像情绪修复中的高波动区。
数据来源：Alternative.me `/fng/` + Deribit DVOL

## 未来24小时观察点
- 若 Top10 外占比持续抬升且 BTC.D 回落，说明风险偏好开始从核心资产外溢。
- 若交易所衍生品占比继续升高但 funding 仍中性，行情更可能表现为高波动震荡。
- 若 F&G 反弹而 DVOL 不降，需警惕情绪修复与波动定价背离。

## 数据来源
- CMC global metrics historical (data-api)
- CMC exchange quotes latest (data-api)
- CoinGecko coins/markets
- Deribit public API
- Alternative.me F&G API
