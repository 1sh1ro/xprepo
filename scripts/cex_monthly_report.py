#!/usr/bin/env python3
"""
Generate a CEX market monthly report using CoinMarketCap (CMC) and CoinGecko (CG).
Outputs a Markdown report and PNG charts.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Ensure matplotlib cache is writable
os.environ.setdefault("MPLCONFIGDIR", str(Path(os.environ.get("TMPDIR", "/tmp")) / "matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CMC_BASE = "https://pro-api.coinmarketcap.com/v1"
CG_PRO_BASE = "https://pro-api.coingecko.com/api/v3"
CG_PUBLIC_BASE = "https://api.coingecko.com/api/v3"


@dataclass
class FetchResult:
    data: Optional[Any]
    error: Optional[str]


@dataclass
class SeriesStats:
    start: Optional[float]
    end: Optional[float]
    change_abs: Optional[float]
    change_pct: Optional[float]
    avg: Optional[float]
    high: Optional[float]
    low: Optional[float]


def http_get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> FetchResult:
    if params:
        url = f"{url}?{urlencode(params)}"
    base_headers = {
        "User-Agent": "cex-monthly-report/1.0",
    }
    if headers:
        base_headers.update(headers)
    req = Request(url, headers=base_headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8", "ignore")
        except Exception:
            body = ""
        return FetchResult(None, f"HTTP {e.code}: {body[:300]}")
    except URLError as e:
        return FetchResult(None, f"URL error: {e}")
    except Exception as e:
        return FetchResult(None, f"Error: {e}")

    try:
        return FetchResult(json.loads(raw.decode("utf-8")), None)
    except Exception as e:
        return FetchResult(None, f"JSON parse error: {e}")


def last_full_month(today: Optional[date] = None) -> Tuple[date, date]:
    today = today or date.today()
    first_this_month = date(today.year, today.month, 1)
    last_prev = first_this_month - timedelta(days=1)
    first_prev = date(last_prev.year, last_prev.month, 1)
    return first_prev, last_prev


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def parse_month(s: str) -> Tuple[date, date]:
    dt = datetime.strptime(s, "%Y-%m")
    first = date(dt.year, dt.month, 1)
    # next month
    if dt.month == 12:
        first_next = date(dt.year + 1, 1, 1)
    else:
        first_next = date(dt.year, dt.month + 1, 1)
    last = first_next - timedelta(days=1)
    return first, last


def to_utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_ts_to_date(ts: str) -> Optional[date]:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts).date()
    except Exception:
        return None


def fmt_usd(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    neg = value < 0
    value = abs(value)
    if value >= 1e12:
        s = f"${value/1e12:.2f}T"
    elif value >= 1e9:
        s = f"${value/1e9:.2f}B"
    elif value >= 1e6:
        s = f"${value/1e6:.2f}M"
    else:
        s = f"${value:,.0f}"
    return f"-{s}" if neg else s


def fmt_pct(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def fmt_signed(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(value):.2f}%"


def series_stats(series: List[Tuple[date, float]]) -> SeriesStats:
    if not series:
        return SeriesStats(None, None, None, None, None, None, None)
    series = sorted(series, key=lambda x: x[0])
    vals = [v for _, v in series]
    start = vals[0]
    end = vals[-1]
    change_abs = end - start
    change_pct = (change_abs / start * 100.0) if start else None
    avg = sum(vals) / len(vals)
    high = max(vals)
    low = min(vals)
    return SeriesStats(start, end, change_abs, change_pct, avg, high, low)


def normalize_daily(points: List[Tuple[date, float]]) -> List[Tuple[date, float]]:
    daily: Dict[date, float] = {}
    for d, v in points:
        daily[d] = v
    return sorted(daily.items(), key=lambda x: x[0])


def filter_range(series: List[Tuple[date, float]], start: date, end: date) -> List[Tuple[date, float]]:
    return [(d, v) for d, v in series if start <= d <= end]


def cmc_headers(api_key: str) -> Dict[str, str]:
    return {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }


def cg_headers(api_key: Optional[str], plan: str) -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if not api_key or plan == "public":
        return headers
    if plan == "pro":
        headers["x-cg-pro-api-key"] = api_key
    elif plan == "demo":
        headers["x-cg-demo-api-key"] = api_key
    return headers


def fetch_cmc_latest(api_key: str) -> FetchResult:
    return http_get_json(f"{CMC_BASE}/global-metrics/quotes/latest", headers=cmc_headers(api_key))


def fetch_cmc_historical(api_key: str, start: date, end: date) -> FetchResult:
    start_dt = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
    end_dt = datetime.combine(end, datetime.max.time(), tzinfo=timezone.utc)
    params = {
        "time_start": to_utc_iso(start_dt),
        "time_end": to_utc_iso(end_dt),
        "interval": "1d",
    }
    return http_get_json(f"{CMC_BASE}/global-metrics/quotes/historical", params=params, headers=cmc_headers(api_key))


def cg_request(path: str, params: Dict[str, Any], api_key: Optional[str], plan: str) -> FetchResult:
    base = CG_PRO_BASE if plan == "pro" else CG_PUBLIC_BASE
    return http_get_json(f"{base}{path}", params=params, headers=cg_headers(api_key, plan))


def fetch_cg_market_cap_chart(api_key: Optional[str], start: date, plan: str) -> FetchResult:
    today = date.today()
    days = max(1, (today - start).days + 2)
    params = {
        "vs_currency": "usd",
        "days": str(days),
    }
    return cg_request("/global/market_cap_chart", params=params, api_key=api_key, plan=plan)


def fetch_cg_categories(api_key: Optional[str], plan: str) -> FetchResult:
    params: Dict[str, Any] = {}
    return cg_request("/coins/categories", params=params, api_key=api_key, plan=plan)


def fetch_cg_global(api_key: Optional[str], plan: str) -> FetchResult:
    params: Dict[str, Any] = {}
    return cg_request("/global", params=params, api_key=api_key, plan=plan)


def extract_cmc_latest(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return {}
    d = data.get("data", {}) if isinstance(data.get("data", {}), dict) else {}
    quote = d.get("quote", {}).get("USD", {}) if isinstance(d.get("quote", {}), dict) else {}

    def pick(*keys: str) -> Optional[float]:
        for k in keys:
            if k in d and isinstance(d[k], (int, float)):
                return float(d[k])
            if k in quote and isinstance(quote[k], (int, float)):
                return float(quote[k])
        return None

    return {
        "total_market_cap": pick("total_market_cap"),
        "total_volume_24h": pick("total_volume_24h", "total_volume_24h_reported"),
        "btc_dominance": pick("btc_dominance"),
        "eth_dominance": pick("eth_dominance"),
        "active_cryptocurrencies": d.get("active_cryptocurrencies"),
        "active_exchanges": d.get("active_exchanges"),
        "active_market_pairs": d.get("active_market_pairs"),
        "defi_market_cap": d.get("defi_market_cap"),
        "defi_volume_24h": d.get("defi_volume_24h"),
        "stablecoin_market_cap": d.get("stablecoin_market_cap"),
        "stablecoin_volume_24h": d.get("stablecoin_volume_24h"),
        "derivatives_volume_24h": d.get("derivatives_volume_24h"),
        "last_updated": d.get("last_updated") or data.get("status", {}).get("timestamp"),
    }


def extract_cmc_historical(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    raw = data.get("data")
    if isinstance(raw, dict):
        raw = raw.get("quotes")
    if not isinstance(raw, list):
        return []

    out: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        ts = item.get("timestamp") or item.get("time_open") or item.get("time_close")
        d = parse_ts_to_date(ts) if isinstance(ts, str) else None
        quote = item.get("quote", {}).get("USD", {}) if isinstance(item.get("quote", {}), dict) else {}
        def pick(*keys: str) -> Optional[float]:
            for k in keys:
                if k in item and isinstance(item[k], (int, float)):
                    return float(item[k])
                if k in quote and isinstance(quote[k], (int, float)):
                    return float(quote[k])
            return None

        out.append({
            "date": d,
            "total_market_cap": pick("total_market_cap"),
            "total_volume_24h": pick("total_volume_24h", "total_volume_24h_reported"),
            "btc_dominance": pick("btc_dominance"),
        })
    return [x for x in out if x.get("date")]


def extract_cg_market_cap_chart(data: Any) -> Tuple[List[Tuple[date, float]], List[Tuple[date, float]]]:
    if not isinstance(data, dict):
        return [], []
    mc = []
    vol = []
    mc_container = data.get("market_cap_chart")
    if isinstance(mc_container, dict):
        mc = mc_container.get("market_cap") or mc_container.get("market_caps") or []
        vol = mc_container.get("volume") or mc_container.get("total_volumes") or []
    elif isinstance(mc_container, list):
        mc = mc_container
    if not mc:
        mc = data.get("market_caps") or []
    if not vol:
        vol = data.get("volume_chart") or data.get("total_volumes") or []

    def parse_points(points: Any) -> List[Tuple[date, float]]:
        out: List[Tuple[date, float]] = []
        if not isinstance(points, list):
            return out
        for p in points:
            if not isinstance(p, list) or len(p) < 2:
                continue
            ts, val = p[0], p[1]
            if not isinstance(ts, (int, float)) or not isinstance(val, (int, float)):
                continue
            d = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).date()
            out.append((d, float(val)))
        return out

    return parse_points(mc), parse_points(vol)


def extract_cg_categories(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        out.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "market_cap": item.get("market_cap"),
            "market_cap_change_24h": item.get("market_cap_change_24h"),
            "volume_24h": item.get("volume_24h"),
            "top_3_coins": item.get("top_3_coins"),
            "top_3_coin_symbols": item.get("top_3_coin_symbols"),
            "updated_at": item.get("updated_at"),
        })
    return out


def extract_cg_global(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return {}
    payload = data.get("data") if isinstance(data.get("data"), dict) else data
    mcp = payload.get("market_cap_percentage") if isinstance(payload.get("market_cap_percentage"), dict) else {}
    out: Dict[str, Any] = {}
    if isinstance(mcp, dict):
        if "btc" in mcp and isinstance(mcp.get("btc"), (int, float)):
            out["btc_dominance"] = float(mcp.get("btc"))
        if "eth" in mcp and isinstance(mcp.get("eth"), (int, float)):
            out["eth_dominance"] = float(mcp.get("eth"))
    total_mc = payload.get("total_market_cap") if isinstance(payload.get("total_market_cap"), dict) else {}
    total_vol = payload.get("total_volume") if isinstance(payload.get("total_volume"), dict) else {}
    if isinstance(total_mc, dict) and isinstance(total_mc.get("usd"), (int, float)):
        out["total_market_cap"] = float(total_mc.get("usd"))
    if isinstance(total_vol, dict) and isinstance(total_vol.get("usd"), (int, float)):
        out["total_volume_24h"] = float(total_vol.get("usd"))
    return out


def plot_charts(
    out_path: Path,
    market_cap_series: List[Tuple[date, float]],
    volume_series: List[Tuple[date, float]],
    btc_dom_series: List[Tuple[date, float]],
    categories: List[Dict[str, Any]],
    month_label: str,
) -> None:
    plots: List[str] = []
    if market_cap_series and volume_series:
        plots.append("market")
    if btc_dom_series:
        plots.append("btc_dom")
    if categories:
        plots.append("categories")
    if not plots:
        return

    nrows = len(plots)
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(12, 4 * nrows))
    if nrows == 1:
        axes = [axes]

    ax_index = 0
    if "market" in plots:
        ax = axes[ax_index]
        ax_index += 1
        dates = [d for d, _ in market_cap_series]
        mc = [v / 1e12 for _, v in market_cap_series]
        vol = [v / 1e9 for _, v in volume_series]
        ax.plot(dates, mc, label="Total Market Cap (T USD)", color="#1f77b4")
        ax.set_ylabel("T USD")
        ax2 = ax.twinx()
        ax2.plot(dates, vol, label="24h Volume (B USD)", color="#ff7f0e", alpha=0.7)
        ax2.set_ylabel("B USD")
        ax.set_title(f"Total Market Cap & 24h Volume ({month_label})")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment("right")

    if "btc_dom" in plots:
        ax = axes[ax_index]
        ax_index += 1
        dates = [d for d, _ in btc_dom_series]
        dom = [v for _, v in btc_dom_series]
        ax.plot(dates, dom, label="BTC Dominance (%)", color="#2ca02c")
        ax.set_ylabel("%")
        ax.set_title(f"BTC Dominance ({month_label})")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment("right")

    if "categories" in plots:
        ax = axes[ax_index]
        cats = sorted(categories, key=lambda x: (x.get("market_cap") or 0), reverse=True)[:10]
        names = [c.get("name") or c.get("id") or "" for c in cats]
        vals = [(c.get("market_cap") or 0) / 1e9 for c in cats]
        changes = [c.get("market_cap_change_24h") for c in cats]
        colors = ["#2ca02c" if (ch is not None and ch >= 0) else "#d62728" for ch in changes]
        ax.barh(names, vals, color=colors)
        ax.set_xlabel("Market Cap (B USD)")
        ax.set_title("Top Categories by Market Cap (Color = 24h Change)")
        ax.invert_yaxis()
        ax.grid(True, axis="x", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def build_report(
    out_path: Path,
    chart_path: Optional[Path],
    month_label: str,
    date_range: Tuple[date, date],
    market_cap_stats: Optional[SeriesStats],
    volume_stats: Optional[SeriesStats],
    btc_dom_stats: Optional[SeriesStats],
    cmc_latest: Dict[str, Any],
    categories: List[Dict[str, Any]],
    data_gaps: List[str],
    btc_dom_current: Optional[float],
    btc_dom_source: Optional[str],
) -> None:
    start, end = date_range
    lines: List[str] = []
    lines.append(f"# 二级市场月度报告（CEX 市场结构 & 板块热点）")
    lines.append("")
    lines.append(f"- 月份：{month_label}（UTC）")
    lines.append(f"- 覆盖区间：{start.isoformat()} 至 {end.isoformat()}")
    lines.append(f"- 生成时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}")
    lines.append("")

    if data_gaps:
        lines.append("## 数据可用性说明")
        for gap in data_gaps:
            lines.append(f"- {gap}")
        lines.append("")

    lines.append("## 关键结论")
    if market_cap_stats and market_cap_stats.start is not None:
        lines.append(
            f"- 总市值：{fmt_usd(market_cap_stats.start)} → {fmt_usd(market_cap_stats.end)}，月度变动 {fmt_usd(market_cap_stats.change_abs)}（{fmt_signed(market_cap_stats.change_pct)}）"
        )
    else:
        lines.append("- 总市值：N/A（缺少月度序列）")

    if volume_stats and volume_stats.avg is not None:
        lines.append(
            f"- 24h 成交量：月均 {fmt_usd(volume_stats.avg)}，区间 {fmt_usd(volume_stats.low)} ~ {fmt_usd(volume_stats.high)}"
        )
    else:
        lines.append("- 24h 成交量：N/A（缺少月度序列）")

    if btc_dom_stats and btc_dom_stats.start is not None:
        lines.append(
            f"- BTC 统治力：{fmt_pct(btc_dom_stats.start)} → {fmt_pct(btc_dom_stats.end)}，变动 {fmt_signed(btc_dom_stats.change_pct)}"
        )
    elif btc_dom_current is not None:
        suffix = f"（当前值，来源 {btc_dom_source}）" if btc_dom_source else "（当前值）"
        lines.append(f"- BTC 统治力：{fmt_pct(btc_dom_current)}{suffix}")
    else:
        lines.append("- BTC 统治力：N/A")
    lines.append("")

    lines.append("## 市场结构（CMC / CG）")
    lines.append("| 指标 | 起点 | 终点 | 变化 | 备注 |")
    lines.append("| --- | --- | --- | --- | --- |")
    if market_cap_stats and market_cap_stats.start is not None:
        lines.append(
            f"| 总市值 | {fmt_usd(market_cap_stats.start)} | {fmt_usd(market_cap_stats.end)} | {fmt_signed(market_cap_stats.change_pct)} | 月内高/低：{fmt_usd(market_cap_stats.high)} / {fmt_usd(market_cap_stats.low)} |"
        )
    else:
        lines.append("| 总市值 | N/A | N/A | N/A | 月度序列不可用 |")

    if volume_stats and volume_stats.avg is not None:
        lines.append(
            f"| 24h 成交量 | N/A | N/A | N/A | 月均 {fmt_usd(volume_stats.avg)}；高/低 {fmt_usd(volume_stats.high)} / {fmt_usd(volume_stats.low)} |"
        )
    else:
        lines.append("| 24h 成交量 | N/A | N/A | N/A | 月度序列不可用 |")

    if btc_dom_stats and btc_dom_stats.start is not None:
        lines.append(
            f"| BTC 统治力 | {fmt_pct(btc_dom_stats.start)} | {fmt_pct(btc_dom_stats.end)} | {fmt_signed(btc_dom_stats.change_pct)} | 月内高/低：{fmt_pct(btc_dom_stats.high)} / {fmt_pct(btc_dom_stats.low)} |"
        )
    elif btc_dom_current is not None:
        src = btc_dom_source or "当前值"
        lines.append(f"| BTC 统治力 | N/A | {fmt_pct(btc_dom_current)} | N/A | {src} |")
    else:
        lines.append("| BTC 统治力 | N/A | N/A | N/A | 不可用 |")

    # Extra CMC latest metrics
    lines.append("")
    lines.append("### 其他可用指标（CMC 全局指标）")
    extra_rows = []
    for key, label in [
        ("active_cryptocurrencies", "活跃币种数"),
        ("active_exchanges", "活跃交易所数"),
        ("active_market_pairs", "活跃交易对数"),
        ("defi_market_cap", "DeFi 市值"),
        ("defi_volume_24h", "DeFi 24h 成交量"),
        ("stablecoin_market_cap", "稳定币市值"),
        ("stablecoin_volume_24h", "稳定币 24h 成交量"),
        ("derivatives_volume_24h", "衍生品 24h 成交量"),
        ("eth_dominance", "ETH 统治力"),
    ]:
        val = cmc_latest.get(key)
        if val is None:
            continue
        if isinstance(val, (int, float)) and "dominance" in key:
            extra_rows.append((label, fmt_pct(float(val))))
        elif isinstance(val, (int, float)) and ("cap" in key or "volume" in key):
            extra_rows.append((label, fmt_usd(float(val))))
        else:
            extra_rows.append((label, str(val)))

    if extra_rows:
        lines.append("| 指标 | 当前值 |")
        lines.append("| --- | --- |")
        for label, val in extra_rows:
            lines.append(f"| {label} | {val} |")
    else:
        lines.append("- 无（CMC 最新数据不可用）")

    lines.append("")
    lines.append("## 板块热点（CoinGecko Categories）")
    if categories:
        top_cap = sorted(categories, key=lambda x: (x.get("market_cap") or 0), reverse=True)[:10]
        top_change = sorted(categories, key=lambda x: (x.get("market_cap_change_24h") or -1e9), reverse=True)[:10]

        lines.append("### 市值 Top 10")
        lines.append("| 板块 | 市值 | 24h 变化 | 24h 成交量 |")
        lines.append("| --- | --- | --- | --- |")
        for c in top_cap:
            lines.append(
                f"| {c.get('name') or c.get('id')} | {fmt_usd(c.get('market_cap'))} | {fmt_pct(c.get('market_cap_change_24h'))} | {fmt_usd(c.get('volume_24h'))} |"
            )

        lines.append("")
        lines.append("### 24h 涨幅 Top 10")
        lines.append("| 板块 | 24h 变化 | 市值 | 24h 成交量 |")
        lines.append("| --- | --- | --- | --- |")
        for c in top_change:
            lines.append(
                f"| {c.get('name') or c.get('id')} | {fmt_pct(c.get('market_cap_change_24h'))} | {fmt_usd(c.get('market_cap'))} | {fmt_usd(c.get('volume_24h'))} |"
            )
    else:
        lines.append("- 板块数据不可用")

    if chart_path is not None:
        lines.append("")
        lines.append("## 图表")
        lines.append(f"![cex-monthly-charts]({chart_path.name})")

    lines.append("")
    lines.append("## 可获取数据字段（按来源）")
    lines.append("### CoinMarketCap Global Metrics")
    lines.append("- 总市值（total_market_cap）")
    lines.append("- 24h 成交量（total_volume_24h）")
    lines.append("- BTC/ETH 统治力（btc_dominance / eth_dominance）")
    lines.append("- 活跃币种数、交易所数、交易对数")
    lines.append("- 稳定币/DeFi 市值与 24h 成交量")
    lines.append("- 衍生品 24h 成交量")
    lines.append("")
    lines.append("### CoinGecko Global & Categories")
    lines.append("- 全市场市值与成交量时间序列（market_cap_chart / volume_chart）")
    lines.append("- 全市场当前指标（total_market_cap / total_volume / market_cap_percentage）")
    lines.append("- 板块列表与市值、24h 变化、24h 成交量、Top3 币种")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CEX monthly report using CMC & CG data.")
    parser.add_argument("--month", help="Target month in YYYY-MM")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--cmc-key", help="CMC API key (or env CMC_API_KEY/CMC_PRO_API_KEY)")
    parser.add_argument("--cg-key", help="CoinGecko API key (or env COINGECKO_API_KEY/CG_API_KEY)")
    parser.add_argument("--cg-plan", choices=["pro", "demo", "public"], help="CoinGecko plan (pro/demo/public)")
    parser.add_argument("--outdir", default="reports", help="Output directory")
    args = parser.parse_args()

    if args.start and args.end:
        start = parse_date(args.start)
        end = parse_date(args.end)
    elif args.month:
        start, end = parse_month(args.month)
    else:
        start, end = last_full_month()

    if start > end:
        print("Start date must be <= end date", file=sys.stderr)
        return 2

    month_label = f"{start.strftime('%Y-%m')}"
    outdir = Path(args.outdir) / month_label
    outdir.mkdir(parents=True, exist_ok=True)

    cmc_key = args.cmc_key or os.getenv("CMC_API_KEY") or os.getenv("CMC_PRO_API_KEY")
    cg_key = args.cg_key or os.getenv("COINGECKO_API_KEY") or os.getenv("CG_API_KEY")
    cg_plan = args.cg_plan or os.getenv("COINGECKO_API_PLAN") or os.getenv("CG_PLAN")

    data_gaps: List[str] = []

    cmc_latest: Dict[str, Any] = {}
    cmc_hist_series: List[Dict[str, Any]] = []
    if cmc_key:
        latest_res = fetch_cmc_latest(cmc_key)
        if latest_res.error:
            data_gaps.append(f"CMC 最新全局指标获取失败：{latest_res.error}")
        else:
            cmc_latest = extract_cmc_latest(latest_res.data)

        hist_res = fetch_cmc_historical(cmc_key, start, end)
        if hist_res.error:
            data_gaps.append(f"CMC 历史全局指标获取失败：{hist_res.error}")
        else:
            cmc_hist_series = extract_cmc_historical(hist_res.data)
            if not cmc_hist_series:
                data_gaps.append("CMC 历史全局指标返回为空（可能是权限或区间问题）")
    else:
        data_gaps.append("未提供 CMC API Key，CMC 数据不可用")

    cg_market_cap_series: List[Tuple[date, float]] = []
    cg_volume_series: List[Tuple[date, float]] = []
    cg_categories: List[Dict[str, Any]] = []
    cg_global: Dict[str, Any] = {}

    if cg_plan in ("pro", "demo") and not cg_key:
        data_gaps.append(f"CoinGecko 指定了 {cg_plan} 计划但未提供 API Key，已回退 public")
        cg_plan = "public"

    if cg_plan:
        cg_plans = [cg_plan]
    else:
        cg_plans = ["pro", "demo", "public"] if cg_key else ["public"]

    def try_cg(fetch_fn, label: str):
        last_error = None
        for plan in cg_plans:
            key = cg_key if plan in ("pro", "demo") else None
            res = fetch_fn(key, plan)
            if res.error:
                last_error = res.error
                if cg_plan:
                    break
                continue
            return res, plan, None
        return None, None, last_error

    cg_res, _, err = try_cg(lambda key, plan: fetch_cg_market_cap_chart(key, start, plan), "market_cap_chart")
    if err:
        data_gaps.append(f"CoinGecko 市值/成交量时间序列获取失败：{err}")
    elif cg_res:
        mc, vol = extract_cg_market_cap_chart(cg_res.data)
        cg_market_cap_series = mc
        cg_volume_series = vol

    cat_res, _, err = try_cg(lambda key, plan: fetch_cg_categories(key, plan), "categories")
    if err:
        data_gaps.append(f"CoinGecko 板块分类获取失败：{err}")
    elif cat_res:
        cg_categories = extract_cg_categories(cat_res.data)

    cg_global_res, _, err = try_cg(lambda key, plan: fetch_cg_global(key, plan), "global")
    if err:
        data_gaps.append(f"CoinGecko Global 获取失败：{err}")
    elif cg_global_res:
        cg_global = extract_cg_global(cg_global_res.data)

    # Build series from CMC history if available
    market_cap_series: List[Tuple[date, float]] = []
    volume_series: List[Tuple[date, float]] = []
    btc_dom_series: List[Tuple[date, float]] = []

    if cmc_hist_series:
        market_cap_series = [(x["date"], x["total_market_cap"]) for x in cmc_hist_series if x.get("total_market_cap") is not None]
        volume_series = [(x["date"], x["total_volume_24h"]) for x in cmc_hist_series if x.get("total_volume_24h") is not None]
        btc_dom_series = [(x["date"], x["btc_dominance"]) for x in cmc_hist_series if x.get("btc_dominance") is not None]
    else:
        # fallback to CoinGecko for market cap & volume
        market_cap_series = cg_market_cap_series
        volume_series = cg_volume_series

    market_cap_series = filter_range(normalize_daily(market_cap_series), start, end)
    volume_series = filter_range(normalize_daily(volume_series), start, end)
    btc_dom_series = filter_range(normalize_daily(btc_dom_series), start, end)

    market_cap_stats = series_stats(market_cap_series) if market_cap_series else None
    volume_stats = series_stats(volume_series) if volume_series else None
    btc_dom_stats = series_stats(btc_dom_series) if btc_dom_series else None

    btc_dom_current = cmc_latest.get("btc_dominance")
    btc_dom_source = "CMC Global"
    if btc_dom_current is None and cg_global.get("btc_dominance") is not None:
        btc_dom_current = cg_global.get("btc_dominance")
        btc_dom_source = "CoinGecko Global"

    chart_path = outdir / "cex_monthly_charts.png"
    plot_charts(
        chart_path,
        market_cap_series,
        volume_series,
        btc_dom_series,
        cg_categories,
        month_label,
    )

    report_path = outdir / "cex_monthly_report.md"
    build_report(
        report_path,
        chart_path if chart_path.exists() else None,
        month_label,
        (start, end),
        market_cap_stats,
        volume_stats,
        btc_dom_stats,
        cmc_latest,
        cg_categories,
        data_gaps,
        btc_dom_current,
        btc_dom_source,
    )

    print(f"Report written to: {report_path}")
    if chart_path.exists():
        print(f"Chart written to: {chart_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
