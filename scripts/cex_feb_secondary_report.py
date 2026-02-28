#!/usr/bin/env python3
"""
Generate a February secondary-market change report for leading exchanges
using CoinMarketCap public data-api endpoint.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


CMC_QUOTES_LATEST = "https://api.coinmarketcap.com/data-api/v3/exchange/quotes/latest"

# CMC front exchanges discussed in this thread (as of 2026-02-27 page view).
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
    volume24h: Optional[float]
    volume7d: Optional[float]
    volume30d: Optional[float]
    pct24h: Optional[float]
    pct7d: Optional[float]
    pct30d: Optional[float]
    spot24h: Optional[float]
    deriv24h: Optional[float]
    prev30d_est: Optional[float]


def to_float(v: Any) -> Optional[float]:
    if isinstance(v, (int, float)):
        return float(v)
    return None


def to_int(v: Any) -> Optional[int]:
    if isinstance(v, int):
        return v
    if isinstance(v, float) and float(v).is_integer():
        return int(v)
    return None


def fmt_usd(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    abs_v = abs(v)
    if abs_v >= 1e12:
        s = f"${v/1e12:.2f}T"
    elif abs_v >= 1e9:
        s = f"${v/1e9:.2f}B"
    elif abs_v >= 1e6:
        s = f"${v/1e6:.2f}M"
    else:
        s = f"${v:,.0f}"
    return s


def fmt_pct(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    return f"{v:+.2f}%"


def fetch_quotes(slugs: List[str]) -> Dict[str, Any]:
    params = {"slug": ",".join(slugs), "convert": "USD"}
    url = f"{CMC_QUOTES_LATEST}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "cex-feb-secondary-report/1.0", "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return json.loads(raw.decode("utf-8"))


def parse_rows(payload: Dict[str, Any]) -> List[ExchangeRow]:
    rows: List[ExchangeRow] = []
    data = payload.get("data") if isinstance(payload.get("data"), list) else []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "")
        slug = str(item.get("slug") or "")
        rank = to_int(item.get("rank"))

        quote = item.get("quote")
        q: Dict[str, Any] = {}
        if isinstance(quote, list) and quote and isinstance(quote[0], dict):
            q = quote[0]

        volume30d = to_float(q.get("volume30d"))
        pct30d = to_float(q.get("percentChangeVolume30d"))
        prev30d_est: Optional[float] = None
        if volume30d is not None and pct30d is not None and not math.isclose(pct30d, -100.0):
            denom = 1.0 + pct30d / 100.0
            if not math.isclose(denom, 0.0):
                prev30d_est = volume30d / denom

        rows.append(
            ExchangeRow(
                rank=rank,
                name=name,
                slug=slug,
                last_updated=q.get("lastUpdated") if isinstance(q.get("lastUpdated"), str) else None,
                volume24h=to_float(q.get("volume24h")),
                volume7d=to_float(q.get("volume7d")),
                volume30d=volume30d,
                pct24h=to_float(q.get("percentChangeVolume24h")),
                pct7d=to_float(q.get("percentChangeVolume7d")),
                pct30d=pct30d,
                spot24h=to_float(q.get("spotVolumeUsd")),
                deriv24h=to_float(q.get("derivativeVolumeUsd")),
                prev30d_est=prev30d_est,
            )
        )
    rows.sort(key=lambda r: (r.rank is None, r.rank if r.rank is not None else 10_000, r.name))
    return rows


def write_csv(rows: List[ExchangeRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank",
                "name",
                "slug",
                "last_updated",
                "volume30d_usd",
                "prev30d_est_usd",
                "percent_change_volume30d",
                "volume7d_usd",
                "percent_change_volume7d",
                "volume24h_usd",
                "percent_change_volume24h",
                "spot_volume_24h_usd",
                "deriv_volume_24h_usd",
                "spot_share_24h_pct",
            ]
        )
        for r in rows:
            total_24h = (r.spot24h or 0.0) + (r.deriv24h or 0.0)
            spot_share = ((r.spot24h or 0.0) / total_24h * 100.0) if total_24h > 0 else None
            w.writerow(
                [
                    r.rank,
                    r.name,
                    r.slug,
                    r.last_updated,
                    r.volume30d,
                    r.prev30d_est,
                    r.pct30d,
                    r.volume7d,
                    r.pct7d,
                    r.volume24h,
                    r.pct24h,
                    r.spot24h,
                    r.deriv24h,
                    spot_share,
                ]
            )


def plot(rows: List[ExchangeRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    names = [r.name for r in rows]
    x = list(range(len(rows)))
    curr = [(r.volume30d or 0.0) / 1e9 for r in rows]
    prev = [(r.prev30d_est or 0.0) / 1e9 for r in rows]
    pct = [r.pct30d or 0.0 for r in rows]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    width = 0.38
    ax1.bar([i - width / 2 for i in x], prev, width=width, color="#b0b8c1", label="Prev 30d (est.)")
    ax1.bar([i + width / 2 for i in x], curr, width=width, color="#1f77b4", label="Current 30d")
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=30, ha="right")
    ax1.set_ylabel("Volume (B USD)")
    ax1.set_title("Top Exchanges: 30d Volume (Estimated Previous vs Current)")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.legend()

    colors = ["#2ca02c" if p >= 0 else "#d62728" for p in pct]
    ax2.bar(x, pct, color=colors)
    ax2.axhline(0, color="black", linewidth=1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=30, ha="right")
    ax2.set_ylabel("%")
    ax2.set_title("30d Volume Change (%)")
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    for i, p in enumerate(pct):
        ax2.text(i, p + (0.6 if p >= 0 else -0.9), f"{p:+.1f}%", ha="center", va="bottom" if p >= 0 else "top", fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def write_report(
    rows: List[ExchangeRow],
    chart_path: Path,
    csv_path: Path,
    out_path: Path,
    source_timestamp: Optional[str],
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_curr = sum((r.volume30d or 0.0) for r in rows)
    valid_prev = [r.prev30d_est for r in rows if r.prev30d_est is not None]
    total_prev = sum(valid_prev) if valid_prev else None
    total_change = ((total_curr / total_prev - 1.0) * 100.0) if total_prev and total_prev != 0 else None

    rising = sorted([r for r in rows if r.pct30d is not None], key=lambda r: r.pct30d or -1e9, reverse=True)
    falling = sorted([r for r in rows if r.pct30d is not None], key=lambda r: r.pct30d or 1e9)

    gen_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines: List[str] = []
    lines.append("# 前排交易所 2 月二级市场变化报告（CMC 口径）")
    lines.append("")
    lines.append(f"- 生成时间（UTC）：{gen_time}")
    if source_timestamp:
        lines.append(f"- 数据快照时间（CMC）：{source_timestamp}")
    lines.append("- 样本：Binance, Coinbase Exchange, Upbit, OKX, Bybit, Bitget, Gate, KuCoin, MEXC, HTX")
    lines.append("- 口径说明：")
    lines.append("  - `volume30d` 为滚动 30 天成交额，不等于完整自然月。")
    lines.append("  - `percentChangeVolume30d` 为当前滚动 30 天相对前一滚动 30 天变化。")
    lines.append("  - 本报告将其作为“2 月窗口变化”的近似观测。")
    lines.append("")
    lines.append("## 关键结论")
    lines.append(f"- 前排样本合计滚动 30 天成交额：{fmt_usd(total_curr)}")
    lines.append(f"- 估算前一滚动 30 天成交额：{fmt_usd(total_prev)}")
    lines.append(f"- 合计变化：{fmt_pct(total_change)}")
    if rising:
        top_up = rising[:3]
        lines.append("- 30 天增幅靠前：")
        for r in top_up:
            lines.append(f"  - {r.name}: {fmt_pct(r.pct30d)}")
    if falling:
        top_down = falling[:3]
        lines.append("- 30 天回落靠前：")
        for r in top_down:
            lines.append(f"  - {r.name}: {fmt_pct(r.pct30d)}")
    lines.append("")
    lines.append("## 明细表（按 CMC 排名）")
    lines.append("| Rank | Exchange | 30d Volume | 30d Change | Est. Prev 30d | 24h Spot | 24h Derivatives |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        lines.append(
            f"| {r.rank if r.rank is not None else 'N/A'} | {r.name} | {fmt_usd(r.volume30d)} | {fmt_pct(r.pct30d)} | {fmt_usd(r.prev30d_est)} | {fmt_usd(r.spot24h)} | {fmt_usd(r.deriv24h)} |"
        )
    lines.append("")
    lines.append("## 图表")
    lines.append(f"![cex-feb-secondary-market]({chart_path.name})")
    lines.append("")
    lines.append("## 参考链接（月报/口径参考）")
    lines.append("- CMC Spot Exchanges: https://coinmarketcap.com/rankings/exchanges/")
    lines.append("- Coinbase Institutional (Feb 2026): https://www.coinbase.com/institutional/research-insights/research/trading-insights/crypto-market-positioning-february-2026")
    lines.append("- OKX Proof of Reserves (Feb 2026 snapshots): https://www.okx.com/proof-of-reserves")
    lines.append("- KuCoin Market Bulletin (Feb 2026): https://www.kucoin.com/news/articles/crypto-daily-market-report-february-25-2026")
    lines.append("")
    lines.append("## 数据文件")
    lines.append(f"- CSV: `{csv_path.name}`")
    lines.append(f"- Chart: `{chart_path.name}`")
    lines.append("")
    lines.append("## 数据源（API）")
    lines.append(f"- `{CMC_QUOTES_LATEST}`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Feb secondary-market report from CMC exchange quotes.")
    parser.add_argument("--outdir", default="reports/2026-02/top10_feb_secondary", help="Output directory")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    payload = fetch_quotes(EXCHANGE_SLUGS)
    rows = parse_rows(payload)
    if not rows:
        raise SystemExit("No rows returned from CMC exchange quotes endpoint.")

    status = payload.get("status") if isinstance(payload.get("status"), dict) else {}
    source_ts = status.get("timestamp") if isinstance(status.get("timestamp"), str) else None

    csv_path = outdir / "top10_feb_secondary_data.csv"
    chart_path = outdir / "top10_feb_secondary_chart.png"
    report_path = outdir / "top10_feb_secondary_report.md"

    write_csv(rows, csv_path)
    plot(rows, chart_path)
    write_report(rows, chart_path, csv_path, report_path, source_ts)

    print(f"Report: {report_path}")
    print(f"Chart:  {chart_path}")
    print(f"CSV:    {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
