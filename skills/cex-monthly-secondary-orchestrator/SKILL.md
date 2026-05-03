---
name: cex-monthly-secondary-orchestrator
description: Orchestrate end-to-end CEX monthly secondary-market reporting by combining Binance/Coinbase/KuCoin benchmark framing with figure skills, Deribit monthly metrics skill, and core report scripts. Includes a v2 polish pass for light-theme charts and finalized monthly-report style.
---

# CEX Monthly Secondary Orchestrator

Run one pipeline to build a complete monthly secondary-market report pack.
Use strict month scope only (first day to last day of target month), never annual aggregation.
Public-facing output is the default target. Do not expose internal production scaffolding in正文.

## Quick Start

```bash
python3 /Users/my/.codex/skills/cex-monthly-secondary-orchestrator/scripts/run_cex_monthly_orchestrator.py \
  --month 2026-02 \
  --outdir /Users/my/xp/reports/2026-02/secondary_orchestrated
```

## V2 Polish Pass (Recommended)

After orchestration, apply the current approved house style:

```bash
python3 /Users/my/.codex/skills/cex-monthly-secondary-orchestrator/scripts/apply_v2_polish.py \
  --report-dir /Users/my/xp/reports/2026-02/secondary_orchestrated
```

This pass applies:

1. Light-theme redraw for Deribit funding chart.
2. USD-normalized redraw for Deribit OI chart.
3. Donut redraw for DeFi TVL single-month share chart.
4. 100% stacked-bar redraw for outside-top10 breadth chart.
5. Report markdown cleanup (removes standalone Derivatives Risk block and NFT figure line when present, strips Chinese smart quotes).

## Writing Contract

Before writing, rewriting, or quality-checking the public monthly report, read:

- [monthly-paragraph-contract.md](references/monthly-paragraph-contract.md)

This contract is mandatory. It defines what each paragraph should do, which metric must support it, when to show or hide charts, and how to handle missing data. Do not rely on hardcoded Python prose when a paragraph needs editorial judgment.

## What It Coordinates

1. Binance-style Figure 2 top coin performance skill.
2. Binance-style Figure 3 DeFi TVL share skill.
3. Binance-style Figure 4 NFT volume skill (data retained; display may be removed by polish pass).
4. Binance-style Figure 6 outside-top10 share skill.
5. Deribit monthly metrics skill.
6. Core yuque-style monthly report generator.

## Output

- `orchestrated_secondary_report.md`
- `orchestrator_manifest.csv`
- `charts/*.png`
- `packages/*` (sub-skill raw outputs)
- `orchestrated_secondary_report_coinbase_style_text.md` (if generated in workspace flow)

## Public Writing Standard

- The monthly page should read like an exchange or broker publication, not like an analyst notebook.
- Do not emit sections such as methodology, data availability, references, chart indexes, or execution status in the public page.
- Do not label sections by chart number.
- Prefer 6 to 9 substantive sections total.
- Every section should pair a chart with a short judgment paragraph.
- Stablecoin opportunity content should be included only when it helps explain capital allocation behavior, and must stay compact.
- Use institutional tone: conclusion-first, evidence-backed, no overclaim wording.
- Paragraphs must follow `monthly-paragraph-contract.md`: each paragraph should have one job (`what changed`, `why it matters`, or `what to watch next`).
- Preferred section order:
  1. `Key Takeaways`
  2. `宏观代理与市场状态`
  3. `交易所流量与资金活跃度`
  4. `主流资产表现与市场广度`
  5. `衍生品仓位温度`
  6. `情绪与波动定价`
  7. `下月交易框架（基准情景）`

## References

- See [benchmark-frame.md](references/benchmark-frame.md)
- See [metric-routing.md](references/metric-routing.md)
- See [v2-house-style.md](references/v2-house-style.md)
- See [monthly-paragraph-contract.md](references/monthly-paragraph-contract.md)
