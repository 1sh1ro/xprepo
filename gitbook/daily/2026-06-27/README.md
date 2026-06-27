# 二级市场日报（2026-06-27）

## 关键结论
- 全市场市值 $2.07T（24h +0.64%），成交额 $93.70B（24h -0.76%）。
- BTC 主导率 58.00%（-0.07pct），Top10 外占比 8.09%。
- Top10 资产上涨 8 / 下跌 2，平均涨跌幅 +1.42%，首尾分化 5.04pct。
- 衍生品：BTC/ETH 资金费率分别为 +0.38bps / -0.78bps，DVOL 收盘 43.88 / 58.75。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Range Trading`。价格与成交未形成同向趋势，市场仍在区间内进行结构轮动。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交走弱，流动性恢复仍依赖少数头部平台；从杠杆维度看，杠杆拥挤度整体可控；在风险定价层面，隐含波动率回落至相对低位，事件冲击前的保护成本下降；再结合情绪仍在恐惧区，反弹更容易受到外部事件扰动。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](charts/chart_btc_eth_24h_trend.png)

- BTC 最新价格约 $60,195，24h 口径上涨 +1.71%，收盘位置位于日内区间约 79.6% 分位，属于偏强修复。
- ETH 最新价格约 $1,579.72，24h 口径上涨 +2.81%，收盘位置位于日内区间约 92.2% 分位，弹性强于 BTC。
- 这组数据说明反弹主要由核心资产同步修复驱动，但 ETH 的区间位置更靠近上沿；如果后续成交额不能同步放大，短线更适合按区间上沿震荡处理，而不是直接外推成趋势突破。
- 补充口径：原 Binance 24h 与 1h K 线接口返回 HTTP 451，本段改用 CoinGecko `market_chart` 1d hourly 数据补齐。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +2.63%。
其中包含奖励补贴的池有 2 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 1.15% 至 6.97% 区间。
- 资金集中：TVL 主要集中在 Spark-USDT（Ethereum，TVL $854.49M）、Aave-USDT（Ethereum，TVL $79.23M）。
- 收益领先：当前收益靠前样本包括 Aave-USDC（Ethereum，Total 6.97%）、Aave-USDT（Ethereum，Total 6.45%）。

风险提示
- 利用率达到 70% 以上的池有 7 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-USDC（Ethereum） 90.31%，Borrow APY 4.00%。
- 奖励收益池数量：2 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(8)，Compound API(6)，DefiLlama(21)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | DAI | 3.28% | 4.96% | N/A | 3.23% | 89.01% | $12.17M | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 2.50% | N/A | N/A | 2.50% | N/A | $854.49M | DefiLlama |
| Compound | Ethereum | USDS | 3.24% | 4.00% | 0.00% | 3.24% | 89.91% | $1.89M | Compound API |
| Aave | Ethereum | USDS | 1.15% | 5.88% | N/A | 1.15% | 26.75% | $9.11M | DefiLlama+Aave API |
| Aave | Ethereum | PYUSD | 3.37% | 4.68% | N/A | 3.32% | 80.51% | $2.50M | DefiLlama+Aave API |
| Aave | Ethereum | USDT | 2.17% | 3.27% | 4.30% | 6.45% | 74.06% | $79.23M | DefiLlama+Aave API |
| Aave | Ethereum | USDC | 3.24% | 4.00% | 3.78% | 6.97% | 90.31% | $60.63M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 2.32% | 3.42% | N/A | 2.29% | 75.65% | $42.38M | DefiLlama+Aave API |
| Aave | Base | USDC | 3.18% | 4.26% | N/A | 3.13% | 83.41% | $29.14M | DefiLlama+Aave API |
| Aave | Arbitrum | DAI | 1.80% | 3.70% | N/A | 1.79% | 65.46% | $1.29M | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 22 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 3.24% | 4.00% | 3.78% | 6.97% | 90.31% | $60.63M | DefiLlama+Aave API |
| USDC | Aave | Arbitrum | 2.32% | 3.42% | N/A | 2.29% | 75.65% | $42.38M | DefiLlama+Aave API |
| USDC | Aave | Base | 3.18% | 4.26% | N/A | 3.13% | 83.41% | $29.14M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.60% | N/A | N/A | 3.60% | N/A | $316.16M | DefiLlama |
| USDC | Compound | Ethereum | 3.18% | 3.95% | 0.10% | 3.27% | 88.22% | $325.94M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.57% | 3.48% | 0.00% | 2.57% | 71.26% | $15.93M | DefiLlama+Compound API |
| USDC | Compound | Base | 4.83% | 5.79% | 0.00% | 4.83% | 90.50% | $8.43M | DefiLlama+Compound API |
| USDT | Aave | Ethereum | 2.17% | 3.27% | 4.30% | 6.45% | 74.06% | $79.23M | DefiLlama+Aave API |
| USDT | Spark | Ethereum | 2.50% | N/A | N/A | 2.50% | N/A | $854.49M | DefiLlama |
| USDT | Compound | Ethereum | 2.72% | 3.60% | 0.09% | 2.81% | 75.61% | $191.22M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 1.87% | 2.94% | 0.00% | 1.87% | 51.83% | $19.71M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 3.28% | 4.96% | N/A | 3.23% | 89.01% | $12.17M | DefiLlama+Aave API |
| DAI | Aave | Arbitrum | 1.80% | 3.70% | N/A | 1.79% | 65.46% | $1.29M | DefiLlama+Aave API |
| DAI | Spark | Ethereum | 2.34% | N/A | N/A | 2.34% | N/A | $100.06M | DefiLlama |
| USDS | Aave | Ethereum | 1.15% | 5.88% | N/A | 1.15% | 26.75% | $9.11M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.20% | N/A | N/A | 2.20% | N/A | $183.25M | DefiLlama |
| USDS | Spark | Arbitrum | 3.60% | N/A | N/A | 3.60% | N/A | $359.80M | DefiLlama |
| USDS | Spark | Base | 3.60% | N/A | N/A | 3.60% | N/A | $223.13M | DefiLlama |
| USDS | Compound | Ethereum | 3.24% | 4.00% | 0.00% | 3.24% | 89.91% | $1.89M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.28M | DefiLlama |
| PYUSD | Aave | Ethereum | 3.37% | 4.68% | N/A | 3.32% | 80.51% | $2.50M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.27% | N/A | N/A | 0.27% | N/A | $91.99M | DefiLlama |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 22 条；DefiLlama 扩展样本 84 条（展示 Top20）；Bitcompare 稳定币利率样本 7 条。
- 覆盖维度：扩展样本覆盖 46 个协议、14 条链、59 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | 3.60% | N/A | 3.60% | $5.85B | DefiLlama API |
| USDC | maple | Ethereum | 4.99% | 0.00% | 4.99% | $3.07B | DefiLlama API |
| USYC | circle-usyc | BSC | 3.17% | N/A | 3.17% | $3.02B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 3.79% | N/A | 3.79% | $1.70B | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $1.11B | DefiLlama API |
| USDT | maple | Ethereum | 4.00% | 0.00% | 4.00% | $1.05B | DefiLlama API |
| USDS | centrifuge-protocol | Ethereum | 1.87% | N/A | 1.87% | $869.74M | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.54% | N/A | 3.54% | $830.61M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.20% | N/A | 3.20% | $821.84M | DefiLlama API |
| BUIDL | blackrock-buidl | Solana | 3.51% | N/A | 3.51% | $636.05M | DefiLlama API |
| USTB | invesco-ustb | Ethereum | 3.42% | N/A | 3.42% | $609.96M | DefiLlama API |
| USDY | ondo-yield-assets | Stellar | 3.55% | N/A | 3.55% | $529.46M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 1.99% | 1.99% | $510.35M | DefiLlama API |
| GTUSDCP | morpho-blue | Base | 4.42% | 0.00% | 4.42% | $429.83M | DefiLlama API |
| BUIDL | blackrock-buidl | Avalanche | 3.51% | N/A | 3.51% | $402.18M | DefiLlama API |
| USDC | jupiter-lend | Solana | 4.84% | 0.77% | 5.62% | $390.08M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | 3.60% | N/A | 3.60% | $359.80M | DefiLlama API |
| SENPYUSDMAIN | morpho-blue | Ethereum | 1.93% | 3.22% | 5.15% | $318.59M | DefiLlama API |
| SUSDAI | usd-ai | Arbitrum | 6.75% | N/A | 6.75% | $299.27M | DefiLlama API |
| STEAKUSDC | morpho-blue | Base | 4.38% | 0.00% | 4.38% | $279.16M | DefiLlama API |

CeFi 稳定币收益/成本对比（Bitcompare vs taoli）
| 币种 | Bitcompare 最高APY | 对应平台 | taoli(Binance借币年化) | 利差(APY-借币) |
|---|---:|---|---:|---:|
| DAI | 7.00% | EarnPark | N/A | N/A |
| PYUSD | 4.44% | Euler Finance | N/A | N/A |
| TUSD | 1.37% | JustLend | N/A | N/A |
| USDC | 4.00% | EarnPark | 3.78% | 0.22% |
| USDE | 3.95% | Pendle | N/A | N/A |
| USDP | 10.50% | Nexo | N/A | N/A |
| USDT | 10.84% | Bitfinex | 3.30% | 7.54% |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## RWA 结构观察
![RWA资产类别快照](charts/chart_rwa_asset_class_snapshot.png)

RWA.xyz 公开页快照显示，样本资产类别合计约 $24.80B；最大类别为 U.S. Treasuries（$14.59B，7D -2.62%）。7D 上升类别 3 个、下降类别 3 个，说明 RWA 当前更适合当作结构变量，而不是日内方向信号。
其中股票、主动策略和非美债这类交易属性更强的类别合计约 $4.21B，占样本 16.97%。这部分更接近 CEX 新品类、Perps 和跨资产成交额的观察入口。

RWA 资产类别对照表
| 类别 | 规模 | 7D变化 | as of |
|---|---:|---:|---|
| U.S. Treasuries | $14.59B | -2.62% | 2026-06-26 |
| Credit | $5.80B | +8.49% | 2026-06-26 |
| Tokenized Stocks | $1.47B | -12.13% | 2026-06-26 |
| Active Strategies | $1.43B | +2.79% | 2026-06-26 |
| Non-U.S. Government Debt | $1.32B | -5.33% | 2026-06-26 |
| Real Estate | $202.64M | +0.41% | 2026-06-26 |

交易含义：RWA 放在日报里可以，但应定位为二级市场的产品线与风险偏好背景；只有 tokenized stocks、RWA perps、可交易收益资产扩容时，才更直接影响交易所成交结构。
数据源：RWA.xyz 公开资产类别页；正式 API 可在设置 RWA_API_KEY 后替换为更稳定口径。

## 非 DeFi（交易所期现）
![非DeFi期现快照](charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：OKX-BTC，年化约 3.27%。
- Funding 最低样本：OKX-ETH，年化约 -4.47%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.30% · 500k | 0.01%/2.51% · 5.0M | N/A | 0.01%/3.55% · 50.0M | N/A | OKX 0.01% |
| USDC | 0.01%/3.78% · 500k | 0.01%/2.51% · 1.0M | N/A | 0.01%/2.13% · 300.0M | N/A | Backpack 0.01% |
| BTC | 0.00%/0.40% · 100 | 0.00%/0.51% · 175 | N/A | 0.00%/0.47% · 3k | N/A | Binance 0.00% |
| ETH | 0.01%/2.24% · 2k | 0.00%/1.51% · 7k | N/A | 0.00%/0.86% · 20k | N/A | Backpack 0.00% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)

截至 2026-06-27，全市场市值 $2.07T，24h 成交额 $93.70B，BTC 主导率 58.00%。
价格上涨但成交回落，反弹质量偏弱，需警惕高位回吐。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](charts/chart_market_daily_change.png)

相对前日，市值 +0.64%、成交 -0.76%、BTC.D -0.07pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 58.00% / Top2-10 33.91% / Top10 外 8.09%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)

Top10 中领涨 SOL（+4.58%），尾部 FIGR_HELOC（-0.47%），均值 +1.42%。分化 5.04pct，结构性交易仍是主导。
上涨家数明显占优，但首尾分化仍大，表明反弹并非无差别普涨。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](charts/chart_exchange_24h_change.png)

前排样本上涨 0 家、下跌 10 家，均值 -41.52%。Coinbase Exchange 最强（-31.53%），HTX 最弱（-48.89%）。
最强与最弱平台的 24h 变化差达到 17.36pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 85.20%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品占比处于高位，行情更容易出现脉冲式放大，风控阈值建议偏保守。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 +0.38bps / -0.78bps；未平仓合约（OI）为 $869.07M / $280.68M；隐含波动率指数（DVOL）位于 Complacency（低波动定价） / Neutral（中性波动定价）。
Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 15（较前日 +2）；配合 BTC/ETH DVOL 43.88/58.75，当前更像情绪修复中的高波动区。
恐惧区内出现边际改善，说明市场开始试探修复，但尚不足以支持激进风险暴露。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

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
- BTC/ETH 24h 趋势原始 Binance 数据不可用（HTTP 451），已使用 CoinGecko 1d hourly 数据补齐正文和图表。
- Binance 非DeFi期现数据获取失败 BTC: HTTP Error 451: 
- Binance 非DeFi期现数据获取失败 ETH: HTTP Error 451: 
- 借币成本部分数据源不可用: Bybit: HTTP Error 403: Forbidden
- Morpho API 获取失败: HTTP Error 400: Bad Request
- OKX 聪明钱数据获取失败：未安装 okx CLI。
- OKX 聪明钱数据获取失败：未安装 okx CLI。
- OKX 新闻情绪快照为空：coin-sentiment 未返回有效样本。
