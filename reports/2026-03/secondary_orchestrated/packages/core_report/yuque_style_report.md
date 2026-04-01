# 202603

## 2026 年 03 月核心市场洞察

- 市值与主导率分析
- 前排交易所成交结构分析
- 市场情绪：恐惧贪婪指数
- 风险与运营建议

本月市场呈现“去杠杆回落、结构分化”的特征，前排交易所整体成交额较前一观察窗口收缩，但头部内部出现分化。


### 2026 年 03 月核心结论
- 总成交额与流动性：前排样本滚动 30 天成交额为 $4.65T，估算环比 -4.98%。
- 全市场总市值：$2.30T -> $2.35T，月内变化 +1.82%。
- 全市场日均 24h 成交额：$96.95B。
- BTC 主导率：+58.15% -> +58.20%。
- 恐惧贪婪指数：11（Extreme Fear）。
- 稳定币资金面：市值 $288.40B，24h 成交量 $97.26B。

![chart-marketcap](charts/chart_1_marketcap.png)

值得注意的是，本期市值下行与主导率回落并存，说明市场风险偏好没有简单回归，仍处于结构性再定价阶段。

## 市值与主导率分析
根据 CMC 全市场历史数据，2 月份总市值整体下移；BTC 主导率虽有回落，但仍维持在高位区间。

![chart-btc-dom](charts/chart_2_btc_dom.png)

这意味着交易量仍倾向集中在核心资产交易对，长尾资产流动性修复较慢。

## 前排交易所成交结构分析
我们以 CMC 前排样本进行横向对比，重点观察 `30d 成交额变化` 与 `24h 现货/衍生品结构`。

![chart-ex-30d](charts/chart_3_exchange_30d_change.png)

关键观察：
1. 增幅靠前：HTX (+9.64%), OKX (+5.59%)。
2. 回落靠前：KuCoin (-68.51%), Upbit (-19.76%)。
3. 结构上，衍生品成交占比在样本内依旧偏高，波动放大风险需持续跟踪。

## 资金费率与波动率观察
参考交易所衍生品月报口径，本节给出资金费率快照与波动率代理指标。
- Deribit BTC-PERP funding: +0.00%
- Deribit ETH-PERP funding: +0.00%
- 全市场衍生品 24h 成交量（CMC）：$825.89B

![chart-rv](charts/chart_5_realized_vol.png)

该图使用 BTC/ETH 7 日已实现波动率（年化）作为期权隐波的替代温度计：上行通常对应风险对冲需求抬升。

## 市场情绪：恐惧贪婪指数
恐惧贪婪指数在本月维持低位震荡，零售情绪修复缓慢。

![chart-fng](charts/chart_4_fng.png)

关键时点分析：
1. 若指数持续低于 25，通常意味着风险偏好尚未恢复。
2. 若指数快速回升并突破 50，往往对应短期交易活跃度提升。

## 社媒与搜索热度（Trending）
以 CoinGecko Trending 作为公开可得的搜索热度代理。
| Symbol | Name | MCap Rank | Price (BTC) |
| --- | --- | --- | --- |
| STO | StakeStone | 304 | 0.00000511 |
| NOM | Nomina | 818 | 0.00000010 |
| MUSD | Mezo USD | 839 | 0.00001460 |
| SIREN | Siren | 172 | 0.00000393 |
| ALGO | Algorand | 68 | 0.00000153 |
| BASED | Based | 799 | 0.00000127 |
| ERG | Ergo | 732 | 0.00000427 |
| HYPE | Hyperliquid | 16 | 0.00053870 |
| TAO | Bittensor | 33 | 0.00475322 |
| BTC | Bitcoin | 1 | 1.00000000 |

## 稳定币与资金面观察
- 稳定币市值：$288.40B
- 稳定币 24h 成交量：$97.26B
- DeFi 市值：$58.79B
- DeFi 24h 成交量：$10.39B

## 风险与运营建议
1. 风险监控：将“衍生品占比 + 30d 量能变化 + F&G”纳入统一预警面板。
2. 业务策略：在主流币对维持深度，同时控制长尾币对库存与做市风险。
3. 对外披露：参考 PoR 风格，补充负债口径与地址级储备说明，增强用户信任。

## 附录：前排交易所明细
| Rank | Exchange | 30d Volume | 30d Change | 7d Change | 24h Spot | 24h Deriv |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Binance | $2.06T | +4.67% | +5.60% | $8.82B | $56.13B |
| 2 | Coinbase Exchange | $60.77B | -2.86% | +9.86% | $1.84B | $0 |
| 3 | Upbit | $40.22B | -19.76% | -5.39% | $1.00B | $0 |
| 6 | OKX | $607.76B | +5.59% | +7.26% | $1.75B | $24.27B |
| 7 | Bybit | $525.41B | +1.66% | -2.86% | $2.15B | $15.73B |
| 8 | Bitget | $343.31B | +4.21% | +4.83% | $1.17B | $9.89B |
| 9 | Gate | $535.49B | -14.12% | +7.45% | $1.83B | $14.27B |
| 10 | KuCoin | $138.64B | -68.51% | -58.28% | $2.14B | $3.28B |
| 12 | MEXC | $229.18B | +0.52% | -7.09% | $2.21B | $12.96B |
| 22 | HTX | $115.69B | +9.64% | +21.79% | $1.35B | $3.15B |

## 数据源
- CMC Exchange Quotes: `https://api.coinmarketcap.com/data-api/v3/exchange/quotes/latest`
- CMC Global Historical: `https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical`
- CMC Global Latest: `https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/latest`
- CoinGecko Trending: `https://api.coingecko.com/api/v3/search/trending`
- CoinGecko Market Chart: `https://api.coingecko.com/api/v3/coins/{id}/market_chart`
- CoinMetrics (State of the Network #348): `https://coinmetrics.substack.com/p/state-of-the-network-issue-348`
- Deribit Ticker: `https://www.deribit.com/api/v2/public/ticker`
- Alternative.me F&G: `https://api.alternative.me/fng/`
- CMC 快照时间：`2026-04-01T14:49:58.931Z`
- 明细数据：`yuque_style_exchange_data.csv`