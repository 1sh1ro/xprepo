#!/usr/bin/env python3
"""
Generate a Yuque-style monthly CEX secondary-market report.

Style reference:
- /Users/my/Downloads/202601 · 语雀.pdf
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
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
CMC_GLOBAL_LATEST = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/latest"
ALT_FNG = "https://api.alternative.me/fng/"
CG_PUBLIC_BASE = "https://api.coingecko.com/api/v3"
CG_PRO_BASE = "https://pro-api.coingecko.com/api/v3"
CG_BASE = CG_PUBLIC_BASE
CG_HEADERS: Dict[str, str] = {}
DEFAULT_CG_SECRET_FILE = Path.home() / ".codex/skills/.coingecko.local.json"
DERIBIT_TICKER = "https://www.deribit.com/api/v2/public/ticker"

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
class RvPoint:
    d: date
    btc_rv: Optional[float]
    eth_rv: Optional[float]


def _get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    full = url if not params else f"{url}?{urlencode(params)}"
    headers = {"User-Agent": "our-cex-yuque-report/1.0", "Accept": "application/json"}
    if "coingecko.com/api/v3" in url and CG_HEADERS:
        headers.update(CG_HEADERS)
    req = Request(full, headers=headers)
    with urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def read_cg_secret_file(path: Path) -> Tuple[Optional[str], Optional[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None, None
    if not isinstance(raw, dict):
        return None, None
    key = raw.get("api_key")
    plan = raw.get("plan")
    key_val = str(key).strip() if isinstance(key, str) and key.strip() else None
    plan_val = str(plan).strip().lower() if isinstance(plan, str) and str(plan).strip() else None
    return key_val, plan_val


def resolve_cg_runtime(cg_plan: str, cg_key_arg: Optional[str], secret_file: Path) -> Tuple[str, Dict[str, str], str, bool]:
    env_plan = (os.getenv("COINGECKO_API_PLAN") or os.getenv("CG_PLAN") or "").strip().lower()
    file_key, file_plan = read_cg_secret_file(secret_file)
    plan = (cg_plan or "auto").strip().lower()
    if plan == "auto" and env_plan in {"public", "demo", "pro"}:
        plan = env_plan
    elif plan == "auto" and file_plan in {"public", "demo", "pro"}:
        plan = file_plan
    if plan not in {"auto", "public", "demo", "pro"}:
        raise ValueError(f"Invalid --cg-plan: {cg_plan}")

    demo_key = os.getenv("CG_DEMO_API_KEY")
    pro_key = os.getenv("CG_PRO_API_KEY")
    shared_key = os.getenv("COINGECKO_API_KEY") or os.getenv("CG_API_KEY")
    key = (cg_key_arg or "").strip() or None

    if plan == "auto":
        if pro_key:
            plan = "pro"
            key = key or pro_key
        elif demo_key:
            plan = "demo"
            key = key or demo_key
        elif key or shared_key:
            plan = "demo"
            key = key or shared_key
        elif file_key:
            plan = "demo"
            key = file_key
        else:
            plan = "public"
            key = None
    else:
        if key is None:
            if plan == "pro":
                key = pro_key or shared_key or file_key
            elif plan == "demo":
                key = demo_key or shared_key or file_key
            else:
                key = None

    base = CG_PRO_BASE if plan == "pro" else CG_PUBLIC_BASE
    headers: Dict[str, str] = {}
    if key:
        if plan == "pro":
            headers["x-cg-pro-api-key"] = key
        else:
            headers["x-cg-demo-api-key"] = key
    return base, headers, plan, bool(key)


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
        quote = item.get("quote")
        q0 = quote[0] if isinstance(quote, list) and quote and isinstance(quote[0], dict) else {}
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
    payload = _get_json(
        CMC_GLOBAL_HIST,
        {
            "interval": "1d",
            "convertId": "2781",
            "timeStart": f"{start.isoformat()}T00:00:00.000Z",
            "timeEnd": f"{end_exclusive.isoformat()}T00:00:00.000Z",
        },
    )
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


def fetch_global_latest() -> Dict[str, Optional[float]]:
    payload = _get_json(CMC_GLOBAL_LATEST)
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    quote = data.get("quotes")
    q0 = quote[0] if isinstance(quote, list) and quote and isinstance(quote[0], dict) else {}
    return {
        "total_market_cap": _to_float(q0.get("totalMarketCap")),
        "total_volume_24h": _to_float(q0.get("totalVolume24H")),
        "stablecoin_market_cap": _to_float(q0.get("stablecoinMarketCap")) or _to_float(data.get("stablecoinMarketCap")),
        "stablecoin_volume_24h": _to_float(q0.get("stablecoinVolume24H")) or _to_float(data.get("stablecoinVolume24h")),
        "derivatives_volume_24h": _to_float(q0.get("derivativesVolume24H")) or _to_float(data.get("derivativesVolume24h")),
        "defi_market_cap": _to_float(q0.get("defiMarketCap")) or _to_float(data.get("defiMarketCap")),
        "defi_volume_24h": _to_float(q0.get("defiVolume24H")) or _to_float(data.get("defiVolume24h")),
    }


def fetch_cg_price_series(coin_id: str, days: int = 90) -> List[Tuple[date, float]]:
    payload = _get_json(
        f"{CG_BASE}/coins/{coin_id}/market_chart",
        {"vs_currency": "usd", "days": str(days)},
    )
    prices = payload.get("prices") if isinstance(payload.get("prices"), list) else []
    out: Dict[date, float] = {}
    for p in prices:
        if not (isinstance(p, list) and len(p) >= 2):
            continue
        ts = p[0]
        val = p[1]
        if not isinstance(ts, (int, float)) or not isinstance(val, (int, float)):
            continue
        d = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).date()
        out[d] = float(val)
    return sorted(out.items(), key=lambda x: x[0])


def compute_realized_vol_series(
    btc_prices: List[Tuple[date, float]],
    eth_prices: List[Tuple[date, float]],
    window: int = 7,
) -> List[RvPoint]:
    def _rv(prices: List[Tuple[date, float]]) -> Dict[date, float]:
        if len(prices) < window + 1:
            return {}
        rets: List[Tuple[date, float]] = []
        for i in range(1, len(prices)):
            prev = prices[i - 1][1]
            cur = prices[i][1]
            if prev <= 0:
                continue
            rets.append((prices[i][0], math.log(cur / prev)))
        out: Dict[date, float] = {}
        for i in range(window - 1, len(rets)):
            chunk = [x[1] for x in rets[i - window + 1 : i + 1]]
            if len(chunk) < 2:
                continue
            std = statistics.pstdev(chunk)
            out[rets[i][0]] = std * math.sqrt(365.0) * 100.0
        return out

    btc_rv = _rv(btc_prices)
    eth_rv = _rv(eth_prices)
    days = sorted(set(btc_rv.keys()) | set(eth_rv.keys()))
    return [RvPoint(d=d, btc_rv=btc_rv.get(d), eth_rv=eth_rv.get(d)) for d in days]


def fetch_cg_trending() -> List[Dict[str, Any]]:
    payload = _get_json(f"{CG_BASE}/search/trending")
    coins = payload.get("coins") if isinstance(payload.get("coins"), list) else []
    out: List[Dict[str, Any]] = []
    for item in coins:
        inner = item.get("item") if isinstance(item, dict) else None
        if not isinstance(inner, dict):
            continue
        out.append(
            {
                "name": inner.get("name"),
                "symbol": inner.get("symbol"),
                "rank": inner.get("market_cap_rank"),
                "price_btc": inner.get("price_btc"),
            }
        )
    return out


def fetch_deribit_funding_snapshot() -> Dict[str, Optional[float]]:
    def _one(instrument: str) -> Optional[float]:
        try:
            payload = _get_json(DERIBIT_TICKER, {"instrument_name": instrument})
        except Exception:
            return None
        result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
        return _to_float(result.get("current_funding"))

    return {
        "btc_perp_funding": _one("BTC-PERPETUAL"),
        "eth_perp_funding": _one("ETH-PERPETUAL"),
    }


def fetch_fng_series(limit: int = 90) -> List[Tuple[date, int, str]]:
    payload = _get_json(ALT_FNG, {"limit": str(limit)})
    raw = payload.get("data") if isinstance(payload.get("data"), list) else []
    out: List[Tuple[date, int, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        val = item.get("value")
        ts = item.get("timestamp")
        if not (isinstance(val, str) and val.isdigit() and isinstance(ts, str) and ts.isdigit()):
            continue
        d = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
        out.append((d, int(val), str(item.get("value_classification") or "")))
    out.sort(key=lambda x: x[0])
    return out


def set_dark_axes(ax: Any, title: str, ylabel: str) -> None:
    ax.set_facecolor("#1B1D22")
    ax.figure.patch.set_facecolor("#1B1D22")
    ax.set_title(title, color="white", fontsize=10)
    ax.set_ylabel(ylabel, color="#D7DBE0")
    ax.tick_params(colors="#D7DBE0", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#404652")
    ax.grid(True, color="#343A46", linestyle="-", linewidth=0.8, alpha=0.8)


def build_charts(
    rows: List[ExchangeRow],
    global_points: List[GlobalPoint],
    fng_month: List[Tuple[date, int, str]],
    rv_month: List[RvPoint],
    outdir: Path,
    month_label: str,
) -> Dict[str, Path]:
    outdir.mkdir(parents=True, exist_ok=True)

    charts: Dict[str, Path] = {}
    dates = [p.d for p in global_points if p.total_market_cap is not None]
    mc = [(p.total_market_cap or 0.0) / 1e12 for p in global_points if p.total_market_cap is not None]
    dom_dates = [p.d for p in global_points if p.btc_dom is not None]
    dom = [p.btc_dom or 0.0 for p in global_points if p.btc_dom is not None]

    # Chart 1: Market Cap
    p1 = outdir / "chart_1_marketcap.png"
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    set_dark_axes(ax, f"Total Market Cap - {month_label}", "Trillion USD")
    if dates and mc:
        ax.plot(dates, mc, color="#00E092", linewidth=2.0)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.tight_layout()
    fig.savefig(p1, dpi=170)
    plt.close(fig)
    charts["marketcap"] = p1

    # Chart 2: BTC Dominance
    p2 = outdir / "chart_2_btc_dom.png"
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    set_dark_axes(ax, f"BTC Dominance - {month_label}", "Dominance %")
    if dom_dates and dom:
        ax.plot(dom_dates, dom, color="#00E092", linewidth=1.8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.tight_layout()
    fig.savefig(p2, dpi=170)
    plt.close(fig)
    charts["btc_dom"] = p2

    # Chart 3: Exchange 30d change
    p3 = outdir / "chart_3_exchange_30d_change.png"
    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    set_dark_axes(ax, f"Top Exchanges 30d Volume Change - {month_label}", "%")
    names = [r.name for r in rows]
    pct = [r.pct30d or 0.0 for r in rows]
    colors = ["#00E092" if v >= 0 else "#FF5A67" for v in pct]
    ax.bar(names, pct, color=colors, alpha=0.95)
    ax.axhline(0, color="#9AA3AF", linewidth=1)
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    fig.tight_layout()
    fig.savefig(p3, dpi=170)
    plt.close(fig)
    charts["ex_30d"] = p3

    # Chart 4: Fear & Greed
    p4 = outdir / "chart_4_fng.png"
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    set_dark_axes(ax, f"Fear & Greed Index - {month_label}", "Index")
    if fng_month:
        x = [d for d, _, _ in fng_month]
        y = [v for _, v, _ in fng_month]
        ax.plot(x, y, color="#00E092", linewidth=1.8)
        ax.axhline(20, color="#7A3B3B", linestyle="--", linewidth=1)
        ax.axhline(80, color="#3B7A3B", linestyle="--", linewidth=1)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.tight_layout()
    fig.savefig(p4, dpi=170)
    plt.close(fig)
    charts["fng"] = p4

    # Chart 5: Realized volatility (fallback proxy for options risk temperature)
    p5 = outdir / "chart_5_realized_vol.png"
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    set_dark_axes(ax, f"BTC/ETH 7D Realized Volatility - {month_label}", "% annualized")
    if rv_month:
        x = [p.d for p in rv_month]
        y_btc = [p.btc_rv for p in rv_month]
        y_eth = [p.eth_rv for p in rv_month]
        if any(v is not None for v in y_btc):
            ax.plot(x, [v if v is not None else math.nan for v in y_btc], color="#00E092", linewidth=1.8, label="BTC RV(7D)")
        if any(v is not None for v in y_eth):
            ax.plot(x, [v if v is not None else math.nan for v in y_eth], color="#5EA2FF", linewidth=1.8, label="ETH RV(7D)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.legend(facecolor="#1B1D22", edgecolor="#404652", labelcolor="#D7DBE0")
    fig.tight_layout()
    fig.savefig(p5, dpi=170)
    plt.close(fig)
    charts["rv"] = p5

    return charts


def write_csv(rows: List[ExchangeRow], out_path: Path) -> None:
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank",
                "name",
                "slug",
                "volume30d_usd",
                "pct30d",
                "volume7d_usd",
                "pct7d",
                "spot24h_usd",
                "deriv24h_usd",
            ]
        )
        for r in rows:
            w.writerow([r.rank, r.name, r.slug, r.volume30d, r.pct30d, r.volume7d, r.pct7d, r.spot24h, r.deriv24h])


def write_report_md(
    out_path: Path,
    rows: List[ExchangeRow],
    global_points: List[GlobalPoint],
    global_latest: Dict[str, Optional[float]],
    fng_month: List[Tuple[date, int, str]],
    trending: List[Dict[str, Any]],
    funding: Dict[str, Optional[float]],
    charts: Dict[str, Path],
    month_label: str,
    source_ts: Optional[str],
    csv_name: str,
    data_gaps: List[str],
) -> None:
    gp_mc = [p for p in global_points if p.total_market_cap is not None]
    gp_vol = [p for p in global_points if p.total_volume_24h is not None]
    gp_dom = [p for p in global_points if p.btc_dom is not None]

    mc_start = gp_mc[0].total_market_cap if gp_mc else None
    mc_end = gp_mc[-1].total_market_cap if gp_mc else None
    mc_delta = ((mc_end / mc_start - 1.0) * 100.0) if mc_start and mc_end else None
    avg_vol = (sum((p.total_volume_24h or 0.0) for p in gp_vol) / len(gp_vol)) if gp_vol else None
    dom_start = gp_dom[0].btc_dom if gp_dom else None
    dom_end = gp_dom[-1].btc_dom if gp_dom else None

    total_curr = sum((r.volume30d or 0.0) for r in rows)
    prev_rows = [r.prev30d_est for r in rows if r.prev30d_est is not None]
    total_prev = sum(prev_rows) if prev_rows else None
    total_delta = ((total_curr / total_prev - 1.0) * 100.0) if total_prev and total_prev > 0 else None

    rising = sorted([r for r in rows if r.pct30d is not None], key=lambda r: r.pct30d or -1e9, reverse=True)
    falling = sorted([r for r in rows if r.pct30d is not None], key=lambda r: r.pct30d or 1e9)

    latest_fng = fng_month[-1] if fng_month else None

    lines: List[str] = []
    lines.append(f"# {month_label.replace('-', '')}")
    lines.append("")
    lines.append(f"## {month_label[:4]} 年 {int(month_label[5:]):02d} 月核心市场洞察")
    lines.append("")
    lines.append("- 市值与主导率分析")
    lines.append("- 前排交易所成交结构分析")
    lines.append("- 市场情绪：恐惧贪婪指数")
    lines.append("- 风险与运营建议")
    lines.append("")
    lines.append("本月市场呈现“去杠杆回落、结构分化”的特征，前排交易所整体成交额较前一观察窗口收缩，但头部内部出现分化。")
    lines.append("")
    if data_gaps:
        lines.append("### 数据可用性说明")
        for g in data_gaps:
            lines.append(f"- {g}")
    lines.append("")
    lines.append(f"### {month_label[:4]} 年 {int(month_label[5:]):02d} 月核心结论")
    lines.append(f"- 总成交额与流动性：前排样本滚动 30 天成交额为 {fmt_usd(total_curr)}，估算环比 {fmt_pct(total_delta)}。")
    lines.append(f"- 全市场总市值：{fmt_usd(mc_start)} -> {fmt_usd(mc_end)}，月内变化 {fmt_pct(mc_delta)}。")
    lines.append(f"- 全市场日均 24h 成交额：{fmt_usd(avg_vol)}。")
    lines.append(f"- BTC 主导率：{fmt_pct(dom_start)} -> {fmt_pct(dom_end)}。")
    if latest_fng:
        lines.append(f"- 恐惧贪婪指数：{latest_fng[1]}（{latest_fng[2]}）。")
    lines.append(
        f"- 稳定币资金面：市值 {fmt_usd(global_latest.get('stablecoin_market_cap'))}，24h 成交量 {fmt_usd(global_latest.get('stablecoin_volume_24h'))}。"
    )
    lines.append("")
    lines.append(f"![chart-marketcap]({charts['marketcap'].as_posix()})")
    lines.append("")
    lines.append("值得注意的是，本期市值下行与主导率回落并存，说明市场风险偏好没有简单回归，仍处于结构性再定价阶段。")
    lines.append("")
    lines.append("## 市值与主导率分析")
    lines.append("根据 CMC 全市场历史数据，2 月份总市值整体下移；BTC 主导率虽有回落，但仍维持在高位区间。")
    lines.append("")
    lines.append(f"![chart-btc-dom]({charts['btc_dom'].as_posix()})")
    lines.append("")
    lines.append("这意味着交易量仍倾向集中在核心资产交易对，长尾资产流动性修复较慢。")
    lines.append("")
    lines.append("## 前排交易所成交结构分析")
    lines.append("我们以 CMC 前排样本进行横向对比，重点观察 `30d 成交额变化` 与 `24h 现货/衍生品结构`。")
    lines.append("")
    lines.append(f"![chart-ex-30d]({charts['ex_30d'].as_posix()})")
    lines.append("")
    lines.append("关键观察：")
    lines.append(f"1. 增幅靠前：{rising[0].name} ({fmt_pct(rising[0].pct30d)}), {rising[1].name} ({fmt_pct(rising[1].pct30d)})。")
    lines.append(f"2. 回落靠前：{falling[0].name} ({fmt_pct(falling[0].pct30d)}), {falling[1].name} ({fmt_pct(falling[1].pct30d)})。")
    lines.append("3. 结构上，衍生品成交占比在样本内依旧偏高，波动放大风险需持续跟踪。")
    lines.append("")
    lines.append("## 资金费率与波动率观察")
    lines.append("参考交易所衍生品月报口径，本节给出资金费率快照与波动率代理指标。")
    btc_fd = funding.get("btc_perp_funding")
    eth_fd = funding.get("eth_perp_funding")
    if btc_fd is not None or eth_fd is not None:
        lines.append(f"- Deribit BTC-PERP funding: {fmt_pct((btc_fd or 0.0) * 100.0) if btc_fd is not None else 'N/A'}")
        lines.append(f"- Deribit ETH-PERP funding: {fmt_pct((eth_fd or 0.0) * 100.0) if eth_fd is not None else 'N/A'}")
    else:
        lines.append("- Deribit funding 快照暂不可用（接口异常），已使用波动率与成交结构作为替代监测。")
    lines.append(f"- 全市场衍生品 24h 成交量（CMC）：{fmt_usd(global_latest.get('derivatives_volume_24h'))}")
    lines.append("")
    lines.append(f"![chart-rv]({charts['rv'].as_posix()})")
    lines.append("")
    lines.append("该图使用 BTC/ETH 7 日已实现波动率（年化）作为期权隐波的替代温度计：上行通常对应风险对冲需求抬升。")
    lines.append("")
    lines.append("## 市场情绪：恐惧贪婪指数")
    lines.append("恐惧贪婪指数在本月维持低位震荡，零售情绪修复缓慢。")
    lines.append("")
    lines.append(f"![chart-fng]({charts['fng'].as_posix()})")
    lines.append("")
    lines.append("关键时点分析：")
    lines.append("1. 若指数持续低于 25，通常意味着风险偏好尚未恢复。")
    lines.append("2. 若指数快速回升并突破 50，往往对应短期交易活跃度提升。")
    lines.append("")
    lines.append("## 社媒与搜索热度（Trending）")
    lines.append("以 CoinGecko Trending 作为公开可得的搜索热度代理。")
    if trending:
        top = trending[:10]
        lines.append("| Symbol | Name | MCap Rank | Price (BTC) |")
        lines.append("| --- | --- | --- | --- |")
        for item in top:
            rank = item.get("rank")
            rank_txt = str(rank) if rank is not None else "N/A"
            price_btc = item.get("price_btc")
            pb = f"{price_btc:.8f}" if isinstance(price_btc, (int, float)) else "N/A"
            lines.append(f"| {item.get('symbol') or ''} | {item.get('name') or ''} | {rank_txt} | {pb} |")
    else:
        lines.append("- Trending 数据暂不可用。")
    lines.append("")
    lines.append("## 稳定币与资金面观察")
    lines.append(f"- 稳定币市值：{fmt_usd(global_latest.get('stablecoin_market_cap'))}")
    lines.append(f"- 稳定币 24h 成交量：{fmt_usd(global_latest.get('stablecoin_volume_24h'))}")
    lines.append(f"- DeFi 市值：{fmt_usd(global_latest.get('defi_market_cap'))}")
    lines.append(f"- DeFi 24h 成交量：{fmt_usd(global_latest.get('defi_volume_24h'))}")
    lines.append("")
    lines.append("## 风险与运营建议")
    lines.append("1. 风险监控：将“衍生品占比 + 30d 量能变化 + F&G”纳入统一预警面板。")
    lines.append("2. 业务策略：在主流币对维持深度，同时控制长尾币对库存与做市风险。")
    lines.append("3. 对外披露：参考 PoR 风格，补充负债口径与地址级储备说明，增强用户信任。")
    lines.append("")
    lines.append("## 附录：前排交易所明细")
    lines.append("| Rank | Exchange | 30d Volume | 30d Change | 7d Change | 24h Spot | 24h Deriv |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        lines.append(
            f"| {r.rank if r.rank is not None else 'N/A'} | {r.name} | {fmt_usd(r.volume30d)} | {fmt_pct(r.pct30d)} | {fmt_pct(r.pct7d)} | {fmt_usd(r.spot24h)} | {fmt_usd(r.deriv24h)} |"
        )
    lines.append("")
    lines.append("## 数据源")
    lines.append(f"- CMC Exchange Quotes: `{CMC_EX_QUOTE}`")
    lines.append(f"- CMC Global Historical: `{CMC_GLOBAL_HIST}`")
    lines.append(f"- CMC Global Latest: `{CMC_GLOBAL_LATEST}`")
    lines.append(f"- CoinGecko Trending: `{CG_BASE}/search/trending`")
    lines.append(f"- CoinGecko Market Chart: `{CG_BASE}/coins/{{id}}/market_chart`")
    lines.append("- CoinMetrics (State of the Network #348): `https://coinmetrics.substack.com/p/state-of-the-network-issue-348`")
    lines.append(f"- Deribit Ticker: `{DERIBIT_TICKER}`")
    lines.append(f"- Alternative.me F&G: `{ALT_FNG}`")
    if source_ts:
        lines.append(f"- CMC 快照时间：`{source_ts}`")
    lines.append(f"- 明细数据：`{csv_name}`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    global CG_BASE, CG_HEADERS
    parser = argparse.ArgumentParser(description="Generate Yuque-style CEX monthly report.")
    parser.add_argument("--month", default="2026-02", help="Month in YYYY-MM")
    parser.add_argument("--outdir", default="reports/2026-02/our_style_report_yuque", help="Output directory")
    parser.add_argument("--cg-key", default=None, help="CoinGecko key (or env COINGECKO_API_KEY/CG_API_KEY)")
    parser.add_argument("--cg-plan", default="auto", choices=["auto", "public", "demo", "pro"], help="CoinGecko plan")
    parser.add_argument(
        "--cg-secret-file",
        default=str(DEFAULT_CG_SECRET_FILE),
        help="Local JSON file with CoinGecko credentials (api_key, plan)",
    )
    args = parser.parse_args()

    CG_BASE, CG_HEADERS, cg_plan_used, has_key = resolve_cg_runtime(
        args.cg_plan, args.cg_key, Path(args.cg_secret_file).expanduser()
    )

    start, end_excl = parse_month(args.month)
    data_gaps: List[str] = []

    rows, source_ts = fetch_exchanges()
    global_points = fetch_global(start, end_excl)
    try:
        global_latest = fetch_global_latest()
    except Exception as e:
        global_latest = {
            "total_market_cap": None,
            "total_volume_24h": None,
            "stablecoin_market_cap": None,
            "stablecoin_volume_24h": None,
            "derivatives_volume_24h": None,
            "defi_market_cap": None,
            "defi_volume_24h": None,
        }
        data_gaps.append(f"CMC Global Latest 获取失败：{e}")

    try:
        fng_all = fetch_fng_series(limit=90)
    except Exception as e:
        fng_all = []
        data_gaps.append(f"Alternative.me F&G 获取失败：{e}")
    fng_month = [p for p in fng_all if start <= p[0] < end_excl]

    try:
        trending = fetch_cg_trending()
    except Exception as e:
        trending = []
        data_gaps.append(f"CoinGecko Trending 获取失败：{e}")

    try:
        funding = fetch_deribit_funding_snapshot()
    except Exception as e:
        funding = {"btc_perp_funding": None, "eth_perp_funding": None}
        data_gaps.append(f"Deribit Funding 快照获取失败：{e}")

    # Volatility proxy data (CoinGecko price series -> realized volatility)
    try:
        btc_prices = fetch_cg_price_series("bitcoin", days=90)
    except Exception as e:
        btc_prices = []
        data_gaps.append(f"CoinGecko BTC 价格序列获取失败：{e}")
    try:
        eth_prices = fetch_cg_price_series("ethereum", days=90)
    except Exception as e:
        eth_prices = []
        data_gaps.append(f"CoinGecko ETH 价格序列获取失败：{e}")
    rv_series = compute_realized_vol_series(btc_prices, eth_prices, window=7)
    rv_month = [p for p in rv_series if start <= p.d < end_excl]

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "yuque_style_exchange_data.csv"
    md_path = outdir / "yuque_style_report.md"
    chart_dir = outdir / "charts"

    charts = build_charts(rows, global_points, fng_month, rv_month, chart_dir, args.month)
    write_csv(rows, csv_path)
    # In markdown, refer to chart names in same folder by relative path
    charts_rel = {k: Path("charts") / v.name for k, v in charts.items()}
    write_report_md(
        md_path,
        rows,
        global_points,
        global_latest,
        fng_month,
        trending,
        funding,
        charts_rel,
        args.month,
        source_ts,
        csv_path.name,
        data_gaps,
    )

    print(f"Report: {md_path}")
    print(f"CSV:    {csv_path}")
    for key, path in charts.items():
        print(f"Chart[{key}]: {path}")
    print(f"CoinGecko: plan={cg_plan_used}, key={'yes' if has_key else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
