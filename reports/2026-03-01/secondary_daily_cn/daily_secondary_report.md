# 二级市场日报（2026-03-01）

## 关键结论
- 全市场市值：$2.30T（+1.41%） | 24h 成交额：$102.41B（+5.23%）
- 资产广度（Top10）：上涨 7 / 下跌 3 | BTC 主导率：58.15%（+0.17pct）
- 衍生品：BTC/ETH funding_8h -0.000040 / +0.000000；DVOL 54.71 / 72.39
- 结构特征：Top10 平均涨跌幅 +2.56%，最大分化 7.02pct。

## 当日脉冲
统计日期：2026-03-01。全市场总市值 $2.30T，24h 成交额 $102.41B，BTC 主导率 58.15%。价格与成交同步走高，风险偏好边际修复。

### 交易所成交变化
![前排交易所24h变化](charts/chart_exchange_24h_change.png)
前排样本中，上涨 2 家、下跌 8 家，均值 -6.66%。KuCoin 24h 成交额增速领先（+2.13%），MEXC 表现偏弱（-20.06%），说明流量仍处于分化而非普涨状态。
数据来源：CMC `exchange/quotes/latest`（前排交易所样本）

### Top10 资产表现
![Top10资产24h表现](charts/chart_top10_assets_24h.png)
Top10 资产中上涨 7 个、下跌 3 个，平均涨跌幅 +2.56%。领涨资产为 SOL（+6.10%），尾部为 FIGR_HELOC（-0.92%），首尾分化 7.02pct，表明市场仍以结构性机会为主。
数据来源：CoinGecko `coins/markets`（按市值前10）

## 衍生品与风险
![衍生品快照](charts/chart_derivatives_snapshot.png)
BTC/ETH funding 8h 分别为 -0.40bps 与 +0.00bps，杠杆方向并未出现单边拥挤。DVOL 收盘分别为 BTC 54.71、ETH 72.39，处于 Neutral（中性波动定价） / Panic（高波动溢价） 阶段，显示期权端对尾部波动仍保留一定风险溢价。
数据来源：Deribit `public/ticker`、`public/get_volatility_index_data`

## 情绪与风险偏好
恐惧贪婪指数为 14，较前日 +3。
情绪仍在恐惧区，短线反弹更容易受事件扰动。
数据来源：Alternative.me `/fng/`

## 未来24小时观察点
- 交易所样本中负增长平台数量是否继续上升，验证流量是否进一步向头部集中。
- Top10 首尾分化是否收敛，判断行情是否从结构性反弹转向普涨。
- DVOL 是否从当前阶段继续抬升或回落，决定波动率策略应偏防守还是偏交易。

## 数据来源
- CMC global metrics historical (data-api)
- CMC exchange quotes latest (data-api)
- CoinGecko coins/markets
- Deribit public API
- Alternative.me F&G API
