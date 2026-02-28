#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/deribit")
OI_CSV = BASE / "deribit_oi_volume_snapshot.csv"
FUNDING_CSV = BASE / "deribit_funding_snapshot.csv"
OUT_MAIN = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/charts/chart_deribit_oi.png")
OUT_PKG = BASE / "chart_deribit_oi.png"


def read_prices() -> dict[str, float]:
    prices: dict[str, float] = {}
    with FUNDING_CSV.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ccy = str(row.get("currency") or "").upper().strip()
            px_raw = row.get("last_price")
            if not ccy or px_raw in (None, ""):
                continue
            try:
                prices[ccy] = float(px_raw)
            except Exception:
                continue
    return prices


def read_oi_usd(prices: dict[str, float]) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    with OI_CSV.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            c = str(row.get("currency") or "").upper().strip()
            k = str(row.get("kind") or "").lower().strip()
            oi_raw = row.get("open_interest_sum")
            if c not in ("BTC", "ETH") or k not in ("future", "option") or oi_raw in (None, ""):
                continue
            try:
                oi = float(oi_raw)
            except Exception:
                continue
            if k == "future":
                usd = oi
            else:
                # Options OI is in native units (BTC/ETH); convert to USD notionals.
                px = prices.get(c)
                usd = oi * px if px is not None else 0.0
            out[(c, k)] = usd
    return out


def plot(oi_usd: dict[tuple[str, str], float]) -> None:
    labels = ["BTC", "ETH"]
    fut_b = [oi_usd.get((ccy, "future"), 0.0) / 1e9 for ccy in labels]
    opt_b = [oi_usd.get((ccy, "option"), 0.0) / 1e9 for ccy in labels]

    x = np.arange(len(labels))
    w = 0.34

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

    fig, ax = plt.subplots(figsize=(10.2, 4.8))

    b1 = ax.bar(x - w / 2, fut_b, width=w, color="#4F8CD6", label="Futures OI (USD)")
    b2 = ax.bar(x + w / 2, opt_b, width=w, color="#F5A623", label="Options OI (USD converted)")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("USD billions")
    ax.set_title("Deribit OI by Currency (USD-normalized)", loc="left", fontweight="bold")
    ax.legend(loc="upper right")

    ymax = max(fut_b + opt_b + [1.0])
    ax.set_ylim(0, ymax * 1.18)

    for bars in (b1, b2):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + ymax * 0.01, f"{h:.2f}B", ha="center", va="bottom", fontsize=10)

    fig.text(
        0.01,
        0.01,
        "Source: Deribit public/get_book_summary_by_currency + public/ticker (options OI converted from native units)",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    OUT_PKG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_MAIN, dpi=180)
    fig.savefig(OUT_PKG, dpi=180)
    plt.close(fig)


def main() -> int:
    prices = read_prices()
    oi_usd = read_oi_usd(prices)
    plot(oi_usd)
    print("[ok] redrawn:", OUT_MAIN)
    print("[ok] redrawn:", OUT_PKG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
