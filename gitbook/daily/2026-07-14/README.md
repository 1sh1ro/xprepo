# 二级市场日报（2026-07-14）

## 关键结论
- 全市场市值 $2.15T（24h -1.97%），成交额 $72.53B（24h +57.66%）。
- BTC 主导率 58.18%（-0.23pct），Top10 外占比 7.43%。
- Top10 资产上涨 4 / 下跌 6，平均涨跌幅 -0.13%，首尾分化 3.73pct。
- 衍生品：BTC/ETH 资金费率分别为 +0.05bps / +0.50bps，DVOL 收盘 37.15 / 50.78。

## 今日盘面判断
如果只用一句话概括今天的市场，关键词是 `Stress Repricing`。价格回撤但换手抬升，说明市场在高分歧下重估风险，波动脉冲概率偏高。广度仍偏窄，增量风险偏好尚未形成持续外溢。这意味着短线虽然有可交易的弹性，但要把它理解成新一轮趋势启动，证据还不够。

## 核心驱动因素
从流动性结构看，多数平台成交回暖，短线流动性环境较前一日改善；从杠杆维度看，杠杆拥挤度整体可控；在风险定价层面，隐含波动率回落至相对低位，事件冲击前的保护成本下降；再结合情绪仍在恐惧区，反弹更容易受到外部事件扰动。整体来看，盘面更像是修复中的高波动环境，而不是低波动顺趋势环境。

## BTC/ETH 24h 趋势判断
![BTC/ETH 24h价格路径](charts/chart_btc_eth_24h_trend.png)

- BTC/ETH 24h 趋势数据暂不可用。

## 稳定币收益情况（链上协议）
按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 10 个主流池；原生供给利率均值约 +2.55%。
其中包含奖励补贴的池有 2 个，补贴收益已单列，不与原生利率混合。

核心观察
- 利率结构：Total APY 位于 0.14% 至 6.85% 区间。
- 资金集中：TVL 主要集中在 Spark-USDT（Ethereum，TVL $404.79M）、Aave-USDT（Ethereum，TVL $80.03M）。
- 收益领先：当前收益靠前样本包括 Aave-USDC（Ethereum，Total 6.85%）、Aave-USDT（Ethereum，Total 6.63%）。

风险提示
- 利用率达到 70% 以上的池有 7 个，杠杆需求主要集中在头部池。
- 利用率最高样本：Aave-USDC（Ethereum） 91.12%，Borrow APY 4.04%。
- 奖励收益池数量：2 个。当前收益主体仍以原生利率为主。

数据覆盖：Aave API(8)，Compound API(6)，DefiLlama(21)。

稳定币收益对照表（安全优先）
| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Aave | Ethereum | DAI | 2.84% | 4.60% | N/A | 2.79% | 82.83% | $20.93M | DefiLlama+Aave API |
| Spark | Ethereum | USDT | 2.75% | N/A | N/A | 2.75% | N/A | $404.79M | DefiLlama |
| Compound | Ethereum | USDS | 3.16% | 3.94% | 0.00% | 3.16% | 87.85% | $1.88M | Compound API |
| Aave | Ethereum | USDS | 0.14% | 5.68% | N/A | 0.14% | 3.32% | $11.91M | DefiLlama+Aave API |
| Aave | Ethereum | PYUSD | 2.99% | 4.44% | N/A | 2.95% | 75.35% | $2.78M | DefiLlama+Aave API |
| Aave | Ethereum | USDT | 2.39% | 3.43% | 4.27% | 6.63% | 77.67% | $80.03M | DefiLlama+Aave API |
| Aave | Ethereum | USDC | 3.30% | 4.04% | 3.60% | 6.85% | 91.12% | $64.25M | DefiLlama+Aave API |
| Aave | Arbitrum | USDC | 2.72% | 3.71% | N/A | 2.68% | 81.90% | $29.90M | DefiLlama+Aave API |
| Aave | Base | USDC | 3.19% | 4.26% | N/A | 3.14% | 83.52% | $29.67M | DefiLlama+Aave API |
| Aave | Arbitrum | DAI | 1.99% | 3.90% | N/A | 1.97% | 68.81% | $1.12M | DefiLlama+Aave API |

