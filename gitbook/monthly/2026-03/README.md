# 二级市场月报（2026-03）

## 2026 年 03 月二级市场月报（整月口径）

- 报告区间：2026-03-01 至 2026-03-31（整月）
- 生成时间：2026-04-01 14:50 UTC
- 口径说明：仅使用当月数据，核心指标按月内日频序列计算，衍生品指标按月内可得快照与日线汇总。
- 范围限定：本报告不使用跨月/跨年的趋势回看窗口。

## 数据可用性说明
- 全市场口径：CMC Global Metrics 日频历史。
- Top 资产与结构分化：CoinGecko + DefiLlama + CryptoSlam 月度快照。
- 衍生品口径：Deribit 公开 API（Funding、OI、DVOL）。
- 交易所横向比较：CMC 前排交易所样本（Binance/Coinbase/OKX/Bybit/KuCoin 等）。

## 参考样本与方法
- Coinbase：机构定位框架参考
  https://www.coinbase.com/institutional/research-insights/research/trading-insights/crypto-market-positioning-february-2026
- Binance：月报图表框架参考
  https://www.binance.com/en/research/analysis/monthly-market-insights-2026-02/
- KuCoin：日频快报语气参考
  https://www.kucoin.com/news/articles/crypto-daily-market-report-february-25-2026

## 2026 年 03 月核心结论
- 全市场市值：$2.30T -> $2.35T，月内变化 +1.82%。
- 全市场日均成交额：$96.95B。
- BTC 主导率：58.15% -> 58.20%，变化 +0.05pct。
- Top 资产月度分化：涨幅最高 TRX +12.07%；跌幅最大 BNB -1.47%。
- 市场广度（Top10 外占比，月末）：16.93%
- Deribit 资金费率（8h）：BTC=+0.000001，ETH=+0.000000。
- Deribit DVOL（月内）：BTC 51.04~60.45（月末 52.25）；ETH 72.37~79.33（月末 72.37）。

## 市值与主导率分析
3 月全市场总市值较月初小幅修复，BTC 主导率基本持平并维持高位，说明资金风险偏好有所回暖，但增量资金仍主要集中在 BTC 与头部资产，尚未明显扩散至长尾币种。

| 指标 | 月初 | 月末/均值 | 月内变化 |
| --- | --- | --- | --- |
| 全市场总市值 | $2.30T | $2.35T | +1.82% |
| 全市场日均成交额 | N/A | $96.95B | N/A |
| BTC 主导率 | 58.15% | 58.20% | +0.05pct |

![core_chart_1_marketcap.png](charts/core_chart_1_marketcap.png)

![core_chart_2_btc_dom.png](charts/core_chart_2_btc_dom.png)

## 前排交易所成交结构分析
前排样本 30d 成交额合计约 $4.65T，估算环比 -4.98%。
增幅靠前为 HTX（+9.64%），回落靠前为 KuCoin（-68.51%）。

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

![core_chart_3_exchange_30d_change.png](charts/core_chart_3_exchange_30d_change.png)

## 板块与资产分化
| 资产 | 月度涨跌 |
| --- | --- |
| TRX | +12.07% |
| LEO | +11.13% |
| ETH | +9.48% |
| WBT | +8.50% |
| BCH | +4.44% |
| BTC | +3.72% |
| DOGE | +1.38% |
| XRP | +0.35% |
| SOL | -0.76% |
| BNB | -1.47% |

| 指标 | 月末值 |
| --- | --- |
| Top10 外市值占比 | 16.93% |
| DeFi TVL（总量） | $92.29B |
| DeFi 链份额（ETH/SOL/BSC/Others） | 56.88% / 6.68% / 5.80% / 21.42% |
| NFT 月成交额 | $153.42M |

![fig2_top10_monthly_performance.png](charts/fig2_top10_monthly_performance.png)

![fig3_defi_tvl_share.png](charts/fig3_defi_tvl_share.png)

![fig4_monthly_nft_volume.png](charts/fig4_monthly_nft_volume.png)

![fig6_altcoin_outside_top10_share.png](charts/fig6_altcoin_outside_top10_share.png)

