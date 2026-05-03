# 二级市场日报（2026-04-24）

## 关键结论
- 全市场市值 $2.61T（24h -0.10%），成交额 $145.44B（24h -5.04%）。
- BTC 主导率 60.09%（+0.12pct），Top10 外占比 7.85%。
- Top10 资产上涨 6 / 下跌 4，平均涨跌幅 +0.47%，首尾分化 2.52pct。
- 衍生品：BTC/ETH 资金费率分别为 +0.15bps / -0.30bps，DVOL 收盘 40.99 / 61.89。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Defensive Drift`。价格与成交同步走弱，属于防守型下移结构，短线以控制回撤为主。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交走弱，流动性恢复仍依赖少数头部平台；从杠杆维度看，杠杆拥挤度整体可控；在风险定价层面，期权端对尾部波动的定价仍偏谨慎；再结合情绪与价格修复节奏尚未完全同步。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](charts/chart_btc_eth_24h_trend.png)

- BTC：$78,233.84（24h +0.66%，区间 $76,960.00 - $78,662.50，当前位于区间 75%）=> 区间震荡。
- ETH：$2,328.44（24h -0.02%，区间 $2,285.42 - $2,343.58，当前位于区间 74%）=> 区间震荡。
- 简评：BTC 与 ETH 出现分化，短线以结构性机会为主。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +6.80%。
其中包含奖励补贴的池有 0 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 2.13% 至 12.60% 区间。
- 资金集中：TVL 主要集中在 Spark-USDT（Ethereum，TVL $991.16M）、Aave-USDC（Ethereum，TVL $65.86M）。
- 收益领先：当前收益靠前样本包括 Aave-USDT（Ethereum，Total 12.60%）、Aave-DAI（Ethereum，Total 9.71%）。

风险提示
- 利用率达到 70% 以上的池有 8 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-USDT（Ethereum） 100.00%，Borrow APY 15.03%。
- 奖励收益池数量：0 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(5)，Compound API(6)，DefiLlama(15)，Morpho API(1)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | USDC | 8.21% | 9.55% | N/A | 8.25% | 96.09% | $65.86M | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 3.00% | N/A | N/A | 3.00% | N/A | $991.16M | DefiLlama |
| Compound | Ethereum | USDS | 7.51% | 8.81% | 0.00% | 7.51% | 91.34% | $1.99M | Compound API |
| Morpho | Ethereum | USDC | 7.17% | 8.25% | 0.00% | 7.17% | 87.41% | $164,378 | Morpho API |
| Aave | Ethereum | USDS | 2.15% | 6.07% | N/A | 2.13% | 48.15% | $17.30M | DefiLlama+Aave API |
| Aave | Ethereum | DAI | 7.44% | 10.82% | N/A | 9.71% | 93.21% | $6.96M | DefiLlama+Aave API |
| Aave | Ethereum | PYUSD | 3.88% | 4.98% | N/A | 3.79% | 86.92% | $3.95M | DefiLlama+Aave API |
| Aave | Ethereum | USDT | 13.43% | 15.03% | N/A | 12.60% | 100.00% | $68,862 | DefiLlama+Aave API |
| Aave | Base | USDC | 3.55% | 4.50% | N/A | 3.49% | 88.04% | $20.58M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 11.69% | 13.29% | N/A | 3.29% | 98.48% | $300,167 | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 17 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 8.21% | 9.55% | N/A | 8.25% | 96.09% | $65.86M | DefiLlama+Aave API |
| USDC | Aave | Base | 3.55% | 4.50% | N/A | 3.49% | 88.04% | $20.58M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.65% | N/A | N/A | 3.65% | N/A | $481.64M | DefiLlama |
| USDC | Compound | Ethereum | 2.45% | 3.39% | 0.12% | 2.57% | 68.06% | $390.98M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.43% | 3.38% | 0.00% | 2.43% | 67.52% | $20.22M | DefiLlama+Compound API |
| USDC | Compound | Base | 7.31% | 8.58% | 0.00% | 7.31% | 91.27% | $9.52M | DefiLlama+Compound API |
| USDC | Morpho | Base | 33.87% | 33.87% | N/A | 33.87% | 100.00% | $1.26M | Morpho API |
| USDT | Spark | Ethereum | 3.00% | N/A | N/A | 3.00% | N/A | $991.16M | DefiLlama |
| USDT | Compound | Ethereum | 3.11% | 3.90% | 0.14% | 3.26% | 86.48% | $179.21M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 2.07% | 3.10% | 0.00% | 2.07% | 57.55% | $19.66M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 7.44% | 10.82% | N/A | 9.71% | 93.21% | $6.96M | DefiLlama+Aave API |
| USDS | Aave | Ethereum | 2.15% | 6.07% | N/A | 2.13% | 48.15% | $17.30M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.48% | N/A | N/A | 2.48% | N/A | $69.76M | DefiLlama |
| USDS | Compound | Ethereum | 7.51% | 8.81% | 0.00% | 7.51% | 91.34% | $1.99M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.43M | DefiLlama |
| PYUSD | Aave | Ethereum | 3.88% | 4.98% | N/A | 3.79% | 86.92% | $3.95M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.39% | N/A | N/A | 0.39% | N/A | $88.76M | DefiLlama |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 17 条；DefiLlama 扩展样本 85 条（展示 Top20）；Bitcompare 稳定币利率样本 4 条。
- 覆盖维度：扩展样本覆盖 43 个协议、14 条链、60 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | N/A | N/A | 3.65% | $5.26B | DefiLlama API |
| USYC | circle-usyc | BSC | 3.14% | N/A | 3.14% | $2.79B | DefiLlama API |
| USDC | maple | Ethereum | 4.89% | 0.00% | 4.89% | $2.62B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 5.14% | N/A | 5.14% | $2.23B | DefiLlama API |
| USDT | maple | Ethereum | 5.01% | 0.00% | 5.01% | $1.15B | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.57% | N/A | 3.57% | $1.12B | DefiLlama API |
| USTB | superstate-ustb | Ethereum | 3.43% | N/A | 3.43% | $855.25M | DefiLlama API |
| USDYC | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $808.40M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.23% | N/A | 3.23% | $559.05M | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $531.94M | DefiLlama API |
| BUIDL | blackrock-buidl | BSC | 3.23% | N/A | 3.23% | $508.41M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 3.51% | 3.51% | $504.13M | DefiLlama API |
| STEAKUSDC | morpho-blue | Base | 4.25% | 0.00% | 4.25% | $467.04M | DefiLlama API |
| USDC | jupiter-lend | Solana | 3.44% | 1.16% | 4.59% | $406.22M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | N/A | N/A | 3.65% | $357.73M | DefiLlama API |
| GTUSDCP | morpho-blue | Base | 4.25% | 0.00% | 4.25% | $347.15M | DefiLlama API |
| USDD | justlend | Tron | 0.00% | 4.26% | 4.26% | $308.27M | DefiLlama API |
| SUSDAI | usd-ai | Arbitrum | 7.11% | N/A | 7.11% | $260.68M | DefiLlama API |
| DAI | sky-lending | Ethereum | N/A | N/A | 1.25% | $244.02M | DefiLlama API |
| SENPYUSD | morpho-blue | Ethereum | 2.25% | 0.47% | 2.72% | $231.66M | DefiLlama API |

CeFi 稳定币收益/成本对比（Bitcompare vs taoli）
| 币种 | Bitcompare 最高APY | 对应平台 | taoli(Binance借币年化) | 利差(APY-借币) |
|---|---:|---|---:|---:|
| DAI | 7.00% | EarnPark | N/A | N/A |
| TUSD | 1.46% | JustLend | N/A | N/A |
| USDC | 4.00% | EarnPark | 2.70% | 1.30% |
| USDT | 20.00% | EarnPark | 3.00% | 17.00% |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## 非 DeFi（交易所期现）
![非DeFi期现快照](charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：Binance-BTC，年化约 -1.28%。
- Funding 最低样本：Binance-ETH，年化约 -10.64%。
- Basis 偏离最大：Binance-ETH，相对指数约 -0.06%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.00% · 100k | 0.01%/2.51% · 5.0M | 0.01%/3.00% · 8.0M | 0.01%/4.19% · 50.0M | N/A | OKX 0.01% |
| USDC | 0.01%/2.70% · 100k | 0.01%/2.51% · 1.0M | 0.01%/2.67% · 3.5M | 0.00%/1.62% · 300.0M | N/A | Backpack 0.00% |
| USDE | N/A | N/A | 0.01%/5.00% · 1.0M | N/A | N/A | Bybit 0.01% |
| BTC | 0.00%/0.42% · 60 | 0.00%/1.01% · 175 | 0.00%/0.41% · 300 | 0.00%/0.26% · 3k | N/A | Backpack 0.00% |
| ETH | 0.01%/2.09% · 400 | 0.01%/2.01% · 7k | 0.01%/2.09% · 2k | 0.01%/2.02% · 20k | N/A | OKX 0.01% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)

截至 2026-04-24，全市场市值 $2.61T，24h 成交额 $145.44B，BTC 主导率 60.09%。
价格与成交同步走弱，风险偏好仍在收缩，盘面更偏防守。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](charts/chart_market_daily_change.png)

相对前日，市值 -0.10%、成交 -5.04%、BTC.D +0.12pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 60.09% / Top2-10 32.06% / Top10 外 7.85%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)

Top10 中领涨 DOGE（+2.06%），尾部 FIGR_HELOC（-0.46%），均值 +0.47%。分化 2.52pct，结构性交易仍是主导。
涨跌家数接近均衡，市场处于结构轮动阶段，方向一致性较弱。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](charts/chart_exchange_24h_change.png)

前排样本上涨 1 家、下跌 9 家，均值 -11.83%。MEXC 最强（+1.58%），Upbit 最弱（-30.53%）。
最强与最弱平台的 24h 变化差达到 32.11pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 84.43%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品仍是主导成交形态，价格连续性更多由杠杆侧情绪决定。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 +0.15bps / -0.30bps；未平仓合约（OI）为 $1.01B / $306.44M；隐含波动率指数（DVOL）位于 Complacency（低波动定价） / Panic（高波动溢价）。
Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 39（较前日 -7）；配合 BTC/ETH DVOL 40.99/61.89，当前更像情绪修复中的高波动区。
情绪回到中性区，若后续成交和广度同步改善，趋势性机会会明显增多。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

## 未来24小时观察
1. 若 Top10 外占比继续抬升且 BTC.D 回落，说明风险偏好开始从核心资产向外扩散。
2. 若衍生品占比继续上升而 funding 仍中性，盘面大概率维持高波动震荡而非顺滑上行。
3. 若 F&G 反弹但 DVOL 不降，代表情绪与风险定价背离，追涨胜率会明显下降。

## 交易与风控含义
- 仓位管理优先级高于方向押注，建议保持核心仓位稳定、战术仓位滚动。
- 若交易所衍生品占比继续上升，建议同步收紧杠杆和止损参数。
- 关注情绪改善与广度扩散是否同步发生，二者背离时避免追逐单边。

