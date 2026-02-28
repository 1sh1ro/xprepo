#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/fig3/fig3_defi_tvl_share.csv")
OUT_MAIN = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/charts/fig3_defi_tvl_share.png")
OUT_PKG = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/fig3/fig3_defi_tvl_share.png")


def read_row() -> dict[str, float]:
    with CSV_PATH.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        row = next(r)
    return {
        "Ethereum": float(row["ethereum_share_pct"]),
        "Solana": float(row["solana_share_pct"]),
        "BSC": float(row["bsc_share_pct"]),
        "Bitcoin": float(row["bitcoin_share_pct"]),
        "Base": float(row["base_share_pct"]),
        "Others": float(row["others_share_pct"]),
        "total_tvl_usd": float(row["total_tvl_usd"]),
        "month": row["month"],
    }


def plot(d: dict[str, float]) -> None:
    labels = ["Ethereum", "Solana", "BSC", "Bitcoin", "Base", "Others"]
    vals = [d[k] for k in labels]
    colors = ["#4CAF50", "#66BB6A", "#F4B400", "#5C6BC0", "#2F7ED8", "#8D6E63"]

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.size": 11,
        }
    )

    fig, ax = plt.subplots(figsize=(8.2, 5.6))

    wedges, _, autotexts = ax.pie(
        vals,
        labels=None,
        autopct=lambda p: f"{p:.1f}%" if p >= 4.0 else "",
        startangle=90,
        counterclock=False,
        colors=colors,
        pctdistance=0.80,
        wedgeprops={"width": 0.40, "edgecolor": "white", "linewidth": 1.2},
    )

    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(10)
        t.set_fontweight("bold")

    ax.set_title("DeFi TVL Share by Chain", loc="left", fontsize=15, fontweight="bold", pad=14)
    ax.legend(wedges, labels, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.08), frameon=False)

    total_b = d["total_tvl_usd"] / 1e9
    ax.text(0, 0.10, f"{d['month']}", ha="center", va="center", fontsize=11, color="#607080")
    ax.text(0, -0.06, f"TVL ${total_b:.2f}B", ha="center", va="center", fontsize=12, fontweight="bold", color="#2C3E50")

    fig.text(0.02, 0.02, "Source: DefiLlama protocol TVL aggregation", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.06, 1, 1])

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    OUT_PKG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_MAIN, dpi=180)
    fig.savefig(OUT_PKG, dpi=180)
    plt.close(fig)


def main() -> int:
    data = read_row()
    plot(data)
    print("[ok] redrawn:", OUT_MAIN)
    print("[ok] redrawn:", OUT_PKG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
