# 二级市场日报（2026-07-19）

## 关键结论
- 全市场市值 $2.21T（24h +0.95%），成交额 $36.46B（24h -43.25%）。
- BTC 主导率 58.78%（+0.27pct），Top10 外占比 8.23%。
- Top10 资产上涨 7 / 下跌 3，平均涨跌幅 +0.99%，首尾分化 4.16pct。
- 衍生品：BTC/ETH 资金费率分别为 +1.31bps / +0.03bps，DVOL 收盘 36.01 / 49.75。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Range Trading`。价格与成交未形成同向趋势，市场仍在区间内进行结构轮动。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交走弱，流动性恢复仍依赖少数头部平台；从杠杆维度看，多头付费抬升，杠杆侧开始拥挤，需警惕回撤时的资金费率反转；在风险定价层面，隐含波动率回落至相对低位，事件冲击前的保护成本下降；再结合情绪与价格修复节奏尚未完全同步。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](charts/chart_btc_eth_24h_trend.png)

- BTC/ETH 24h 趋势数据暂不可用。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +2.72%。
其中包含奖励补贴的池有 3 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 1.99% 至 6.86% 区间。
- 资金集中：TVL 主要集中在 Spark-USDT（Ethereum，TVL $412.18M）、Aave-USDT（Ethereum，TVL $80.24M）。
- 收益领先：当前收益靠前样本包括 Aave-USDT（Ethereum，Total 6.86%）、Aave-USDC（Ethereum，Total 6.78%）。

风险提示
- 利用率达到 70% 以上的池有 7 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-DAI（Ethereum） 92.23%，Borrow APY 6.18%。
- 奖励收益池数量：3 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(8)，Compound API(6)，DefiLlama(21)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | DAI | 4.24% | 6.18% | N/A | 4.15% | 92.23% | $8.52M | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 2.75% | N/A | N/A | 2.75% | N/A | $412.18M | DefiLlama |
| Compound | Ethereum | USDS | 3.19% | 3.96% | 0.00% | 3.19% | 88.57% | $1.87M | Compound API |
| Aave | Ethereum | PYUSD | 2.91% | 4.39% | N/A | 2.87% | 74.13% | $2.87M | DefiLlama+Aave API |
| Aave | Ethereum | USDT | 2.64% | 3.61% | 4.26% | 6.86% | 81.58% | $80.24M | DefiLlama+Aave API |
| Aave | Ethereum | USDC | 3.26% | 4.01% | 3.57% | 6.78% | 90.50% | $65.07M | DefiLlama+Aave API |
| Aave | Ethereum | USDS | 0.14% | 5.68% | 3.42% | 3.56% | 3.46% | $11.44M | DefiLlama+Aave API |
| Aave | Base | USDC | 3.13% | 4.23% | N/A | 3.09% | 82.80% | $31.28M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 2.90% | 3.83% | N/A | 2.86% | 84.56% | $25.52M | DefiLlama+Aave API |
| Aave | Arbitrum | DAI | 2.01% | 3.91% | N/A | 1.99% | 69.05% | $1.11M | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 22 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 3.26% | 4.01% | 3.57% | 6.78% | 90.50% | $65.07M | DefiLlama+Aave API |
| USDC | Aave | Arbitrum | 2.90% | 3.83% | N/A | 2.86% | 84.56% | $25.52M | DefiLlama+Aave API |
| USDC | Aave | Base | 3.13% | 4.23% | N/A | 3.09% | 82.80% | $31.28M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.60% | N/A | N/A | 3.60% | N/A | $273.30M | DefiLlama |
| USDC | Compound | Ethereum | 3.20% | 3.97% | 0.10% | 3.31% | 88.99% | $336.93M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.69% | 3.57% | 0.00% | 2.69% | 74.62% | $15.71M | DefiLlama+Compound API |
| USDC | Compound | Base | 5.74% | 6.82% | 0.00% | 5.74% | 90.78% | $8.42M | DefiLlama+Compound API |
| USDT | Aave | Ethereum | 2.64% | 3.61% | 4.26% | 6.86% | 81.58% | $80.24M | DefiLlama+Aave API |
| USDT | Spark | Ethereum | 2.75% | N/A | N/A | 2.75% | N/A | $412.18M | DefiLlama |
| USDT | Compound | Ethereum | 2.73% | 3.61% | 0.10% | 2.83% | 75.87% | $193.03M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 1.94% | 3.00% | 0.00% | 1.94% | 54.01% | $19.62M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 4.24% | 6.18% | N/A | 4.15% | 92.23% | $8.52M | DefiLlama+Aave API |
| DAI | Aave | Arbitrum | 2.01% | 3.91% | N/A | 1.99% | 69.05% | $1.11M | DefiLlama+Aave API |
| DAI | Spark | Ethereum | 2.34% | N/A | N/A | 2.34% | N/A | $103.10M | DefiLlama |
| USDS | Aave | Ethereum | 0.14% | 5.68% | 3.42% | 3.56% | 3.46% | $11.44M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.20% | N/A | N/A | 2.20% | N/A | $220.03M | DefiLlama |
| USDS | Spark | Arbitrum | 3.60% | N/A | N/A | 3.60% | N/A | $360.59M | DefiLlama |
| USDS | Spark | Base | 3.60% | N/A | N/A | 3.60% | N/A | $11.94M | DefiLlama |
| USDS | Compound | Ethereum | 3.19% | 3.96% | 0.00% | 3.19% | 88.57% | $1.87M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.29M | DefiLlama |
| PYUSD | Aave | Ethereum | 2.91% | 4.39% | N/A | 2.87% | 74.13% | $2.87M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.28% | N/A | N/A | 0.28% | N/A | $91.46M | DefiLlama |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 22 条；DefiLlama 扩展样本 91 条（展示 Top20）；Bitcompare 稳定币利率样本 0 条。
- 覆盖维度：扩展样本覆盖 46 个协议、15 条链、61 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | 3.60% | N/A | 3.60% | $4.79B | DefiLlama API |
| USDC | maple | Ethereum | 4.83% | 0.00% | 4.83% | $3.21B | DefiLlama API |
| USYC | circle-usyc | BSC | 3.05% | N/A | 3.05% | $2.87B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 4.00% | N/A | 4.00% | $1.57B | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $1.11B | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.51% | N/A | 3.51% | $962.46M | DefiLlama API |
| USDT | maple | Ethereum | 4.19% | 0.00% | 4.19% | $932.20M | DefiLlama API |
| USDS | centrifuge-protocol | Ethereum | 3.33% | N/A | 3.33% | $869.60M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.17% | N/A | 3.17% | $821.87M | DefiLlama API |
| BUIDL | blackrock-buidl | Avalanche | 3.48% | N/A | 3.48% | $736.05M | DefiLlama API |
| USTB | invesco-ustb | Ethereum | 3.30% | N/A | 3.30% | $653.32M | DefiLlama API |
| BUIDL | blackrock-buidl | Solana | 3.48% | N/A | 3.48% | $547.36M | DefiLlama API |
| USDY | ondo-yield-assets | Stellar | 3.55% | N/A | 3.55% | $532.92M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 2.25% | 2.25% | $507.85M | DefiLlama API |
| USDD | justlend-v1 | Tron | 0.02% | 3.94% | 3.96% | $447.40M | DefiLlama API |
| GTUSDCP | morpho-blue | Base | 4.26% | 0.00% | 4.26% | $426.68M | DefiLlama API |
| USDC | jupiter-lend | Solana | 3.82% | 0.72% | 4.54% | $420.16M | DefiLlama API |
| AUSD | centrifuge-protocol | Ethereum | 2.57% | N/A | 2.57% | $374.35M | DefiLlama API |
| STEAKUSDC | morpho-blue | Base | 4.27% | 0.00% | 4.27% | $369.36M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | 3.60% | N/A | 3.60% | $360.59M | DefiLlama API |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## RWA 结构观察
![RWA资产类别快照](charts/chart_rwa_asset_class_snapshot.png)

RWA.xyz 公开页快照显示，样本资产类别合计约 $28.00B；最大类别为 U.S. Treasuries（$15.98B，7D +3.19%）。7D 上升类别 5 个、下降类别 0 个，说明 RWA 当前更适合当作结构变量，而不是日内方向信号。
其中股票、主动策略和非美债这类交易属性更强的类别合计约 $4.98B，占样本 17.80%。这部分更接近 CEX 新品类、Perps 和跨资产成交额的观察入口。

RWA 资产类别对照表
| 类别 | 规模 | 7D变化 | as of |
|---|---:|---:|---|
| U.S. Treasuries | $15.98B | +3.19% | 2026-07-17 |
| Credit | $7.03B | +4.25% | 2026-07-17 |
| Tokenized Stocks | $1.85B | +14.39% | 2026-07-17 |
| Active Strategies | $1.77B | +14.34% | 2026-07-17 |
| Non-U.S. Government Debt | $1.36B | +3.86% | 2026-07-17 |

交易含义：RWA 放在日报里可以，但应定位为二级市场的产品线与风险偏好背景；只有 tokenized stocks、RWA perps、可交易收益资产扩容时，才更直接影响交易所成交结构。
数据源：RWA.xyz 公开资产类别页；正式 API 可在设置 RWA_API_KEY 后替换为更稳定口径。

## 非 DeFi（交易所期现）
![非DeFi期现快照](charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：OKX-BTC，年化约 8.70%。
- Funding 最低样本：OKX-ETH，年化约 1.48%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.64% · 500k | 0.01%/2.51% · 5.0M | N/A | N/A | N/A | OKX 0.01% |
| USDC | 0.01%/4.22% · 500k | 0.01%/2.51% · 1.0M | N/A | N/A | N/A | OKX 0.01% |
| BTC | 0.00%/0.38% · 100 | 0.00%/0.51% · 175 | N/A | N/A | N/A | Binance 0.00% |
| ETH | 0.01%/2.27% · 2k | 0.00%/1.51% · 7k | N/A | N/A | N/A | OKX 0.00% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)

截至 2026-07-19，全市场市值 $2.21T，24h 成交额 $36.46B，BTC 主导率 58.78%。
价格上涨但成交回落，反弹质量偏弱，需警惕高位回吐。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](charts/chart_market_daily_change.png)

相对前日，市值 +0.95%、成交 -43.25%、BTC.D +0.27pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 58.78% / Top2-10 32.99% / Top10 外 8.23%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)

Top10 中领涨 HYPE（+3.76%），尾部 BNB（-0.40%），均值 +0.99%。分化 4.16pct，结构性交易仍是主导。
上涨家数明显占优，但首尾分化仍大，表明反弹并非无差别普涨。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](charts/chart_exchange_24h_change.png)

前排样本上涨 0 家、下跌 10 家，均值 -34.98%。Upbit 最强（-8.01%），MEXC 最弱（-50.01%）。
最强与最弱平台的 24h 变化差达到 42.00pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 84.71%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品仍是主导成交形态，价格连续性更多由杠杆侧情绪决定。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 +1.31bps / +0.03bps；未平仓合约（OI）为 $750.83M / $281.59M；隐含波动率指数（DVOL）位于 Complacency（低波动定价） / Neutral（中性波动定价）。
多头付费抬升且波动仍高，组合信号偏向拥挤，需防范回撤时杠杆反身性。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 28（较前日 +3）；配合 BTC/ETH DVOL 36.01/49.75，当前更像情绪修复中的高波动区。
情绪回到中性区，若后续成交和广度同步改善，趋势性机会会明显增多。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

## OKX 聪明钱仓位结构（Top10交易员）
聪明钱榜单数据暂不可用（见 Data Gaps）。

仓位结构暂不可用（见 Data Gaps）。

BTC/ETH 聪明钱聚合信号未启用（设置 `OKX_SMARTMONEY_FETCH_SIGNAL=1` 可尝试拉取）。

交易含义：聪明钱仓位更适合做方向与拥挤度监控，不应单独作为开仓触发。

## OKX 新闻情绪快照
OKX 新闻情绪快照暂不可用（见 Data Gaps）。

## 未来24小时观察
1. 若 Top10 外占比继续抬升且 BTC.D 回落，说明风险偏好开始从核心资产向外扩散。
2. 若衍生品占比继续上升而 funding 仍中性，盘面大概率维持高波动震荡而非顺滑上行。
3. 若 F&G 反弹但 DVOL 不降，代表情绪与风险定价背离，追涨胜率会明显下降。

## 交易与风控含义
- 仓位管理优先级高于方向押注，建议保持核心仓位稳定、战术仓位滚动。
- 若交易所衍生品占比继续上升，建议同步收紧杠杆和止损参数。
- 关注情绪改善与广度扩散是否同步发生，二者背离时避免追逐单边。

## 数据缺口（Data Gaps）
- Binance BTC/ETH 24h 批量数据获取失败，转单币重试: HTTP Error 451: 
- Binance 24h 单币数据获取失败 BTCUSDT: HTTP Error 451: 
- Binance 24h 未返回 BTCUSDT 数据。
- Binance 24h 单币数据获取失败 ETHUSDT: HTTP Error 451: 
- Binance 24h 未返回 ETHUSDT 数据。
- Binance BTCUSDT 1h K线获取失败: HTTP Error 451: 
- Binance ETHUSDT 1h K线获取失败: HTTP Error 451: 
- Binance 非DeFi期现数据获取失败 BTC: HTTP Error 451: 
- Binance 非DeFi期现数据获取失败 ETH: HTTP Error 451: 
- 借币成本部分数据源不可用: Bybit: HTTP Error 403: Forbidden | Backpack: Remote end closed connection without response
- Morpho API 获取失败: HTTP Error 400: Bad Request
- Bitcompare CeFi 稳定币样本为空：未匹配到稳定币资产。
- RWA.xyz Real Estate 快照获取失败: <urlopen error _ssl.c:1112: The handshake operation timed out>
- OKX 聪明钱数据获取失败（traders）: Update available for @okx_ai/okx-trade-cli: 1.3.2 → 1.3.9
Run: npm install -g @okx_ai/okx-trade-cli

Error: Session expired — run `okx-auth login` again
Error: No credentials found.
Hint: Run `okx auth login` to authenticate, or configure API key credentials.
Version: @okx_ai/okx-trade-cli@1.3.2
- OKX 聪明钱数据获取失败（news:coin-sentiment）: Update available for @okx_ai/okx-trade-cli: 1.3.2 → 1.3.9
Run: npm install -g @okx_ai/okx-trade-cli

Error: Session expired — run `okx-auth login` again
Error: No credentials found.
Hint: Run `okx auth login` to authenticate, or configure API key credentials.
Version: @okx_ai/okx-trade-cli@1.3.2
- OKX 新闻情绪快照为空：coin-sentiment 未返回有效样本。