稳定币收益对比（扩展样本，TVL≥$1M，共 22 条）
| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| USDC | Aave | Ethereum | 3.30% | 4.04% | 3.60% | 6.85% | 91.12% | $64.25M | DefiLlama+Aave API |
| USDC | Aave | Arbitrum | 2.72% | 3.71% | N/A | 2.68% | 81.90% | $29.90M | DefiLlama+Aave API |
| USDC | Aave | Base | 3.19% | 4.26% | N/A | 3.14% | 83.52% | $29.67M | DefiLlama+Aave API |
| USDC | Spark | Ethereum | 3.60% | N/A | N/A | 3.60% | N/A | $306.44M | DefiLlama |
| USDC | Compound | Ethereum | 3.19% | 3.96% | 0.10% | 3.29% | 88.73% | $335.47M | DefiLlama+Compound API |
| USDC | Compound | Arbitrum | 2.66% | 3.55% | 0.00% | 2.66% | 73.75% | $15.77M | DefiLlama+Compound API |
| USDC | Compound | Base | 8.92% | 10.39% | 0.00% | 8.92% | 91.78% | $8.13M | DefiLlama+Compound API |
| USDT | Aave | Ethereum | 2.39% | 3.43% | 4.27% | 6.63% | 77.67% | $80.03M | DefiLlama+Aave API |
| USDT | Spark | Ethereum | 2.75% | N/A | N/A | 2.75% | N/A | $404.79M | DefiLlama |
| USDT | Compound | Ethereum | 2.75% | 3.62% | 0.09% | 2.84% | 76.35% | $192.72M | DefiLlama+Compound API |
| USDT | Compound | Arbitrum | 1.95% | 3.00% | 0.00% | 1.95% | 54.08% | $19.61M | DefiLlama+Compound API |
| DAI | Aave | Ethereum | 2.84% | 4.60% | N/A | 2.79% | 82.83% | $20.93M | DefiLlama+Aave API |
| DAI | Aave | Arbitrum | 1.99% | 3.90% | N/A | 1.97% | 68.81% | $1.12M | DefiLlama+Aave API |
| DAI | Spark | Ethereum | 2.34% | N/A | N/A | 2.34% | N/A | $103.19M | DefiLlama |
| USDS | Aave | Ethereum | 0.14% | 5.68% | N/A | 0.14% | 3.32% | $11.91M | DefiLlama+Aave API |
| USDS | Spark | Ethereum | 2.20% | N/A | N/A | 2.20% | N/A | $217.91M | DefiLlama |
| USDS | Spark | Arbitrum | 3.60% | N/A | N/A | 3.60% | N/A | $360.64M | DefiLlama |
| USDS | Spark | Base | 3.60% | N/A | N/A | 3.60% | N/A | $11.94M | DefiLlama |
| USDS | Compound | Ethereum | 3.16% | 3.94% | 0.00% | 3.16% | 87.85% | $1.88M | Compound API |
| SUSDS | Spark | Ethereum | 0.00% | N/A | N/A | 0.00% | N/A | $3.28M | DefiLlama |
| PYUSD | Aave | Ethereum | 2.99% | 4.44% | N/A | 2.95% | 75.35% | $2.78M | DefiLlama+Aave API |
| PYUSD | Spark | Ethereum | 0.23% | N/A | N/A | 0.23% | N/A | $92.96M | DefiLlama |

跨源补充（比 taoli 更全）
- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare CeFi 利率，并与现有链上主流池快照交叉核对。
- 覆盖规模：原链上精表 22 条；DefiLlama 扩展样本 88 条（展示 Top20）；Bitcompare 稳定币利率样本 0 条。
- 覆盖维度：扩展样本覆盖 45 个协议、14 条链、58 类稳定币。
- 口径说明：Bitcompare 为平台展示 APY，taoli 为 Binance 借币年化，两者用于横向参考，不等价于无风险套利收益。

