# 二级市场日报（2026-05-03）

## 关键结论
- 全市场市值 $2.61T（24h +0.53%），成交额 $90.28B（24h -31.39%）。
- BTC 主导率 60.42%（+0.04pct），Top10 外占比 7.68%。
- Top10 资产上涨 8 / 下跌 2，平均涨跌幅 +0.40%，首尾分化 2.25pct。
- 衍生品：BTC/ETH 资金费率分别为 +0.02bps / +0.00bps，DVOL 收盘 40.03 / 55.13。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Range Trading`。价格与成交未形成同向趋势，市场仍在区间内进行结构轮动。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交走弱，流动性恢复仍依赖少数头部平台；从杠杆维度看，杠杆拥挤度整体可控；在风险定价层面，隐含波动率回落至相对低位，事件冲击前的保护成本下降；再结合情绪与价格修复节奏尚未完全同步。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](./charts/chart_btc_eth_24h_trend.png)

- BTC：$78,701.49（24h +0.33%，区间 $78,084.08 - $79,199.48，当前位于区间 55%）=> 区间震荡。
- ETH：$2,325.15（24h +0.75%，区间 $2,297.59 - $2,343.60，当前位于区间 60%）=> 区间震荡。
- 简评：BTC 与 ETH 出现分化，短线以结构性机会为主。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +4.59%。
其中包含奖励补贴的池有 0 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 1.00% 至 11.28% 区间。
- 资金集中：TVL 主要集中在 Spark-USDT（Ethereum，TVL $1.49B）、Aave-USDT（Ethereum，TVL $145.52M）。
- 收益领先：当前收益靠前样本包括 Compound-USDS（Ethereum，Total 11.28%）、Morpho-USDC（Ethereum，Total 7.19%）。

风险提示
- 利用率达到 70% 以上的池有 8 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-USDC（Ethereum） 93.64%，Borrow APY 6.23%。
- 奖励收益池数量：0 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(7)，Compound API(6)，DefiLlama(17)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | USDT | 4.11% | 4.95% | N/A | 3.90% | 92.66% | $145.52M | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 2.75% | N/A | N/A | 2.75% | N/A | $1.49B | DefiLlama |
| Compound | Ethereum | USDS | 11.28% | 13.05% | 0.00% | 11.28% | 92.51% | $1.98M | Compound API |
| Morpho | Ethereum | USDC | 7.19% | 8.11% | N/A | 7.19% | 89.05% | $161,675 | Morpho API |
| Aave | Ethereum | USDC | 5.23% | 6.23% | N/A | 5.28% | 93.64% | $117.94M | DefiLlama+Aave API |
| Aave | Ethereum | DAI | 2.66% | 4.46% | N/A | 2.63% | 80.26% | $25.82M | DefiLlama+Aave API |
| Aave | Ethereum | USDS | 1.00% | 5.86% | N/A | 1.00% | 23.41% | $16.59M | DefiLlama+Aave API |
| Aave | Ethereum | PYUSD | 4.08% | 5.10% | N/A | 4.00% | 89.37% | $2.81M | DefiLlama+Aave API |
| Aave | Base | USDC | 3.39% | 4.40% | N/A | 3.33% | 86.08% | $24.63M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 4.23% | 5.19% | N/A | 4.37% | 91.06% | $14.01M | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 18 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 5.23% | 6.23% | N/A | 5.28% | 93.64% | $117.94M | DefiLlama+Aave API |
| USDC | Aave | Arbitrum | 4.23% | 5.19% | N/A | 4.37% | 91.06% | $14.01M | DefiLlama+Aave API |
| USDC | Aave | Base | 3.39% | 4.40% | N/A | 3.33% | 86.08% | $24.63M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.65% | N/A | N/A | 3.65% | N/A | $961.45M | DefiLlama |
| USDC | Compound | Ethereum | 2.77% | 3.64% | 0.13% | 2.91% | 77.06% | $348.41M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.88% | 3.73% | 0.00% | 2.88% | 80.13% | $17.93M | DefiLlama+Compound API |
| USDC | Compound | Base | 3.98% | 4.83% | 0.00% | 3.98% | 90.23% | $9.37M | DefiLlama+Compound API |
| USDT | Aave | Ethereum | 4.11% | 4.95% | N/A | 3.90% | 92.66% | $145.52M | DefiLlama+Aave API |
| USDT | Spark | Ethereum | 2.75% | N/A | N/A | 2.75% | N/A | $1.49B | DefiLlama |
| USDT | Compound | Ethereum | 2.84% | 3.69% | 0.13% | 2.97% | 78.84% | $191.68M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 2.33% | 3.30% | 0.00% | 2.33% | 64.80% | $19.82M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 2.66% | 4.46% | N/A | 2.63% | 80.26% | $25.82M | DefiLlama+Aave API |
| USDS | Aave | Ethereum | 1.00% | 5.86% | N/A | 1.00% | 23.41% | $16.59M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.48% | N/A | N/A | 2.48% | N/A | $50.79M | DefiLlama |
| USDS | Compound | Ethereum | 11.28% | 13.05% | 0.00% | 11.28% | 92.51% | $1.98M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.44M | DefiLlama |
| PYUSD | Aave | Ethereum | 4.08% | 5.10% | N/A | 4.00% | 89.37% | $2.81M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.37% | N/A | N/A | 0.37% | N/A | $89.28M | DefiLlama |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 18 条；DefiLlama 扩展样本 82 条（展示 Top20）；Bitcompare 稳定币利率样本 7 条。
- 覆盖维度：扩展样本覆盖 41 个协议、14 条链、58 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | N/A | N/A | 3.65% | $5.99B | DefiLlama API |
| USDC | maple | Ethereum | 4.75% | 0.00% | 4.75% | $3.02B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 3.21% | N/A | 3.21% | $2.03B | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.57% | N/A | 3.57% | $1.12B | DefiLlama API |
| USDT | maple | Ethereum | 4.54% | 0.00% | 4.54% | $1.05B | DefiLlama API |
| USDYC | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $809.10M | DefiLlama API |
| USTB | superstate-ustb | Ethereum | 3.18% | N/A | 3.18% | $804.62M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.23% | N/A | 3.23% | $559.06M | DefiLlama API |
| BUIDL | blackrock-buidl | BSC | 3.23% | N/A | 3.23% | $508.80M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 3.35% | 3.35% | $507.83M | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $480.30M | DefiLlama API |
| STEAKUSDC | morpho-blue | Base | 4.08% | 0.00% | 4.08% | $468.42M | DefiLlama API |
| USDC | jupiter-lend | Solana | 3.05% | 1.10% | 4.14% | $430.45M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | N/A | N/A | 3.65% | $358.07M | DefiLlama API |
| GTUSDCP | morpho-blue | Base | 4.08% | 0.00% | 4.08% | $354.18M | DefiLlama API |
| USDD | justlend | Tron | 0.00% | 4.00% | 4.00% | $307.28M | DefiLlama API |
| SUSDAI | usd-ai | Arbitrum | 7.26% | N/A | 7.26% | $269.47M | DefiLlama API |
| USDY | ondo-yield-assets | Sei | 3.55% | N/A | 3.55% | $262.48M | DefiLlama API |
| SENPYUSD | morpho-blue | Ethereum | 2.32% | 0.00% | 2.32% | $243.01M | DefiLlama API |
| SENPYUSDMAIN | morpho-blue | Ethereum | 1.36% | 3.91% | 5.27% | $243.01M | DefiLlama API |

CeFi 稳定币收益/成本对比（Bitcompare vs taoli）
| 币种 | Bitcompare 最高APY | 对应平台 | taoli(Binance借币年化) | 利差(APY-借币) |
|---|---:|---|---:|---:|
| DAI | 7.00% | EarnPark | N/A | N/A |
| PYUSD | 5.90% | Euler Finance | N/A | N/A |
| TUSD | 1.38% | JustLend | N/A | N/A |
| USDC | 4.00% | EarnPark | 2.94% | 1.06% |
| USDE | 5.36% | Pendle | N/A | N/A |
| USDP | 10.50% | Nexo | N/A | N/A |
| USDT | 20.00% | EarnPark | 3.00% | 17.00% |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## 非 DeFi（交易所期现）
![非DeFi期现快照](./charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：Binance-ETH，年化约 8.97%。
- Funding 最低样本：Binance-BTC，年化约 1.07%。
- Basis 偏离最大：Binance-BTC，相对指数约 -0.05%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.00% · 100k | 0.01%/2.51% · 5.0M | 0.01%/3.00% · 8.0M | 0.01%/3.08% · 50.0M | N/A | OKX 0.01% |
| USDC | 0.01%/2.94% · 100k | 0.01%/2.51% · 1.0M | 0.01%/2.61% · 3.5M | 0.01%/2.00% · 300.0M | N/A | Backpack 0.01% |
| USDE | N/A | N/A | 0.01%/5.00% · 1.0M | N/A | N/A | Bybit 0.01% |
| BTC | 0.00%/0.41% · 60 | 0.00%/1.01% · 175 | 0.00%/0.41% · 300 | 0.00%/0.58% · 3k | N/A | Bybit 0.00% |
| ETH | 0.01%/2.72% · 400 | 0.01%/2.01% · 7k | 0.01%/2.68% · 2k | 0.00%/1.36% · 20k | N/A | Backpack 0.00% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](./charts/chart_market_snapshot_levels.png)

截至 2026-05-03，全市场市值 $2.61T，24h 成交额 $90.28B，BTC 主导率 60.42%。
价格上涨但成交回落，反弹质量偏弱，需警惕高位回吐。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](./charts/chart_market_daily_change.png)

相对前日，市值 +0.53%、成交 -31.39%、BTC.D +0.04pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](./charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 60.42% / Top2-10 31.90% / Top10 外 7.68%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](./charts/chart_top10_assets_24h.png)

Top10 中领涨 TRX（+1.84%），尾部 DOGE（-0.41%），均值 +0.40%。分化 2.25pct，结构性交易仍是主导。
上涨家数明显占优，但首尾分化仍大，表明反弹并非无差别普涨。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](./charts/chart_exchange_24h_change.png)

前排样本上涨 4 家、下跌 6 家，均值 -6.52%。KuCoin 最强（+13.06%），Coinbase Exchange 最弱（-37.50%）。
最强与最弱平台的 24h 变化差达到 50.55pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](./charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 85.65%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品占比处于高位，行情更容易出现脉冲式放大，风控阈值建议偏保守。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](./charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 +0.02bps / +0.00bps；未平仓合约（OI）为 $938.64M / $311.90M；隐含波动率指数（DVOL）位于 Complacency（低波动定价） / Neutral（中性波动定价）。
Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](./charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 47（较前日 +8）；配合 BTC/ETH DVOL 40.03/55.13，当前更像情绪修复中的高波动区。
情绪回到中性区，若后续成交和广度同步改善，趋势性机会会明显增多。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

## OKX 聪明钱仓位结构（Top10交易员）
当日抓取到 OKX 聪明钱榜单 Top10（30d 按 PnL 排序）。
| # | 昵称 | Author ID | 30d PnL | 收益率 | 胜率 | 最大回撤 | 资产 |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | tal***@proton.me | 872836768625012736 | $8.52M | +47.74% | 59.93% | -27.31% | $19.70M |
| 2 | 查理斯，你给我跪下，哼 | 872838143249428480 | $1.89M | +13.63% | 48.62% | -57.22% | $15.73M |
| 3 | 墙头草 | 872876787821654016 | $1.02M | +105.73% | 63.08% | -21.93% | $1.99M |
| 4 | crypto游鱼 | 872860490396205057 | $991,493 | +3.25% | 33.33% | -2.35% | $4.51M |
| 5 | kimi大林 | 872865277548376064 | $977,251 | +1988.35% | 61.63% | -98.93% | $978,271 |
| 6 | 玄弘 | 872896553906995200 | $922,568 | +54.43% | 60.42% | -93.26% | $2.13M |
| 7 | DamiStone | 872835122113150976 | $650,655 | +176.50% | 67.06% | -99.60% | $982,616 |
| 8 | GG16888888 | 872838344060121088 | $613,672 | +48.82% | 78.77% | -68.48% | $1.78M |
| 9 | BTC 星辰 | 872851947123322884 | $523,650 | +52.05% | 97.33% | -23.15% | $1.53M |
| 10 | B譕 | 872832688838094848 | $502,429 | +89.54% | 83.79% | -54.43% | $713,797 |

基于可用交易员详情成功解析 10 位交易员仓位，按净名义仓位（USDT）排序：
| 合约 | 多头名义 | 空头名义 | 净敞口 | 多头人数 | 空头人数 |
|---|---:|---:|---:|---:|---:|
| ETH-USDT-SWAP | $32.04M | $0 | $32.04M | 4 | 0 |
| BTC-USDT-SWAP | $27.82M | $0 | $27.82M | 5 | 0 |
| BTC-USD-260626 | $22.50M | $0 | $22.50M | 1 | 0 |
| BTC-USD-SWAP | $10.61M | $0 | $10.61M | 4 | 0 |
| XRP-USDT-SWAP | $3.34M | $0 | $3.34M | 2 | 0 |
| BTC-USD-260925 | $2.61M | $0 | $2.61M | 1 | 0 |
| SOL-USDT-SWAP | $2.53M | $0 | $2.53M | 2 | 0 |
| ETH-USD-SWAP | $1.30M | $0 | $1.30M | 1 | 0 |

动向：仓位主要集中在 ETH-USDT-SWAP（净敞口 $32.04M) 与 BTC-USDT-SWAP（净敞口 $27.82M)。
含义：若净多持续集中于 BTC/ETH 主合约，通常代表风险偏好偏向核心资产，而非全面扩散。
观察点：重点跟踪净敞口是否由单边转向对冲，以及空头人数是否开始抬升。

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

