#!/usr/bin/env python3
"""
Generate an exchange secondary-market report in a style inspired by:
- Coinbase positioning notes
- OKX PoR style risk transparency section
- KuCoin daily bulletin sectioning

Data source:
- CoinMarketCap public data-api
- Alternative.me Fear & Greed index
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


CMC_EX_QUOTE = "https://api.coinmarketcap.com/data-api/v3/exchange/quotes/latest"
CMC_GLOBAL_HIST = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"
ALT_FNG = "https://api.alternative.me/fng/"

EXCHANGE_SLUGS = [
    "binance",
    "coinbase-exchange",
    "upbit",
    "okx",
    "bybit",
    "bitget",
    "gate",
    "kucoin",
    "mexc",
    "htx",
]


@dataclass
class ExchangeRow:
    rank: Optional[int]
    name: str
    slug: str
    last_updated: Optional[str]
    volume30d: Optional[float]
    prev30d_est: Optional[float]
    pct30d: Optional[float]
    volume7d: Optional[float]
    pct7d: Optional[float]
    volume24h: Optional[float]
    pct24h: Optional[float]
    spot24h: Optional[float]
    deriv24h: Optional[float]


@dataclass
class GlobalPoint:
    d: date
    total_market_cap: Optional[float]
    total_volume_24h: Optional[float]
    btc_dom: Optional[float]


@dataclass
class FnGPoint:
    value: Optional[int]
    classification: Optional[str]
    ts: Optional[int]


def _get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    full = url if not params else f"{url}?{urlencode(params)}"
    req = Request(full, headers={"User-Agent": "our-cex-feb-report/1.0", "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def _to_float(v: Any) -> Optional[float]:
    return float(v) if isinstance(v, (int, float)) else None


def _to_int(v: Any) -> Optional[int]:
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


def fmt_usd(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    if abs(v) >= 1e12:
        return f"${v/1e12:.2f}T"
    if abs(v) >= 1e9:
        return f"${v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:.2f}M"
    return f"${v:,.0f}"


def fmt_pct(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    return f"{v:+.2f}%"


def parse_month(month: str) -> Tuple[date, date]:
    dt = datetime.strptime(month, "%Y-%m")
    start = date(dt.year, dt.month, 1)
    if dt.month == 12:
        end = date(dt.year + 1, 1, 1)
    else:
        end = date(dt.year, dt.month + 1, 1)
    return start, end


def fetch_exchanges() -> Tuple[List[ExchangeRow], Optional[str]]:
    payload = _get_json(CMC_EX_QUOTE, {"slug": ",".join(EXCHANGE_SLUGS), "convert": "USD"})
    status = payload.get("status") if isinstance(payload.get("status"), dict) else {}
    source_ts = status.get("timestamp") if isinstance(status.get("timestamp"), str) else None

    rows: List[ExchangeRow] = []
    data = payload.get("data") if isinstance(payload.get("data"), list) else []
    for item in data:
        if not isinstance(item, dict):
            continue
        q = item.get("quote")
        q0 = q[0] if isinstance(q, list) and q and isinstance(q[0], dict) else {}
        vol30 = _to_float(q0.get("volume30d"))
        pct30 = _to_float(q0.get("percentChangeVolume30d"))
        prev = None
        if vol30 is not None and pct30 is not None and pct30 > -99.9:
            prev = vol30 / (1.0 + pct30 / 100.0)
        rows.append(
            ExchangeRow(
                rank=_to_int(item.get("rank")),
                name=str(item.get("name") or ""),
                slug=str(item.get("slug") or ""),
                last_updated=q0.get("lastUpdated") if isinstance(q0.get("lastUpdated"), str) else None,
                volume30d=vol30,
                prev30d_est=prev,
                pct30d=pct30,
                volume7d=_to_float(q0.get("volume7d")),
                pct7d=_to_float(q0.get("percentChangeVolume7d")),
                volume24h=_to_float(q0.get("volume24h")),
                pct24h=_to_float(q0.get("percentChangeVolume24h")),
                spot24h=_to_float(q0.get("spotVolumeUsd")),
                deriv24h=_to_float(q0.get("derivativeVolumeUsd")),
            )
        )
    rows.sort(key=lambda r: (r.rank is None, r.rank if r.rank is not None else 10_000, r.name))
    return rows, source_ts


def fetch_global(start: date, end_exclusive: date) -> List[GlobalPoint]:
    params = {
        "interval": "1d",
        "convertId": "2781",
        "timeStart": f"{start.isoformat()}T00:00:00.000Z",
        "timeEnd": f"{(end_exclusive).isoformat()}T00:00:00.000Z",
    }
    payload = _get_json(CMC_GLOBAL_HIST, params)
    quotes = ((payload.get("data") or {}).get("quotes") or []) if isinstance(payload, dict) else []
    out: List[GlobalPoint] = []
    for q in quotes:
        if not isinstance(q, dict):
            continue
        ts = q.get("timestamp")
        if not isinstance(ts, str):
            continue
        try:
            d = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
        except Exception:
            continue
        qq = q.get("quote")
        qq0 = qq[0] if isinstance(qq, list) and qq and isinstance(qq[0], dict) else {}
        out.append(
            GlobalPoint(
                d=d,
                total_market_cap=_to_float(qq0.get("totalMarketCap")),
                total_volume_24h=_to_float(qq0.get("totalVolume24H")),
                btc_dom=_to_float(q.get("btcDominance")),
            )
        )
    out.sort(key=lambda x: x.d)
    return out


def fetch_fng() -> FnGPoint:
    payload = _get_json(ALT_FNG, {"limit": "1"})
    data = payload.get("data") if isinstance(payload.get("data"), list) else []
    if not data:
        return FnGPoint(None, None, None)
    d0 = data[0] if isinstance(data[0], dict) else {}
    value = None
    if isinstance(d0.get("value"), str) and d0.get("value").isdigit():
        value = int(d0.get("value"))
    ts = None
    if isinstance(d0.get("timestamp"), str) and d0.get("timestamp").isdigit():
        ts = int(d0.get("timestamp"))
    return FnGPoint(
        value=value,
        classification=d0.get("value_classification") if isinstance(d0.get("value_classification"), str) else None,
        ts=ts,
    )


def write_csv(rows: List[ExchangeRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank",
                "name",
                "slug",
                "volume30d_usd",
                "prev30d_est_usd",
                "pct30d",
                "volume7d_usd",
                "pct7d",
                "volume24h_usd",
                "pct24h",
                "spot24h_usd",
                "deriv24h_usd",
                "spot_share_24h_pct",
            ]
        )
        for r in rows:
            total_24h = (r.spot24h or 0.0) + (r.deriv24h or 0.0)
            share = (r.spot24h or 0.0) / total_24h * 100 if total_24h > 0 else None
            w.writerow(
                [
                    r.rank,
                    r.name,
                    r.slug,
                    r.volume30d,
                    r.prev30d_est,
                    r.pct30d,
                    r.volume7d,
                    r.pct7d,
                    r.volume24h,
                    r.pct24h,
                    r.spot24h,
                    r.deriv24h,
                    share,
                ]
            )


def plot_dashboard(rows: List[ExchangeRow], global_points: List[GlobalPoint], out_path: Path, month_label: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(14, 13))

    # 1) Market cap + BTC dominance
    ax = axes[0]
    dates = [p.d for p in global_points if p.total_market_cap is not None]
    mcs = [(p.total_market_cap or 0.0) / 1e12 for p in global_points if p.total_market_cap is not None]
    dom_dates = [p.d for p in global_points if p.btc_dom is not None]
    doms = [p.btc_dom or 0.0 for p in global_points if p.btc_dom is not None]

    if dates and mcs:
        ax.plot(dates, mcs, color="#1f77b4", linewidth=2, label="Total Market Cap (T USD)")
        ax.set_ylabel("T USD")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax2 = ax.twinx()
        if dom_dates and doms:
            ax2.plot(dom_dates, doms, color="#ff7f0e", linewidth=1.8, label="BTC Dominance (%)")
            ax2.set_ylabel("%")
        ax.set_title(f"Global Positioning ({month_label})")

    # 2) Exchange 30d change
    ax = axes[1]
    names = [r.name for r in rows]
    pct = [r.pct30d or 0.0 for r in rows]
    colors = ["#2ca02c" if p >= 0 else "#d62728" for p in pct]
    ax.bar(names, pct, color=colors)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylabel("%")
    ax.set_title("Exchange 30d Volume Change")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.tick_params(axis="x", rotation=30)

    # 3) Spot vs derivatives
    ax = axes[2]
    spot = [(r.spot24h or 0.0) / 1e9 for r in rows]
    deriv = [(r.deriv24h or 0.0) / 1e9 for r in rows]
    ax.bar(names, spot, color="#4e79a7", label="Spot 24h (B USD)")
    ax.bar(names, deriv, bottom=spot, color="#f28e2b", label="Derivatives 24h (B USD)")
    ax.set_ylabel("B USD")
    ax.set_title("24h Spot vs Derivatives Mix")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.tick_params(axis="x", rotation=30)
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def write_report(
    rows: List[ExchangeRow],
    global_points: List[GlobalPoint],
    fng: FnGPoint,
    out_path: Path,
    chart_path: Path,
    csv_path: Path,
    month_label: str,
    source_ts: Optional[str],
) -> None:
    total_curr = sum((r.volume30d or 0.0) for r in rows)
    prev_rows = [r.prev30d_est for r in rows if r.prev30d_est is not None]
    total_prev = sum(prev_rows) if prev_rows else None
    total_delta = ((total_curr / total_prev - 1.0) * 100.0) if total_prev and total_prev > 0 else None

    rises = sorted([r for r in rows if r.pct30d is not None], key=lambda x: x.pct30d or -1e9, reverse=True)
    falls = sorted([r for r in rows if r.pct30d is not None], key=lambda x: x.pct30d or 1e9)

    gp_mc = [p for p in global_points if p.total_market_cap is not None]
    gp_vol = [p for p in global_points if p.total_volume_24h is not None]
    gp_dom = [p for p in global_points if p.btc_dom is not None]
    mc_start = gp_mc[0].total_market_cap if gp_mc else None
    mc_end = gp_mc[-1].total_market_cap if gp_mc else None
    mc_delta = ((mc_end / mc_start - 1.0) * 100.0) if mc_start and mc_end else None
    avg_vol = (sum((p.total_volume_24h or 0.0) for p in gp_vol) / len(gp_vol)) if gp_vol else None
    dom_start = gp_dom[0].btc_dom if gp_dom else None
    dom_end = gp_dom[-1].btc_dom if gp_dom else None
    dom_delta = (dom_end - dom_start) if dom_start is not None and dom_end is not None else None

    total_spot = sum((r.spot24h or 0.0) for r in rows)
    total_deriv = sum((r.deriv24h or 0.0) for r in rows)
    spot_share = (total_spot / (total_spot + total_deriv) * 100.0) if (total_spot + total_deriv) > 0 else None

    gen_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines: List[str] = []
    lines.append(f"# 我们的二级市场月报（{month_label}）")
    lines.append("")
    lines.append("- 报告定位：参考 Coinbase/OKX/KuCoin 的结构，形成“定位 + 风险透明 + 日度跟踪”三段式。")
    lines.append(f"- 生成时间（UTC）：{gen_time}")
    if source_ts:
        lines.append(f"- 数据快照时间（CMC）：{source_ts}")
    lines.append(f"- 覆盖交易所：{', '.join([r.name for r in rows])}")
    lines.append("")
    lines.append("## A. 参考样式拆解（你提到的三家）")
    lines.append("- Coinbase《Crypto Market Positioning》：以市场结构和仓位信号为主，常见章节是 Technicals、Flows、Market Depth、Volume、Open Interest。")
    lines.append("- OKX《Proof of Reserves》：核心是“可验证透明度”，强调 Merkle Tree + zk-STARK 以及储备覆盖率。")
    lines.append("- KuCoin《Daily Market Report》：偏交易台快报，结构是 Summary、Major Asset Changes、Industry Highlights、今日催化剂与观察位。")
    lines.append("")
    lines.append("## B. Executive Summary（Positioning）")
    lines.append(f"- 前排交易所滚动 30 天总成交额：{fmt_usd(total_curr)}（估算环比 {fmt_pct(total_delta)}）")
    lines.append(f"- 全市场总市值（CMC）：{fmt_usd(mc_start)} -> {fmt_usd(mc_end)}（月内 {fmt_pct(mc_delta)}）")
    lines.append(f"- 全市场 24h 成交额（日均）：{fmt_usd(avg_vol)}")
    lines.append(f"- BTC Dominance：{fmt_pct(dom_start)} -> {fmt_pct(dom_end)}（变动 {fmt_pct(dom_delta)}）")
    if fng.value is not None:
        lines.append(
            f"- 市场情绪（Alternative.me F&G）：{fng.value} / 100（{fng.classification or 'N/A'}）"
        )
    lines.append("")
    lines.append("## C. Exchange Cross-Section（前排交易所横截面）")
    lines.append("| Rank | Exchange | 30d Volume | 30d Change | 7d Change | 24h Spot | 24h Deriv | Spot Share(24h) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        total_24h = (r.spot24h or 0.0) + (r.deriv24h or 0.0)
        share = (r.spot24h or 0.0) / total_24h * 100.0 if total_24h > 0 else None
        lines.append(
            f"| {r.rank if r.rank is not None else 'N/A'} | {r.name} | {fmt_usd(r.volume30d)} | {fmt_pct(r.pct30d)} | {fmt_pct(r.pct7d)} | {fmt_usd(r.spot24h)} | {fmt_usd(r.deriv24h)} | {fmt_pct(share)} |"
        )
    lines.append("")
    lines.append("## D. Risk Transparency（PoR 风格章节）")
    lines.append("- 现阶段我们可稳定拿到的是“交易行为与结构”数据（量、变化率、现货/衍生品拆分）。")
    lines.append("- 这版的风险代理指标：")
    lines.append(f"  - 24h 结构：样本内现货占比 {fmt_pct(spot_share)}，衍生品占比 {fmt_pct(100.0 - spot_share if spot_share is not None else None)}。")
    lines.append(f"  - 30 天分化：增幅前三 {', '.join([f'{r.name} {fmt_pct(r.pct30d)}' for r in rises[:3]])}。")
    lines.append(f"  - 30 天回落前三 {', '.join([f'{r.name} {fmt_pct(r.pct30d)}' for r in falls[:3]])}。")
    lines.append("- 当前缺口（需 PoR 原站补充）：负债口径、钱包地址级储备明细、资产负债比与审计证明。")
    lines.append("")
    lines.append("## E. Daily Bulletin（KuCoin 风格快照）")
    lines.append("- Today’s Outlook：样本 30d 总量延续收缩，但结构性分化明显（少数平台逆势放量）。")
    lines.append("- Major Changes（30d）：")
    for r in rises[:2]:
        lines.append(f"  - {r.name}: {fmt_pct(r.pct30d)}")
    for r in falls[:2]:
        lines.append(f"  - {r.name}: {fmt_pct(r.pct30d)}")
    lines.append("- Watchlist（下一期建议）:")
    lines.append("  - 若 BTC Dominance 继续回落且衍生品占比继续上行，需关注高杠杆波动放大风险。")
    lines.append("  - 若成交额回升集中于少数交易所，关注流动性集中度风险。")
    lines.append("")
    lines.append("## 图表")
    lines.append(f"![our-cex-feb-dashboard]({chart_path.name})")
    lines.append("")
    lines.append("## 数据与来源")
    lines.append(f"- CMC Exchange Quotes: `{CMC_EX_QUOTE}`")
    lines.append(f"- CMC Global Historical: `{CMC_GLOBAL_HIST}`")
    lines.append(f"- Alternative.me F&G: `{ALT_FNG}`")
    lines.append("- 风格参考：")
    lines.append("  - Coinbase Institutional: Crypto Market Positioning (February 2026)")
    lines.append("  - OKX Proof of Reserves")
    lines.append("  - KuCoin Crypto Daily Market Report (Feb 25, 2026)")
    lines.append("")
    lines.append("## 文件")
    lines.append(f"- 数据表：`{csv_path.name}`")
    lines.append(f"- 图表：`{chart_path.name}`")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate our CEX-style monthly report.")
    parser.add_argument("--month", default="2026-02", help="Month, format YYYY-MM")
    parser.add_argument("--outdir", default="reports/2026-02/our_style_report", help="Output directory")
    args = parser.parse_args()

    start, end_excl = parse_month(args.month)
    month_label = args.month

    rows, source_ts = fetch_exchanges()
    global_points = fetch_global(start, end_excl)
    fng = fetch_fng()

    outdir = Path(args.outdir)
    csv_path = outdir / "our_style_exchange_data.csv"
    chart_path = outdir / "our_style_dashboard.png"
    report_path = outdir / "our_style_report.md"

    write_csv(rows, csv_path)
    plot_dashboard(rows, global_points, chart_path, month_label)
    write_report(rows, global_points, fng, report_path, chart_path, csv_path, month_label, source_ts)

    print(f"Report: {report_path}")
    print(f"Chart:  {chart_path}")
    print(f"CSV:    {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
