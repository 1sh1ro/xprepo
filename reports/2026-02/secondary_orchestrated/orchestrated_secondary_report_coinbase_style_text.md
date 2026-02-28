#  2026-02 月度报告

- 报告区间：2026-02-01 至 2026-02-28


## 观点
- **市场状态（Regime）**：2 月是典型的全市场去风险阶段，不是单一资产轮动。总市值 **-14.61%**（$2.66T -> $2.27T）。
- **市场广度（Breadth）**：Top 资产全线下跌（最抗跌 TRX **-4.27%**，最弱 ETH **-36.81%**），Top10 外占比仅 **21.36%**，风险偏好传导不足。
- **流动性（Flows）**：样本交易所 30d 成交额合计 **$3.90T**，较前观察窗口估算 **-7.11%**，但内部离散很大（KuCoin +118.51%，MEXC -24.36%）。
- **衍生品与情绪（Derivatives & Sentiment）**：Deribit 8h 资金费率小幅负值（BTC/ETH 均约 **-0.000042**），DVOL 与 RV 仍偏高，F&G 月末 **11（Extreme Fear）**。


## 三个核心变化
**1) 下跌是系统性压缩，不是板块轮动失败。**  
总市值走势、Top 资产收益和已实现波动率三项指标共振，说明 2 月核心矛盾是全市场风险预算压缩。

**2) 流动性没有消失，而是进一步向头部集中。**  
交易所 30d 成交额变化显示总量仍大，但交易效率更依赖头部场所与核心交易对，长尾深度恢复明显落后。

**3) 杠杆拥挤缓解，但风险溢价仍高。**  
Funding 已接近中性偏空，而 DVOL 与 RV 仍处高位，说明去杠杆已发生，但风险偏好尚未重建。


### Market Structure
2 月的核心特征不是单一利空触发的短暂波动，而是风险预算在全市场范围内的再定价。总市值从 $2.66T 下移到 $2.27T，回撤幅度足以覆盖多数风险资产的短期弹性；BTC.D 回落 1.09pct，但主导率绝对水平仍接近 58% 的高位区间。  
这组信号意味着资金并未进入进攻型扩散，而是先在核心资产之间做防守再平衡。市场驱动从估值扩张切换到现金流与流动性约束，价格对宏观流动性预期更敏感。  
在这个阶段，趋势判断不能只看单日反弹，需要同时看到市值斜率放缓、主导率稳定、以及跨资产相关性下降，才可以确认风险偏好真正重建。

![全市场总市值](charts/core_chart_1_marketcap.png)

![BTC主导率](charts/core_chart_2_btc_dom.png)

### Liquidity & Venue Rotation
交易所成交额变化反映出总量仍在，但效率分层。样本交易所 30d 成交额仍有 $3.90T，但环比估算回落 7.11%，说明市场并未失去交易能力，而是把交易需求重新压缩到少数深度更好的场所与交易对。  
同时，KuCoin 与 MEXC 的变动方向和幅度差异很大，提示流量在平台间的迁移速度明显高于平时。这种环境下，盘口管理比方向判断更重要，尤其在新闻驱动行情里，滑点和冲击成本会放大利润回撤。  

![前排交易所30d变化](charts/core_chart_3_exchange_30d_change.png)

### Breadth & Sector Risk
广度层面目前仍以防守主导，而非风险扩散。Top10 资产全线收负，最抗跌 TRX 也为 -4.27%，说明没有形成可以带动全市场风险偏好的新主线；Top10 外占比 21.36%，还不足以支持长尾资产重新定价叙事。  
DeFi TVL 结构显示链上主题仍以存量博弈为主：总 TVL 维持在 $93.05B，链间份额未出现足以改写主线的快速迁移，增量资金持续净流入信号仍不充分。  
因此，当前更像结构性轮动中的阶段性防守，而不是新上升周期的早期扩散。

![Top资产月度收益](charts/fig2_top10_monthly_performance.png)

![DeFi TVL链份额](charts/fig3_defi_tvl_share.png)

![Top10外市值占比](charts/fig6_altcoin_outside_top10_share.png)

### Sentiment & Volatility
情绪指标显示市场仍处于典型压缩区：F&G 月末 11，且月内区间仅 5-17，说明市场虽然已经历较深调整，但信心修复仍未启动。已实现波动率同时处于高位，代表短期价格发现仍主要靠风险再评估推动，而不是稳定资金曲线推动。  
极端恐惧叠加高波动，往往对应两个并存结果：一方面容易出现技术性反弹，另一方面反弹的持久性通常受限于流动性与广度。  
因此这里的读法不是马上反转，而是战术机会增多、战略确认不足。只有当情绪中枢抬升且 RV 明显降档，反弹才更可能从交易性机会演化为趋势性机会。