稳定币收益补充表（DefiLlama 扩展，TVL≥$30M，去重后 Top20）
| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |
|---|---|---|---:|---:|---:|---:|---|
| SUSDS | sky-lending | Ethereum | 3.60% | N/A | 3.60% | $4.73B | DefiLlama API |
| USDC | maple | Ethereum | 4.86% | 0.00% | 4.86% | $3.35B | DefiLlama API |
| USYC | circle-usyc | BSC | 3.26% | N/A | 3.26% | $2.91B | DefiLlama API |
| SUSDE | ethena-usde | Ethereum | 3.96% | N/A | 3.96% | $1.57B | DefiLlama API |
| USDY | ondo-yield-assets | Ethereum | 3.55% | N/A | 3.55% | $1.11B | DefiLlama API |
| USDT | maple | Ethereum | 4.13% | 0.00% | 4.13% | $990.66M | DefiLlama API |
| BUIDL | blackrock-buidl | Avalanche | 3.49% | N/A | 3.49% | $902.96M | DefiLlama API |
| USDS | centrifuge-protocol | Ethereum | 3.46% | N/A | 3.46% | $868.24M | DefiLlama API |
| BUIDL | blackrock-buidl | Ethereum | 3.52% | N/A | 3.52% | $826.96M | DefiLlama API |
| BUIDL | blackrock-buidl | Aptos | 3.18% | N/A | 3.18% | $821.87M | DefiLlama API |
| USTB | invesco-ustb | Ethereum | 3.26% | N/A | 3.26% | $667.41M | DefiLlama API |
| BUIDL | blackrock-buidl | Solana | 3.49% | N/A | 3.49% | $630.72M | DefiLlama API |
| USDY | ondo-yield-assets | Stellar | 3.55% | N/A | 3.55% | $532.32M | DefiLlama API |
| BUSD0 | usual-usd0 | Ethereum | N/A | 2.20% | 2.20% | $507.76M | DefiLlama API |
| USDD | justlend-v1 | Tron | 0.00% | 3.99% | 3.99% | $439.77M | DefiLlama API |
| GTUSDCP | morpho-blue | Base | 4.53% | 0.00% | 4.53% | $424.51M | DefiLlama API |
| USDC | jupiter-lend | Solana | 3.55% | 0.72% | 4.27% | $419.31M | DefiLlama API |
| AUSD | centrifuge-protocol | Ethereum | 3.59% | N/A | 3.59% | $371.77M | DefiLlama API |
| STEAKUSDC | morpho-blue | Base | 4.50% | 0.00% | 4.50% | $369.18M | DefiLlama API |
| SUSDS | sky-lending | Arbitrum | 3.60% | N/A | 3.60% | $360.64M | DefiLlama API |

交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。
部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。

## RWA 结构观察
![RWA资产类别快照](charts/chart_rwa_asset_class_snapshot.png)

RWA.xyz 公开页快照显示，样本资产类别合计约 $27.51B；最大类别为 U.S. Treasuries（$15.52B，7D +4.02%）。7D 上升类别 5 个、下降类别 1 个，说明 RWA 当前更适合当作结构变量，而不是日内方向信号。
其中股票、主动策略和非美债这类交易属性更强的类别合计约 $4.86B，占样本 17.66%。这部分更接近 CEX 新品类、Perps 和跨资产成交额的观察入口。

RWA 资产类别对照表
| 类别 | 规模 | 7D变化 | as of |
|---|---:|---:|---|
| U.S. Treasuries | $15.52B | +4.02% | 2026-07-13 |
| Credit | $6.92B | +2.51% | 2026-07-13 |
| Tokenized Stocks | $1.82B | +19.35% | 2026-07-13 |
| Active Strategies | $1.66B | +12.64% | 2026-07-13 |
| Non-U.S. Government Debt | $1.38B | +2.56% | 2026-07-13 |
| Real Estate | $202.64M | -0.10% | 2026-07-13 |

交易含义：RWA 放在日报里可以，但应定位为二级市场的产品线与风险偏好背景；只有 tokenized stocks、RWA perps、可交易收益资产扩容时，才更直接影响交易所成交结构。
数据源：RWA.xyz 公开资产类别页；正式 API 可在设置 RWA_API_KEY 后替换为更稳定口径。

## 非 DeFi（交易所期现）
![非DeFi期现快照](charts/chart_nondefi_carry_snapshot.png)

样本范围覆盖 Binance 与 OKX 的 BTC/ETH 现货与永续，用于观察 funding 与 basis 的当期结构。
- Funding 最高样本：OKX-BTC，年化约 2.16%。
- Funding 最低样本：OKX-ETH，年化约 -0.95%。

