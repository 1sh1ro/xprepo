#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/fig6/fig6_altcoin_outside_top10_share.csv")
OUT_MAIN = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/charts/fig6_altcoin_outside_top10_share.png")
OUT_PKG = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/fig6/fig6_altcoin_outside_top10_share.png")


def read_row() -> dict[str, float | str]:
    with CSV_PATH.open("r", encoding="utf-8") as f:
        row = next(csv.DictReader(f))

    total = float(row["total_market_cap_usd"])
    btc = float(row["btc_market_cap_usd"])
    top10_alt = float(row["top10_alt_market_cap_usd"])
    outside = float(row["outside_top10_alt_market_cap_usd"])
    return {
        "month": row["month"],
        "total": total,
        "btc_pct": btc / total * 100.0 if total else 0.0,
        "top10_alt_pct": top10_alt / total * 100.0 if total else 0.0,
        "outside_pct": outside / total * 100.0 if total else 0.0,
    }


def plot(d: dict[str, float | str]) -> None:
    month = str(d["month"])
    btc_pct = float(d["btc_pct"])
    top10_alt_pct = float(d["top10_alt_pct"])
    outside_pct = float(d["outside_pct"])
    total_t = float(d["total"]) / 1e12

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.edgecolor": "#D9DEE7",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "legend.frameon": False,
        }
    )

    fig, ax = plt.subplots(figsize=(10.6, 4.3))

    y = [0]
    ax.barh(y, [btc_pct], color="#4F8CD6", height=0.42, label="BTC")
    ax.barh(y, [top10_alt_pct], left=[btc_pct], color="#66BB6A", height=0.42, label="Top10 Alt")
    ax.barh(y, [outside_pct], left=[btc_pct + top10_alt_pct], color="#F5A623", height=0.42, label="Outside Top10")

    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("Share of total market cap (%)")
    ax.set_title("Altcoin Market Breadth Composition", loc="left", fontweight="bold")
    ax.grid(True, axis="x", color="#E9EDF4")

    # Segment labels
    if btc_pct >= 7:
        ax.text(btc_pct / 2, 0, f"BTC\n{btc_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    if top10_alt_pct >= 7:
        ax.text(btc_pct + top10_alt_pct / 2, 0, f"Top10 Alt\n{top10_alt_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    if outside_pct >= 5:
        ax.text(btc_pct + top10_alt_pct + outside_pct / 2, 0, f"Outside\n{outside_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")

    # Highlight outside share
    ax.annotate(
        f"Outside Top10 share: {outside_pct:.2f}%",
        xy=(btc_pct + top10_alt_pct + outside_pct * 0.5, 0),
        xytext=(0, 36),
        textcoords="offset points",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color="#C26C00",
        arrowprops={"arrowstyle": "-|>", "color": "#C26C00", "lw": 1.1},
    )

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=3)

    fig.text(0.02, 0.06, f"Month: {month} | Total market cap: ${total_t:.2f}T", fontsize=10, color="#5F6B7A")
    fig.text(0.02, 0.02, "Source: CMC historical global metrics + top10 aggregation", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.10, 1, 1])

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    OUT_PKG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_MAIN, dpi=180)
    fig.savefig(OUT_PKG, dpi=180)
    plt.close(fig)


def main() -> int:
    d = read_row()
    plot(d)
    print("[ok] redrawn:", OUT_MAIN)
    print("[ok] redrawn:", OUT_PKG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
