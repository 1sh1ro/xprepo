#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CSV_PATH = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/deribit/deribit_funding_snapshot.csv")
OUT_MAIN = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/charts/chart_deribit_funding.png")
OUT_PKG = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/deribit/chart_deribit_funding.png")


def read_rows() -> list[tuple[str, float, float]]:
    rows: list[tuple[str, float, float]] = []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ccy = str(row.get("currency") or "").upper().strip()
            if ccy not in ("BTC", "ETH"):
                continue
            try:
                funding_8h = float(row.get("funding_8h") or 0.0) * 10000.0
            except Exception:
                funding_8h = 0.0
            try:
                current_funding = float(row.get("current_funding") or 0.0) * 10000.0
            except Exception:
                current_funding = 0.0
            rows.append((ccy, funding_8h, current_funding))
    order = {"BTC": 0, "ETH": 1}
    rows.sort(key=lambda x: order.get(x[0], 99))
    return rows


def plot(rows: list[tuple[str, float, float]]) -> None:
    labels = [r[0] for r in rows]
    f8 = [r[1] for r in rows]
    cur = [r[2] for r in rows]

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.grid": True,
            "grid.color": "#E9EDF4",
            "grid.alpha": 1.0,
            "axes.edgecolor": "#D9DEE7",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "legend.frameon": False,
        }
    )

    x = np.arange(len(labels))
    w = 0.32

    fig, ax = plt.subplots(figsize=(9.2, 4.8))

    color_8h = "#F97316"
    color_cur = "#4F8CD6"

    b1 = ax.bar(x - w / 2, f8, width=w, color=color_8h, label="Funding 8h (bps)")
    b2 = ax.bar(x + w / 2, cur, width=w, color=color_cur, label="Current funding (bps)")

    ax.axhline(0, color="#AEB6C2", linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("bps")
    ax.set_title("Deribit Perp Funding Snapshot", loc="left", fontweight="bold")
    ax.legend(loc="upper right")

    max_abs = max([abs(v) for v in f8 + cur] + [0.8])
    ax.set_ylim(-max_abs * 1.5, max_abs * 1.5)

    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            x0 = bar.get_x() + bar.get_width() / 2
            if h >= 0:
                y0 = h + max_abs * 0.06
                va = "bottom"
            else:
                y0 = h - max_abs * 0.08
                va = "top"
            ax.text(x0, y0, f"{h:+.2f}", ha="center", va=va, fontsize=10)

    fig.text(0.01, 0.01, "Source: Deribit public/ticker", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.04, 1, 1])

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    OUT_PKG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_MAIN, dpi=180)
    fig.savefig(OUT_PKG, dpi=180)
    plt.close(fig)


def main() -> int:
    rows = read_rows()
    if not rows:
        raise SystemExit("no funding rows")
    plot(rows)
    print("[ok] redrawn:", OUT_MAIN)
    print("[ok] redrawn:", OUT_PKG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