## 衍生品市场洞察（Deribit）
| 指标 | BTC | ETH |
| --- | --- | --- |
| Perp Funding（8h） | +0.000001 | +0.000000 |
| Future OI（聚合） | $2.00B | $515.18M |
| Option OI（聚合） | $378,195 | $2.08M |
| DVOL（月内区间） | 51.04 ~ 60.45（末值 52.25） | 72.37 ~ 79.33（末值 72.37） |

![chart_deribit_funding.png](charts/chart_deribit_funding.png)

![chart_deribit_oi.png](charts/chart_deribit_oi.png)

![chart_deribit_dvol.png](charts/chart_deribit_dvol.png)

## 情绪与波动观察
尽管总市值较月初有所修复，但恐惧情绪并未同步改善，说明这轮反弹更偏存量仓位修复而非增量资金持续进场。与此同时，BTC/ETH 已实现波动率与 DVOL 在月末都回到区间偏低位置，短线交易更需要警惕低情绪环境下的事件驱动型波动放大。

![core_chart_4_fng.png](charts/core_chart_4_fng.png)

![core_chart_5_realized_vol.png](charts/core_chart_5_realized_vol.png)

## 图表逐项解读（按 1 月月报风格）

### 图 1：全市场总市值（日频）
![core_chart_1_marketcap.png](charts/core_chart_1_marketcap.png)
- 数据现象：市值从 $2.30T 升至 $2.35T，月内变化 +1.82%。
- 区间特征：月内高低点区间 $2.56T -> $2.27T，区间回撤 -11.20%。
- 解释：月内呈现“上冲后回吐、月底企稳”的节奏，资金并未全面转向进攻，但头部资产承接仍在。

### 图 2：BTC 主导率（日频）
![core_chart_2_btc_dom.png](charts/core_chart_2_btc_dom.png)
- 数据现象：BTC.D 从 58.15% 升至 58.20%，变化 +0.05pct。
- 区间特征：主导率波动区间 57.90% ~ 59.20%。
- 解释：主导率基本持平且维持高位，说明反弹阶段资金仍优先配置 BTC 与头部资产，长尾扩散并不充分。

### 图 3：前排交易所 30d 成交额变化
![core_chart_3_exchange_30d_change.png](charts/core_chart_3_exchange_30d_change.png)
- 数据现象：样本内上涨 6 家、下跌 4 家，中位数变动 +1.09%。
- 分化点：增幅第一 HTX（+9.64%），跌幅第一 KuCoin（-68.51%）。
- 解释：头部平台成交保持韧性，但交易恢复并不均衡，说明用户活跃度仍优先回流到流动性和产品深度更强的平台。

### 图 4：Top 资产月度收益分布
![fig2_top10_monthly_performance.png](charts/fig2_top10_monthly_performance.png)
- 数据现象：最强 TRX +12.07%，最弱 BNB -1.47%，首尾价差 13.54pct。
- 结构特征：上涨资产 8 个，下跌资产 2 个。
- 解释：3 月头部资产整体偏修复，资金更偏好确定性较高的主流币与防御属性资产，全面风险偏好扩张仍未出现。

### 图 5：DeFi TVL 链份额
![fig3_defi_tvl_share.png](charts/fig3_defi_tvl_share.png)
- 数据现象：总 TVL $92.29B，ETH/SOL/BSC/Others 份额分别为 56.88% / 6.68% / 5.80% / 21.42%。
- 解释：以太坊仍是绝对流动性中枢，多链分散但尚未改变主链主导格局。

### 图 6：NFT 月成交额
![fig4_monthly_nft_volume.png](charts/fig4_monthly_nft_volume.png)
- 数据现象：3 月 NFT 交易额约 $153.42M。
- 解释：NFT 量能仍处低位，说明零售风险偏好修复有限，高波动题材尚未重新成为资金主线。

### 图 7：Top10 外市值占比
![fig6_altcoin_outside_top10_share.png](charts/fig6_altcoin_outside_top10_share.png)
- 数据现象：Top10 外市值占比 16.93%，核心资产合计占比 83.07%。
- 解释：市场广度仍弱，资金主要围绕 BTC 与头部资产交易。