![恐惧贪婪指数](charts/core_chart_4_fng.png)

![BTC/ETH已实现波动率](charts/core_chart_5_realized_vol.png)

## March 观察框架（Base/Bull/Bear）
- **Base（基准情景）**：高波动区间市。条件：Funding 接近 0、BTC.D 横盘、Top10 外占比无持续抬升。  
- **Bull（上修条件）**：广度和情绪同时改善。触发：Top10 外占比上行 + F&G 回到中性附近 + DVOL 回落。  
- **Bear（下修条件）**：若市值继续下台阶且 DVOL 再次抬升，同时 Funding 深负，则下行风险重新放大。



### Funding 极值时序复盘
这张 OKX BTC/ETH 永续 funding 复盘图把日内区间与日均值放在同一张图上。2 月上旬仍能看到正 funding 高点（BTC/ETH 均触及 `+1.00 bps`），但到 2 月 23 日同时出现显著负极值（BTC `-0.92 bps`、ETH `-2.22 bps`），说明杠杆方向从偏多付费切换到偏空付费，并且 ETH 的去杠杆压力更深。  
结合前文 funding 指标可见，月末虽然 funding 已经回到接近中性，但恢复过程并不平滑，中段仍有多次快速摆动。这意味着资金并未形成稳定单边预期，而是在高波动环境里短周期换手，策略上更适合轻仓、快调仓的节奏。

![OKX Funding 极值复盘](supplement/charts/fig_s1_okx_funding_extremes.png)
数据来源：OKX `public/funding-rate-history`（`BTC-USDT-SWAP` / `ETH-USDT-SWAP`）  

### DVOL 分阶段叙事
2 月 DVOL 的主线是先急升、后回落、再高位停留。BTC 在三天内从 `46.29` 升至 `82.62`，ETH 从 `64.24` 升至 `95.78`，随后虽明显回落，但月末仍未回到月初低波区间。说明恐慌冲击后，风险溢价并未完全出清，市场仍处于高波动再平衡阶段。
结合同月 Deribit 衍生品快照看，funding 已回到中性偏空区间，显示多头拥挤度下降；但 OI 口径（期权按本位 OI 折算为 USD）仍处高位，说明尾部风险对冲需求并未明显退潮。这也是 DVOL 回落后仍停留在相对高位的核心原因。

![Deribit OI（USD统一口径）](charts/chart_deribit_oi.png)

![Deribit Funding](charts/chart_deribit_funding.png)

![DVOL 分阶段叙事](supplement/charts/fig_s2_dvol_phase_narrative.png)
数据来源：Deribit `public/get_volatility_index_data`、`public/get_book_summary_by_currency`、`public/ticker`  

### F&G 关键时点映射
这张情绪图把指标从区间描述升级为事件点映射：月内高点 `17`（2026-02-03）与低点 `5`（2026-02-12）都仍落在 Extreme Fear，期间最大单日上行 `+7`（2026-02-09）、最大单日下行 `-6`（2026-02-12）。  
这代表情绪修复是脉冲式而非趋势式，短反弹出现后很快会被新的风险定价打断。与前文情绪章节一致，2 月的情绪结构更接近出清后反复测试底部，而不是恐慌结束后的稳定回升。

![F&G 关键时点映射](supplement/charts/fig_s3_fng_keypoints.png)
数据来源：Alternative.me `fng`  

### Google Trends 三阶段热度
按 1-10 日、11-20 日、21-28 日分三段看虚拟货币关注度变化。Bitcoin 均值从 `53.9` 降至 `30.0` 再到 `24.6`；Ethereum 从 `5.9` 逐段降至 `2.8`；Memecoin 全月接近 `0`。  
这说明月初冲击过后，外部关注度持续衰减，且没有出现新的零售叙事接棒。对应到盘面，就是成交仍在但增量注意力不足，支持前文对广度偏弱、主题扩散不足的判断。

![Google Trends 三阶段热度](supplement/charts/fig_s4_google_trends_three_phases.png)
数据来源：Google Trends（pytrends，全球，关键词 `Bitcoin/Ethereum/Memecoin`）  

### 稳定币周度趋势
稳定币周度份额图显示 USDT 全月维持主导，并从 `91.47%`（2026-01-26 起始周）抬升到 `92.22%`（2026-02-23 当周），同期 USDC 从 `8.53%` 降至 `7.78%`。  
在风险偏好偏弱阶段，这种份额变化通常意味着交易资金更集中到流动性更深、摩擦更低的主稳定币通道。它与前文流动性分层结论一致，体现的是同一逻辑在币种结算层面的映射。

![稳定币周度趋势](supplement/charts/fig_s5_stablecoin_weekly_trend.png)
数据来源：CoinGecko `coins/{id}/market_chart`（`total_volumes`，USDT/USDC）  
