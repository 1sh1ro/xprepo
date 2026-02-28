#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import mean
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

BASE = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/supplement")
CHARTS = BASE / "charts"
DERIBIT_DVOL = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/deribit/deribit_dvol_daily.csv")
SUPPLEMENT_MD = BASE / "feb_missing_sections_supplement.md"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.edgecolor": "#D9DEE7",
            "axes.grid": True,
            "grid.color": "#E9EDF4",
            "grid.alpha": 1.0,
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "legend.frameon": False,
        }
    )


def parse_day(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def read_funding(path: Path) -> Tuple[List[date], List[float], List[float], List[float], Tuple[date, float], Tuple[date, float]]:
    by_day: Dict[date, List[float]] = defaultdict(list)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = parse_day(str(row["date"]))
                v = float(row["funding_rate"])
            except Exception:
                continue
            by_day[d].append(v)

    days = sorted(by_day.keys())
    mins = [min(by_day[d]) * 10000 for d in days]
    maxs = [max(by_day[d]) * 10000 for d in days]
    avgs = [mean(by_day[d]) * 10000 for d in days]
    hi_idx = max(range(len(days)), key=lambda i: maxs[i])
    lo_idx = min(range(len(days)), key=lambda i: mins[i])
    hi = (days[hi_idx], maxs[hi_idx])
    lo = (days[lo_idx], mins[lo_idx])
    return days, mins, maxs, avgs, hi, lo


def plot_okx_funding() -> Path:
    btc = read_funding(BASE / "okx_funding_btc_feb2026.csv")
    eth = read_funding(BASE / "okx_funding_eth_feb2026.csv")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    for ax, data, color, title in [
        (axes[0], btc, "#F7931A", "BTC-USDT-SWAP"),
        (axes[1], eth, "#627EEA", "ETH-USDT-SWAP"),
    ]:
        days, mins, maxs, avgs, hi, lo = data
        ax.fill_between(days, mins, maxs, color=color, alpha=0.18, label="Daily min-max range")
        ax.plot(days, avgs, color=color, linewidth=2.0, label="Daily average")
        ax.scatter([hi[0], lo[0]], [hi[1], lo[1]], color=["#0F9D58", "#DB4437"], s=42, zorder=5)
        ax.annotate(
            f"High {hi[1]:+.2f} bps\n{hi[0].isoformat()}",
            xy=(hi[0], hi[1]),
            xytext=(10, 8),
            textcoords="offset points",
            fontsize=9,
            color="#0F9D58",
        )
        ax.annotate(
            f"Low {lo[1]:+.2f} bps\n{lo[0].isoformat()}",
            xy=(lo[0], lo[1]),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=9,
            color="#DB4437",
        )
        ax.axhline(0, color="#AEB6C2", linewidth=1)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_ylabel("Funding (bps)")
        ax.legend(loc="upper right")

    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    axes[1].xaxis.set_major_locator(mdates.DayLocator(interval=3))
    fig.suptitle("OKX Funding Rate Extremes Replay | Feb 2026", fontsize=15, fontweight="bold", y=0.98)
    fig.text(0.01, 0.01, "Source: OKX public/funding-rate-history", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    out = CHARTS / "fig_s1_okx_funding_extremes.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def read_dvol() -> Tuple[List[date], List[float], List[float]]:
    days: List[date] = []
    btc: List[float] = []
    eth: List[float] = []
    with DERIBIT_DVOL.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = parse_day(str(row["date"]))
                b = float(row["btc_dvol_close"])
                e = float(row["eth_dvol_close"])
            except Exception:
                continue
            if d.month == 2 and d.year == 2026:
                days.append(d)
                btc.append(b)
                eth.append(e)
    return days, btc, eth


def plot_dvol_phases() -> Path:
    days, btc, eth = read_dvol()

    min_idx = min(range(len(days)), key=lambda i: btc[i])
    max_idx = max(range(len(days)), key=lambda i: btc[i])
    if max_idx < min_idx:
        min_idx, max_idx = max_idx, min_idx

    min_day = days[min_idx]
    max_day = days[max_idx]

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axvspan(days[0], min_day, color="#E8F5E9", alpha=0.65, label="Complacency")
    ax.axvspan(min_day, max_day, color="#FDECEA", alpha=0.7, label="Panic")
    ax.axvspan(max_day, days[-1], color="#EEF3FB", alpha=0.8, label="Normalization")

    ax.plot(days, btc, color="#F7931A", linewidth=2.2, label="BTC DVOL")
    ax.plot(days, eth, color="#627EEA", linewidth=2.2, label="ETH DVOL")

    ax.scatter([min_day, max_day], [btc[min_idx], btc[max_idx]], color=["#0F9D58", "#DB4437"], s=46, zorder=6)
    ax.annotate(
        f"BTC low {btc[min_idx]:.2f}\n{min_day.isoformat()}",
        xy=(min_day, btc[min_idx]),
        xytext=(8, -30),
        textcoords="offset points",
        fontsize=9,
        color="#0F9D58",
    )
    ax.annotate(
        f"BTC peak {btc[max_idx]:.2f}\n{max_day.isoformat()}",
        xy=(max_day, btc[max_idx]),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=9,
        color="#DB4437",
    )

    ax.set_title("Deribit DVOL Phase Narrative | Feb 2026", loc="left", fontweight="bold")
    ax.set_ylabel("DVOL")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.legend(ncols=5, loc="upper right")

    fig.text(0.01, 0.01, "Source: Deribit public/get_volatility_index_data", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.03, 1, 1])

    out = CHARTS / "fig_s2_dvol_phase_narrative.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def read_fng() -> Tuple[List[date], List[int], List[str]]:
    days: List[date] = []
    vals: List[int] = []
    cls: List[str] = []
    with (BASE / "fng_daily_feb2026.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = parse_day(str(row["date"]))
                v = int(row["value"])
            except Exception:
                continue
            days.append(d)
            vals.append(v)
            cls.append(str(row.get("classification") or ""))
    return days, vals, cls


def plot_fng_keypoints() -> Path:
    days, vals, _ = read_fng()

    deltas = [None]
    for i in range(1, len(vals)):
        deltas.append(vals[i] - vals[i - 1])

    hi_idx = max(range(len(vals)), key=lambda i: vals[i])
    lo_idx = min(range(len(vals)), key=lambda i: vals[i])
    up_idx = max(range(1, len(vals)), key=lambda i: vals[i] - vals[i - 1])
    down_idx = min(range(1, len(vals)), key=lambda i: vals[i] - vals[i - 1])

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axhspan(0, 25, color="#FCE8E6", alpha=0.6)
    ax.axhspan(25, 45, color="#FFF3E0", alpha=0.5)
    ax.axhspan(45, 55, color="#F5F7FA", alpha=0.5)

    ax.plot(days, vals, color="#1E88E5", linewidth=2.2, marker="o", markersize=3)

    hi_off = 10
    up_off = 10
    lo_off = -28
    down_off = -30
    if hi_idx == up_idx:
        hi_off = 10
        up_off = 40
    if lo_idx == down_idx:
        lo_off = 10
        down_off = 40

    points = [
        (hi_idx, "Month high", "#0F9D58", hi_off),
        (lo_idx, "Month low", "#DB4437", lo_off),
        (up_idx, f"Largest up {deltas[up_idx]:+d}", "#00897B", up_off),
        (down_idx, f"Largest down {deltas[down_idx]:+d}", "#8E24AA", down_off),
    ]
    for idx, label, color, yoff in points:
        ax.scatter(days[idx], vals[idx], color=color, s=45, zorder=6)
        ax.annotate(
            f"{label}\n{days[idx].isoformat()} ({vals[idx]})",
            xy=(days[idx], vals[idx]),
            xytext=(10, yoff),
            textcoords="offset points",
            fontsize=9,
            color=color,
        )

    ax.set_title("Fear & Greed Key Timestamp Mapping | Feb 2026", loc="left", fontweight="bold")
    ax.set_ylabel("Index")
    ax.set_ylim(0, 60)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))

    fig.text(0.01, 0.01, "Source: Alternative.me F&G API", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.03, 1, 1])

    out = CHARTS / "fig_s3_fng_keypoints.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def read_trends() -> Tuple[List[date], List[int], List[int], List[int]]:
    days: List[date] = []
    btc: List[int] = []
    eth: List[int] = []
    meme: List[int] = []
    with (BASE / "google_trends_daily_feb2026.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = parse_day(str(row["date"]))
                b = int(row["Bitcoin"])
                e = int(row["Ethereum"])
                m = int(row["Memecoin"])
            except Exception:
                continue
            days.append(d)
            btc.append(b)
            eth.append(e)
            meme.append(m)
    return days, btc, eth, meme


def plot_google_trends() -> Path:
    days, btc, eth, meme = read_trends()

    p1_end = date(2026, 2, 10)
    p2_end = date(2026, 2, 20)

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axvspan(days[0], p1_end, color="#E3F2FD", alpha=0.55)
    ax.axvspan(p1_end, p2_end, color="#F1F8E9", alpha=0.55)
    ax.axvspan(p2_end, days[-1], color="#FFF8E1", alpha=0.55)

    ax.plot(days, btc, color="#F7931A", linewidth=2.2, label="Bitcoin")
    ax.plot(days, eth, color="#627EEA", linewidth=2.0, label="Ethereum")
    ax.plot(days, meme, color="#5F6B7A", linewidth=1.8, label="Memecoin")

    ax.axvline(p1_end, color="#9AA5B1", linestyle="--", linewidth=1)
    ax.axvline(p2_end, color="#9AA5B1", linestyle="--", linewidth=1)

    ax.text(days[1], max(btc) * 0.92, "Phase 1\n(1-10)", fontsize=9, color="#3E4C59")
    ax.text(date(2026, 2, 12), max(btc) * 0.92, "Phase 2\n(11-20)", fontsize=9, color="#3E4C59")
    ax.text(date(2026, 2, 22), max(btc) * 0.92, "Phase 3\n(21-28)", fontsize=9, color="#3E4C59")

    ax.set_title("Google Trends: Three-Phase Attention Shift | Feb 2026", loc="left", fontweight="bold")
    ax.set_ylabel("Search interest")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.legend(ncols=3, loc="upper right")

    fig.text(0.01, 0.01, "Source: Google Trends via pytrends (Global, daily)", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.03, 1, 1])

    out = CHARTS / "fig_s4_google_trends_three_phases.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def read_stablecoin_weekly() -> Tuple[List[date], List[float], List[float], List[float]]:
    weeks: List[date] = []
    usdt_share: List[float] = []
    usdc_share: List[float] = []
    total_bn: List[float] = []
    with (BASE / "stablecoin_weekly_usdt_usdc_feb2026.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                w = parse_day(str(row["week_start"]))
                s1 = float(row["usdt_share_pct"])
                s2 = float(row["usdc_share_pct"])
                t = float(row["total_usdt_usdc_weekly_volume_usd"]) / 1e9
            except Exception:
                continue
            weeks.append(w)
            usdt_share.append(s1)
            usdc_share.append(s2)
            total_bn.append(t)
    return weeks, usdt_share, usdc_share, total_bn


def plot_stablecoin_weekly() -> Path:
    weeks, usdt_share, usdc_share, total_bn = read_stablecoin_weekly()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6.8), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.2]})

    ax1.stackplot(weeks, usdt_share, usdc_share, colors=["#26A17B", "#2775CA"], alpha=0.72, labels=["USDT share", "USDC share"])
    ax1.plot(weeks, usdt_share, color="#1B8F6B", linewidth=1.8)
    ax1.plot(weeks, usdc_share, color="#1F5FA8", linewidth=1.8)
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Share (%)")
    ax1.set_title("Stablecoin Weekly Trend: USDT vs USDC | Feb 2026", loc="left", fontweight="bold")
    ax1.legend(loc="upper right", ncols=2)

    ax2.bar(weeks, total_bn, color="#8AA4D6", width=4.5)
    ax2.set_ylabel("Total vol (B USD)")
    ax2.set_xlabel("Week start")

    ax1.annotate(
        f"Start USDT {usdt_share[0]:.2f}%",
        xy=(weeks[0], usdt_share[0]),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=9,
        color="#1B8F6B",
    )
    ax1.annotate(
        f"End USDT {usdt_share[-1]:.2f}%",
        xy=(weeks[-1], usdt_share[-1]),
        xytext=(8, -24),
        textcoords="offset points",
        fontsize=9,
        color="#1B8F6B",
    )

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))

    fig.text(0.01, 0.01, "Source: CoinGecko coins/{id}/market_chart total_volumes", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.03, 1, 1])

    out = CHARTS / "fig_s5_stablecoin_weekly_trend.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def embed_images(md_path: Path) -> None:
    content = md_path.read_text(encoding="utf-8")
    inserts = {
        "## 1) 单一交易所 Funding 极值时序复盘（OKX)": "![](./charts/fig_s1_okx_funding_extremes.png)",
    }
    # robust line-based insertion by section header
    lines = content.splitlines()
    out_lines: List[str] = []

    def maybe_insert(header: str, image_rel: str) -> None:
        pass

    mapping = {
        "## 1) 单一交易所 Funding 极值时序复盘（OKX）": "![](./charts/fig_s1_okx_funding_extremes.png)",
        "## 2) DVOL 分阶段叙事（Complacency / Panic）": "![](./charts/fig_s2_dvol_phase_narrative.png)",
        "## 3) F&G 关键时点映射": "![](./charts/fig_s3_fng_keypoints.png)",
        "## 4) Google Trends 搜索热度三阶段": "![](./charts/fig_s4_google_trends_three_phases.png)",
        "## 5) 稳定币周度趋势（USDT vs USDC）": "![](./charts/fig_s5_stablecoin_weekly_trend.png)",
    }

    for idx, line in enumerate(lines):
        out_lines.append(line)
        if line in mapping:
            next_line = lines[idx + 1] if idx + 1 < len(lines) else ""
            if mapping[line] not in next_line:
                out_lines.append("")
                out_lines.append(mapping[line])

    md_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def main() -> int:
    CHARTS.mkdir(parents=True, exist_ok=True)
    setup_style()

    out_files = [
        plot_okx_funding(),
        plot_dvol_phases(),
        plot_fng_keypoints(),
        plot_google_trends(),
        plot_stablecoin_weekly(),
    ]
    embed_images(SUPPLEMENT_MD)

    print("[ok] generated charts:")
    for p in out_files:
        print(" -", p)
    print("[ok] updated:", SUPPLEMENT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