借币成本多源对比表
| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |
|---|---:|---:|---:|---:|---:|---:|
| USDT | 0.01%/3.64% · 500k | 0.01%/2.51% · 5.0M | N/A | 0.01%/3.68% · 50.0M | N/A | OKX 0.01% |
| USDC | 0.01%/4.21% · 500k | 0.01%/2.51% · 1.0M | N/A | 0.01%/2.15% · 300.0M | N/A | Backpack 0.01% |
| BTC | 0.00%/0.39% · 100 | 0.00%/0.51% · 175 | N/A | 0.00%/0.44% · 3k | N/A | Binance 0.00% |
| ETH | 0.01%/2.23% · 2k | 0.00%/1.51% · 7k | N/A | 0.00%/0.76% · 20k | N/A | Backpack 0.00% |
说明：统一按日利率/年化展示，单元格尾部为可借额度。
- 交易含义：当 funding 年化显著高于 basis 且持续为正，carry 交易更偏向收取 funding；若 basis 与 funding 同步回落，需降低杠杆并关注资金回流速度。
该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。

## 市场脉冲
![全市场当日水平](charts/chart_market_snapshot_levels.png)

截至 2026-07-14，全市场市值 $2.15T，24h 成交额 $72.53B，BTC 主导率 58.18%。
价格下行但换手放大，反映分歧加剧，通常伴随更高的日内波动。在这种盘面下，成交能否继续跟上，是判断明天反弹延续还是回吐的第一道分水岭。

![全市场当日变化](charts/chart_market_daily_change.png)

相对前日，市值 -1.97%、成交 +57.66%、BTC.D -0.23pct。
把这组变化拆开看，比看单一涨跌更有用：价格、成交、主导率三者同向时，行情更有连续性；一旦出现背离，走势往往会变得更短促、更反复。

## 主导率与市场广度
![市场广度快照](charts/chart_market_breadth_snapshot.png)

当前结构为 BTC 58.18% / Top2-10 34.38% / Top10 外 7.43%。长尾占比仍偏低，广度修复还未形成持续趋势。
Top10 外占比处于低位，风险偏好仍主要停留在 BTC 与头部资产。换句话说，资金目前更愿意在高流动性的核心资产里做仓位调整，而不是大面积扩散到长尾资产。

## 资产与交易所资金流
![Top10资产24h表现](charts/chart_top10_assets_24h.png)

Top10 中领涨 FIGR_HELOC（+1.91%），尾部 HYPE（-1.83%），均值 -0.13%。分化 3.73pct，结构性交易仍是主导。
涨跌家数接近均衡，市场处于结构轮动阶段，方向一致性较弱。对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。

![前排交易所24h变化](charts/chart_exchange_24h_change.png)

前排样本上涨 9 家、下跌 1 家，均值 +19.74%。Coinbase Exchange 最强（+61.87%），Upbit 最弱（-2.15%）。
最强与最弱平台的 24h 变化差达到 64.02pct，说明流动性仍在选择性回流，头部平台的价格发现能力更强。当平台间流量分化明显时，报价连续性和滑点表现会同步分化，执行层面要更关注成交质量。

![交易所现货衍生品结构](charts/chart_exchange_spot_deriv_structure.png)

样本内衍生品成交占比 88.02%。若该占比继续走高且 funding 不同步回落，短线波动脉冲通常会增强。
衍生品占比处于高位，行情更容易出现脉冲式放大，风控阈值建议偏保守。这也是为什么同样的消息面在当前阶段更容易被放大成大振幅走势。

## 衍生品与情绪
![衍生品快照](charts/chart_derivatives_snapshot.png)

资金费率（Funding）仍在中性附近，BTC/ETH 分别 +0.05bps / +0.50bps；未平仓合约（OI）为 $760.20M / $274.17M；隐含波动率指数（DVOL）位于 Complacency（低波动定价） / Neutral（中性波动定价）。
Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。

![情绪与波动当日快照](charts/chart_sentiment_snapshot.png)

恐惧与贪婪指数（F&G）当日 22（较前日 -6）；配合 BTC/ETH DVOL 37.15/50.78，当前更像情绪修复中的高波动区。
情绪维持在恐惧区，反弹通常更依赖事件驱动，持续性需要成交确认。只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。

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
- 借币成本部分数据源不可用: Bybit: HTTP Error 403: Forbidden
- Morpho API 获取失败: HTTP Error 400: Bad Request
- Bitcompare CeFi 稳定币样本为空：未匹配到稳定币资产。
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