### 图 8：Deribit 资金费率（Perp）
![chart_deribit_funding.png](charts/chart_deribit_funding.png)
- 数据现象：BTC=+0.000001、ETH=+0.000000（8h）。
- 解释：BTC 与 ETH 资金费率都贴近零轴，说明杠杆方向性并不强，衍生品仓位更多体现中性博弈而非单边拥挤。

### 图 9：Deribit OI 结构（Future vs Option）
![chart_deribit_oi.png](charts/chart_deribit_oi.png)
- 数据现象：BTC Future OI $2.00B、Option OI $378,195；ETH Future OI $515.18M、Option OI $2.08M。
- 结构特征：Option/Future OI 比例 BTC 0.0189%、ETH 0.4029%。
- 解释：OI 主要集中在永续/期货，期权端更偏风险对冲与事件交易。

### 图 10：Deribit DVOL（月内）
![chart_deribit_dvol.png](charts/chart_deribit_dvol.png)
- 数据现象：BTC DVOL 51.04~60.45（峰值日 2026-03-08）；ETH DVOL 72.37~79.33（峰值日 2026-03-19）。
- 波动脉冲：BTC 峰值较低位 +18.44%，ETH 峰值较低位 +9.62%。
- 解释：隐含波动率在月内事件窗口短暂抬升，但月末已回到区间下沿附近，风险溢价整体呈收敛状态。

### 图 11：恐惧与贪婪指数（F&G，日频）
![core_chart_4_fng.png](charts/core_chart_4_fng.png)
- 数据现象：月末指数 11（极度恐惧），月内区间 8~28，均值 14.23。
- 极端恐惧天数：26 天。
- 解释：零售情绪修复缓慢，风险偏好恢复仍需要更长验证周期。

### 图 12：BTC/ETH 7D 已实现波动率
![core_chart_5_realized_vol.png](charts/core_chart_5_realized_vol.png)
- 数据现象：月末 BTC RV 46.00%、ETH RV 58.79%；月内区间 BTC 21.77%~76.87%，ETH 24.84%~108.51%。
- 相对波动：月末 ETH 较 BTC 高 12.78pct。
- 解释：ETH 波动弹性仍高于 BTC，风险预算配置需维持分层仓位管理。

## 风险与运营建议
1. 盘口与库存：主流币对维持深度优先，长尾币对库存上限与滑点阈值同步收紧。
2. 风控联动：将 Funding、DVOL、Top10 外占比纳入统一预警，触发阈值时自动提升保证金提示。
3. 用户沟通：在恐惧区间加强风险教育与仓位管理提示，避免用户在低情绪反弹阶段追涨或过度加杠杆。

## 月内图表索引
- core_chart_1_marketcap.png
- core_chart_2_btc_dom.png
- fig2_top10_monthly_performance.png
- fig3_defi_tvl_share.png
- fig4_monthly_nft_volume.png
- fig6_altcoin_outside_top10_share.png
- chart_deribit_funding.png
- chart_deribit_oi.png
- chart_deribit_dvol.png
- core_chart_3_exchange_30d_change.png
- core_chart_4_fng.png
- core_chart_5_realized_vol.png

## 数据源
- CMC Global Historical: `https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical`
- CMC Exchange Quotes: `https://api.coinmarketcap.com/data-api/v3/exchange/quotes/latest`
- CoinGecko Markets: `https://api.coingecko.com/api/v3/coins/markets`
- DefiLlama Historical TVL: `https://api.llama.fi/v2/historicalChainTvl`
- CryptoSlam Global Sales: `https://web-api.cryptoslam.io/v1/global/sales`
- Deribit Public API: `https://www.deribit.com/api/v2`
- Alternative.me F&G: `https://api.alternative.me/fng/`
- CoinMetrics (State of the Network #348): `https://coinmetrics.substack.com/p/state-of-the-network-issue-348`

## 执行状态
- fig2: ok
- fig3: ok
- fig4: ok
- fig6: ok
- deribit: ok
- core_report: ok
