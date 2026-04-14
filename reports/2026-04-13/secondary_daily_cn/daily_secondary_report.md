# 二级市场日报（2026-04-13）

## 关键结论
- 全市场市值 $2.41T（24h -2.75%），成交额 $75.89B（24h +4.79%）。
- BTC 主导率 58.80%（-0.25pct），Top10 外占比 7.85%。
- Top10 资产上涨 1 / 下跌 8，平均涨跌幅 -0.26%，首尾分化 1.13pct。
- 衍生品：BTC/ETH 资金费率分别为 -0.00bps / -0.02bps，DVOL 收盘 45.71 / 66.05。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Stress Repricing`。价格回撤但换手抬升，说明市场在高分歧下重估风险，波动脉冲概率偏高。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交回暖，短线流动性环境较前一日改善；从杠杆维度看，杠杆拥挤度整体可控；在风险定价层面，期权端对尾部波动的定价仍偏谨慎；再结合情绪仍在恐惧区，反弹更容易受到外部事件扰动。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](charts/chart_btc_eth_24h_trend.png)

- BTC：$70,888.28（24h -0.71%，区间 $70,505.88 - $71,500.00，当前位于区间 38%）=> 区间震荡。
- ETH：$2,185.58（24h -0.75%，区间 $2,175.00 - $2,218.13，当前位于区间 25%）=> 区间震荡。
- 简评：BTC 与 ETH 出现分化，短线以结构性机会为主。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +1.79%。
其中包含奖励补贴的池有 0 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 0.00% 至 2.96% 区间。
- 资金集中：TVL 主要集中在 Aave-USDT（Ethereum，TVL $1.20B）、Spark-USDT（Ethereum，TVL $871.65M）。
- 收益领先：当前收益靠前样本包括 Spark-USDT（Ethereum，Total 2.96%）、Aave-USDC（Base，Total 2.67%）。

风险提示
- 利用率达到 70% 以上的池有 4 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-DAI（Ethereum） 80.01%，Borrow APY 4.44%。
- 奖励收益池数量：0 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(8)，Compound API(7)，DefiLlama(21)，Morpho API(2)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | USDT | 2.23% | 3.32% | N/A | 2.18% | 75.01% | $1.20B | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 2.96% | N/A | N/A | 2.96% | N/A | $871.65M | DefiLlama |
| Compound | Ethereum | USDS | 2.25% | 3.23% | 0.00% | 2.25% | 62.43% | $2.94M | Compound API |
| Morpho | Ethereum | PYUSD | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | $9.72M | Morpho API |
| Aave | Ethereum | USDC | 2.30% | 3.37% | N/A | 2.28% | 76.25% | $786.33M | DefiLlama+Aave API |
| Aave | Ethereum | PYUSD | 1.25% | 3.08% | N/A | 1.25% | 45.67% | $120.19M | DefiLlama+Aave API |
| Aave | Ethereum | USDS | 0.08% | 5.67% | N/A | 0.08% | 1.89% | $51.58M | DefiLlama+Aave API |
| Aave | Ethereum | DAI | 2.64% | 4.44% | N/A | 2.61% | 80.01% | $29.19M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 1.51% | 2.75% | N/A | 1.49% | 61.12% | $104.49M | DefiLlama+Aave API |
| Aave | Base | USDC | 2.70% | 3.92% | N/A | 2.67% | 76.98% | $82.14M | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 24 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 2.30% | 3.37% | N/A | 2.28% | 76.25% | $786.33M | DefiLlama+Aave API |
| USDC | Aave | Arbitrum | 1.51% | 2.75% | N/A | 1.49% | 61.12% | $104.49M | DefiLlama+Aave API |
| USDC | Aave | Base | 2.70% | 3.92% | N/A | 2.67% | 76.98% | $82.14M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.75% | N/A | N/A | 3.75% | N/A | $399.23M | DefiLlama |
| USDC | Compound | Ethereum | 2.54% | 3.46% | 0.11% | 2.65% | 70.45% | $370.26M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.26% | 3.25% | 0.00% | 2.26% | 62.91% | $21.03M | DefiLlama+Compound API |
| USDC | Compound | Base | 2.95% | 3.78% | 0.00% | 2.95% | 82.07% | $10.49M | DefiLlama+Compound API |
| USDC | Morpho | Base | 11.44% | 11.44% | N/A | 11.44% | 100.00% | $1.25M | DefiLlama+Morpho API |
| USDT | Aave | Ethereum | 2.23% | 3.32% | N/A | 2.18% | 75.01% | $1.20B | DefiLlama+Aave API |
| USDT | Spark | Ethereum | 2.96% | N/A | N/A | 2.96% | N/A | $871.65M | DefiLlama |
| USDT | Compound | Ethereum | 2.48% | 3.41% | 0.11% | 2.59% | 68.91% | $208.22M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 1.87% | 2.94% | 0.00% | 1.87% | 51.83% | $20.23M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 2.64% | 4.44% | N/A | 2.61% | 80.01% | $29.19M | DefiLlama+Aave API |
| DAI | Aave | Arbitrum | 1.85% | 3.76% | N/A | 1.84% | 66.37% | $1.58M | DefiLlama+Aave API |
| USDS | Aave | Ethereum | 0.08% | 5.67% | N/A | 0.08% | 1.89% | $51.58M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.55% | N/A | N/A | 2.55% | N/A | $30.79M | DefiLlama |
| USDS | Compound | Ethereum | 2.25% | 3.23% | 0.00% | 2.25% | 62.43% | $2.94M | Compound API |
| USDS | Compound | Base | 2.06% | 3.41% | 0.00% | 2.06% | 38.13% | $1.12M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.44M | DefiLlama |
| SUSDS | Morpho | Ethereum | N/A | N/A | N/A | 0.00% | N/A | $202.31M | DefiLlama |
| SUSDS | Morpho | Arbitrum | N/A | N/A | N/A | 0.00% | N/A | $6.91M | DefiLlama |
| PYUSD | Aave | Ethereum | 1.25% | 3.08% | N/A | 1.25% | 45.67% | $120.19M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.48% | N/A | N/A | 0.48% | N/A | $86.56M | DefiLlama |
| PYUSD | Morpho | Ethereum | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | $9.72M | Morpho API |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 24 条；DefiLlama 扩展样本 71 条（展示 Top20）；Bitcompare 稳定币利率样本 5 条。
- 覆盖维度：扩展样本覆盖 49 个协议、15 条链、47 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | N/A | N/A | 3.75% | $6.36B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 3.59% | N/A | 3.59% | $3.44B | DefiLlama API |
| USDC | maple | Ethereum | 4.18% | 0.00% | 4.18% | $3.43B | DefiLlama API |
| USYC | circle-usyc | BSC | 2.92% | N/A | 2.92% | $2.55B | DefiLlama API |
| USDT | maple | Ethereum | 3.64% | 0.00% | 3.64% | $1.97B | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.54% | N/A | 3.54% | $1.07B | DefiLlama API |
| USDYC | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $807.55M | DefiLlama API |
| USTB | superstate-ustb | Ethereum | 3.20% | N/A | 3.20% | $642.00M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.20% | N/A | 3.20% | $559.02M | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $552.14M | DefiLlama API |
| BUIDL | blackrock-buidl | Solana | 3.51% | N/A | 3.51% | $525.80M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 2.72% | 2.72% | $513.91M | DefiLlama API |
| BUIDL | blackrock-buidl | BSC | 3.20% | N/A | 3.20% | $507.78M | DefiLlama API |
| USDC | jupiter-lend | Solana | 2.56% | 1.07% | 3.63% | $443.53M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | N/A | N/A | 3.75% | $357.63M | DefiLlama API |
| USDD | justlend | Tron | 0.00% | 4.51% | 4.51% | $354.85M | DefiLlama API |
| SUSDAI | usd-ai | Arbitrum | 6.94% | N/A | 6.94% | $248.60M | DefiLlama API |
| DAI | sky-lending | Ethereum | N/A | N/A | 1.25% | $244.77M | DefiLlama API |
| USDX | stables-labs-usdx | BSC | 1.35% | N/A | 1.35% | $241.97M | DefiLlama API |
| WSRUSD | reservoir-protocol | Ethereum | N/A | N/A | 4.75% | $203.49M | DefiLlama API |

CeFi 稳定币收益/成本对比（Bitcompare vs taoli）
| 币种 | Bitcompare 最高APY | 对应平台 | taoli(Binance借币年化) | 利差(APY-借币) |
|---|---:|---|---:|---:|
| DAI | 7.00% | EarnPark | N/A | N/A |
| TUSD | 1.45% | JustLend | N/A | N/A |
| USDC | 4.00% | EarnPark | 2.62% | 1.38% |
| USDP | 11.50% | Nexo | N/A | N/A |
| USDT | 20.00% | EarnPark | 3.00% | 17.00% |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## 非 DeFi（交易所期现）
![非DeFi期现快照](charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：OKX-ETH，年化约 10.35%。
- Funding 最低样本：Binance-BTC，年化约 -5.28%。
- Basis 偏离最大：Binance-BTC，相对指数约 -0.06%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.00% · 100k | 0.01%/2.51% · 5.0M | 0.01%/3.00% · 8.0M | 0.01%/2.59% · 50.0M | N/A | OKX 0.01% |
| USDC | 0.01%/2.62% · 100k | 0.01%/2.51% · 1.0M | 0.01%/2.55% · 3.5M | 0.00%/1.57% · 300.0M | N/A | Backpack 0.00% |
| USDE | N/A | N/A | 0.01%/5.00% · 1.0M | N/A | N/A | Bybit 0.01% |
| BTC | 0.00%/0.40% · 60 | 0.00%/1.01% · 175 | 0.00%/0.40% · 300 | 0.00%/0.17% · 3k | N/A | Backpack 0.00% |
| ETH | 0.01%/2.58% · 400 | 0.01%/2.01% · 7k | 0.01%/2.58% · 2k | 0.00%/1.81% · 20k | N/A | Backpack 0.00% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)

截至 2026-04-13，全市场市值 $2.41T，24h 成交额 $75.89B，BTC 主导率 58.80%。
价格下行但换手放大，反映分歧加剧，通常伴随更高的日内波动。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](charts/chart_market_daily_change.png)

相对前日，市值 -2.75%、成交 +4.79%、BTC.D -0.25pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 58.80% / Top2-10 33.35% / Top10 外 7.85%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)

Top10 中领涨 BNB（+0.42%），尾部 ETH（-0.70%），均值 -0.26%。分化 1.13pct，结构性交易仍是主导。
下跌家数占优，风险偏好修复仍较脆弱，短线追高性价比一般。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](charts/chart_exchange_24h_change.png)

前排样本上涨 6 家、下跌 4 家，均值 +0.62%。Coinbase Exchange 最强（+27.23%），HTX 最弱（-23.25%）。
最强与最弱平台的 24h 变化差达到 50.48pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 85.67%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品占比处于高位，行情更容易出现脉冲式放大，风控阈值建议偏保守。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 -0.00bps / -0.02bps；未平仓合约（OI）为 $943.44M / $342.97M；隐含波动率指数（DVOL）位于 Neutral（中性波动定价） / Panic（高波动溢价）。
Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 12（较前日 -4）；配合 BTC/ETH DVOL 45.71/66.05，当前更像情绪修复中的高波动区。
情绪维持在恐惧区，反弹通常更依赖事件驱动，持续性需要成交确认。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

## 未来24小时观察
1. 若 Top10 外占比继续抬升且 BTC.D 回落，说明风险偏好开始从核心资产向外扩散。
2. 若衍生品占比继续上升而 funding 仍中性，盘面大概率维持高波动震荡而非顺滑上行。
3. 若 F&G 反弹但 DVOL 不降，代表情绪与风险定价背离，追涨胜率会明显下降。

## 交易与风控含义
- 仓位管理优先级高于方向押注，建议保持核心仓位稳定、战术仓位滚动。
- 若交易所衍生品占比继续上升，建议同步收紧杠杆和止损参数。
- 关注情绪改善与广度扩散是否同步发生，二者背离时避免追逐单边。

