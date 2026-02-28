#!/usr/bin/env python3
"""
CEX market report agent.
Generates daily and monthly reports with HTML + PDF outputs and PNG charts.
Data sources: CoinMarketCap, CoinGecko, Deribit (public JSON-RPC).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Matplotlib cache should be writable
os.environ.setdefault("MPLCONFIGDIR", str(Path(os.environ.get("TMPDIR", "/tmp")) / "matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

CMC_BASE = "https://pro-api.coinmarketcap.com/v1"
CG_PRO_BASE = "https://pro-api.coingecko.com/api/v3"
CG_PUBLIC_BASE = "https://api.coingecko.com/api/v3"
DERIBIT_BASE = "https://www.deribit.com/api/v2"


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
        "User-Agent": "cex-report-agent/1.0",
        "Accept": "application/json",
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


def http_post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> FetchResult:
    base_headers = {
        "User-Agent": "cex-report-agent/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if headers:
        base_headers.update(headers)
    body = json.dumps(payload).encode("utf-8")
    req = Request(url, data=body, headers=base_headers, method="POST")
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


def to_epoch_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


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


def safe_float(v: Any) -> Optional[float]:
    try:
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str) and v.strip():
            return float(v)
    except Exception:
        return None
    return None


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


def last_full_month(today: Optional[date] = None) -> Tuple[date, date]:
    today = today or date.today()
    first_this_month = date(today.year, today.month, 1)
    last_prev = first_this_month - timedelta(days=1)
    first_prev = date(last_prev.year, last_prev.month, 1)
    return first_prev, last_prev


def last_full_day(today: Optional[date] = None) -> date:
    today = today or date.today()
    return today - timedelta(days=1)


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def parse_month(s: str) -> Tuple[date, date]:
    dt = datetime.strptime(s, "%Y-%m")
    first = date(dt.year, dt.month, 1)
    if dt.month == 12:
        first_next = date(dt.year + 1, 1, 1)
    else:
        first_next = date(dt.year, dt.month + 1, 1)
    last = first_next - timedelta(days=1)
    return first, last


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
    return cg_request("/coins/categories", params={}, api_key=api_key, plan=plan)


def fetch_cg_global(api_key: Optional[str], plan: str) -> FetchResult:
    return cg_request("/global", params={}, api_key=api_key, plan=plan)


def fetch_cg_markets(api_key: Optional[str], plan: str, per_page: int = 20, page: int = 1) -> FetchResult:
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": str(per_page),
        "page": str(page),
        "sparkline": "false",
    }
    return cg_request("/coins/markets", params=params, api_key=api_key, plan=plan)


def fetch_cg_trending(api_key: Optional[str], plan: str) -> FetchResult:
    return cg_request("/search/trending", params={}, api_key=api_key, plan=plan)


def fetch_cg_derivatives_exchanges(api_key: Optional[str], plan: str) -> FetchResult:
    return cg_request("/derivatives/exchanges", params={}, api_key=api_key, plan=plan)


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


def extract_cg_markets(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        out.append({
            "id": item.get("id"),
            "symbol": item.get("symbol"),
            "name": item.get("name"),
            "current_price": safe_float(item.get("current_price")),
            "market_cap": safe_float(item.get("market_cap")),
            "market_cap_rank": item.get("market_cap_rank"),
            "total_volume": safe_float(item.get("total_volume")),
            "price_change_percentage_24h": safe_float(item.get("price_change_percentage_24h")),
        })
    return out


def extract_cg_trending(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    coins = data.get("coins")
    if not isinstance(coins, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in coins:
        payload = item.get("item") if isinstance(item, dict) else None
        if not isinstance(payload, dict):
            continue
        out.append({
            "id": payload.get("id"),
            "coin_id": payload.get("coin_id"),
            "name": payload.get("name"),
            "symbol": payload.get("symbol"),
            "market_cap_rank": payload.get("market_cap_rank"),
            "price_btc": safe_float(payload.get("price_btc")),
            "score": payload.get("score"),
        })
    return out


def extract_cg_derivatives_exchanges(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        out.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "open_interest_btc": safe_float(item.get("open_interest_btc")),
            "trade_volume_24h_btc": safe_float(item.get("trade_volume_24h_btc")),
            "number_of_perpetual_pairs": item.get("number_of_perpetual_pairs"),
            "number_of_futures_pairs": item.get("number_of_futures_pairs"),
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
    if isinstance(payload.get("active_cryptocurrencies"), int):
        out["active_cryptocurrencies"] = payload.get("active_cryptocurrencies")
    if isinstance(payload.get("markets"), int):
        out["markets"] = payload.get("markets")
    out["market_cap_change_percentage_24h_usd"] = safe_float(payload.get("market_cap_change_percentage_24h_usd"))
    out["volume_change_percentage_24h_usd"] = safe_float(payload.get("volume_change_percentage_24h_usd"))
    return out


# Deribit JSON-RPC

def deribit_rpc(method: str, params: Optional[Dict[str, Any]] = None, base_url: Optional[str] = None) -> FetchResult:
    url = base_url or DERIBIT_BASE
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1_000_000_000,
        "method": method,
        "params": params or {},
    }
    res = http_post_json(url, payload)
    if res.error:
        return res
    if not isinstance(res.data, dict):
        return FetchResult(None, "Deribit response not a dict")
    if "error" in res.data:
        return FetchResult(None, f"Deribit RPC error: {res.data.get('error')}")
    return FetchResult(res.data.get("result"), None)


def deribit_get_ticker(instrument_name: str, base_url: Optional[str] = None) -> FetchResult:
    return deribit_rpc("public/ticker", {"instrument_name": instrument_name}, base_url)


def deribit_get_book_summary_by_currency(currency: str, kind: str, base_url: Optional[str] = None) -> FetchResult:
    return deribit_rpc("public/get_book_summary_by_currency", {"currency": currency, "kind": kind}, base_url)


def deribit_get_instruments(currency: str, kind: str, expired: bool = False, base_url: Optional[str] = None) -> FetchResult:
    return deribit_rpc("public/get_instruments", {"currency": currency, "kind": kind, "expired": expired}, base_url)


def deribit_get_vol_index(currency: str, start: datetime, end: datetime, resolution: int = 3600, base_url: Optional[str] = None) -> FetchResult:
    params = {
        "currency": currency,
        "start_timestamp": to_epoch_ms(start),
        "end_timestamp": to_epoch_ms(end),
        "resolution": str(resolution),
    }
    return deribit_rpc("public/get_volatility_index_data", params, base_url)


def extract_deribit_dvol_series(data: Any) -> List[Tuple[date, float]]:
    if not isinstance(data, dict):
        return []
    raw = data.get("data")
    if not isinstance(raw, list):
        return []
    out: List[Tuple[date, float]] = []
    for item in raw:
        if not isinstance(item, list) or len(item) < 5:
            continue
        ts, _open, _high, _low, close = item[:5]
        if not isinstance(ts, (int, float)) or not isinstance(close, (int, float)):
            continue
        d = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).date()
        out.append((d, float(close)))
    return out


def extract_deribit_ticker(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return {}
    stats = data.get("stats") if isinstance(data.get("stats"), dict) else {}
    return {
        "instrument_name": data.get("instrument_name"),
        "open_interest": safe_float(data.get("open_interest")),
        "volume": safe_float(stats.get("volume")),
        "volume_usd": safe_float(stats.get("volume_usd")),
        "funding_8h": safe_float(data.get("funding_8h")),
        "current_funding": safe_float(data.get("current_funding")),
        "mark_price": safe_float(data.get("mark_price")),
        "index_price": safe_float(data.get("index_price")),
        "last_price": safe_float(data.get("last_price")),
    }


def aggregate_deribit_summary(data: Any) -> Dict[str, Optional[float]]:
    if not isinstance(data, list):
        return {"open_interest": None, "volume_usd": None}
    total_oi = 0.0
    total_vol = 0.0
    has_oi = False
    has_vol = False
    for item in data:
        if not isinstance(item, dict):
            continue
        oi = safe_float(item.get("open_interest"))
        vol = safe_float(item.get("volume_usd"))
        if oi is not None:
            total_oi += oi
            has_oi = True
        if vol is not None:
            total_vol += vol
            has_vol = True
    return {
        "open_interest": total_oi if has_oi else None,
        "volume_usd": total_vol if has_vol else None,
    }


def apply_dark_theme() -> None:
    plt.rcParams.update({
        "figure.facecolor": "#0f1115",
        "axes.facecolor": "#0f1115",
        "savefig.facecolor": "#0f1115",
        "text.color": "#d8dee9",
        "axes.labelcolor": "#d8dee9",
        "xtick.color": "#9aa4b2",
        "ytick.color": "#9aa4b2",
        "grid.color": "#2a2f3a",
        "axes.edgecolor": "#2a2f3a",
        "font.size": 10,
    })


def plot_line(series: List[Tuple[date, float]], title: str, ylabel: str, out_path: Path, color: str = "#00d084") -> None:
    if not series:
        return
    apply_dark_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    dates = [d for d, _ in series]
    vals = [v for _, v in series]
    ax.plot(dates, vals, color=color, linewidth=2)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_dual_line(series_a: List[Tuple[date, float]], series_b: List[Tuple[date, float]], labels: Tuple[str, str], title: str, ylabel: str, out_path: Path) -> None:
    if not series_a and not series_b:
        return
    apply_dark_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    if series_a:
        dates = [d for d, _ in series_a]
        vals = [v for _, v in series_a]
        ax.plot(dates, vals, color="#6d9eff", linewidth=2, label=labels[0])
    if series_b:
        dates = [d for d, _ in series_b]
        vals = [v for _, v in series_b]
        ax.plot(dates, vals, color="#b183ff", linewidth=2, label=labels[1])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_market_cap_volume(series_mc: List[Tuple[date, float]], series_vol: List[Tuple[date, float]], title: str, out_path: Path) -> None:
    if not series_mc and not series_vol:
        return
    apply_dark_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    if series_mc:
        dates = [d for d, _ in series_mc]
        mc = [v / 1e12 for _, v in series_mc]
        ax.plot(dates, mc, label="Total Market Cap (T USD)", color="#00d084", linewidth=2)
        ax.set_ylabel("T USD")
    if series_vol:
        ax2 = ax.twinx()
        dates = [d for d, _ in series_vol]
        vol = [v / 1e9 for _, v in series_vol]
        ax2.plot(dates, vol, label="24h Volume (B USD)", color="#ffb86b", linewidth=1.8, alpha=0.85)
        ax2.set_ylabel("B USD")
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_categories(categories: List[Dict[str, Any]], out_path: Path, title: str) -> None:
    if not categories:
        return
    apply_dark_theme()
    cats = sorted(categories, key=lambda x: (x.get("market_cap") or 0), reverse=True)[:10]
    names = [c.get("name") or c.get("id") or "" for c in cats]
    vals = [(c.get("market_cap") or 0) / 1e9 for c in cats]
    changes = [c.get("market_cap_change_24h") for c in cats]
    colors_ = ["#00d084" if (ch is not None and ch >= 0) else "#ff6b6b" for ch in changes]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(names, vals, color=colors_)
    ax.set_xlabel("Market Cap (B USD)")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def build_insights(market_cap_stats: Optional[SeriesStats], btc_dom_stats: Optional[SeriesStats], dvol_stats: Optional[SeriesStats]) -> List[str]:
    insights: List[str] = []
    if market_cap_stats and market_cap_stats.change_pct is not None:
        direction = "上行" if market_cap_stats.change_pct >= 0 else "回落"
        insights.append(f"总市值区间 {direction}，变动 {fmt_signed(market_cap_stats.change_pct)}。")
    if btc_dom_stats and btc_dom_stats.change_pct is not None:
        direction = "上升" if btc_dom_stats.change_pct >= 0 else "下降"
        insights.append(f"BTC 统治力 {direction}，变动 {fmt_signed(btc_dom_stats.change_pct)}。")
    if dvol_stats and dvol_stats.change_pct is not None:
        direction = "走高" if dvol_stats.change_pct >= 0 else "回落"
        insights.append(f"隐含波动率（DVOL）{direction}，变动 {fmt_signed(dvol_stats.change_pct)}。")
    if not insights:
        insights.append("本期数据不足，无法生成稳定的趋势判断。")
    return insights


def render_html(report: Dict[str, Any], out_path: Path) -> None:
    charts = report.get("charts", [])
    sections = report.get("sections", [])
    data_gaps = report.get("data_gaps", [])
    key_points = report.get("key_points", [])
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='zh'>")
    html.append("<head>")
    html.append("<meta charset='utf-8' />")
    html.append(f"<title>{report.get('title')}</title>")
    html.append("<style>")
    html.append("body { font-family: -apple-system, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif; margin: 40px; color: #111; }")
    html.append("h1 { margin-bottom: 4px; }")
    html.append("h2 { margin-top: 28px; border-bottom: 1px solid #e3e5e8; padding-bottom: 6px; }")
    html.append(".meta { color: #666; font-size: 13px; }")
    html.append(".gap { color: #b11; }")
    html.append("table { border-collapse: collapse; width: 100%; margin-top: 12px; }")
    html.append("th, td { border: 1px solid #ddd; padding: 8px; font-size: 13px; }")
    html.append("th { background: #f5f6f8; text-align: left; }")
    html.append(".chart { margin: 16px 0; }")
    html.append(".chart img { max-width: 100%; border-radius: 6px; }")
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append(f"<h1>{report.get('title')}</h1>")
    html.append(f"<div class='meta'>区间：{report.get('range_label')} ｜ 生成时间：{report.get('generated_at')}</div>")

    if data_gaps:
        html.append("<h2>数据可用性说明</h2>")
        html.append("<ul>")
        for gap in data_gaps:
            html.append(f"<li class='gap'>{gap}</li>")
        html.append("</ul>")

    if key_points:
        html.append("<h2>关键结论</h2>")
        html.append("<ul>")
        for item in key_points:
            html.append(f"<li>{item}</li>")
        html.append("</ul>")

    for section in sections:
        html.append(f"<h2>{section.get('title')}</h2>")
        if section.get("paragraphs"):
            for p in section["paragraphs"]:
                html.append(f"<p>{p}</p>")
        if section.get("table"):
            headers = section["table"].get("headers")
            rows = section["table"].get("rows", [])
            html.append("<table>")
            if headers:
                html.append("<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>")
            for row in rows:
                html.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
            html.append("</table>")
        if section.get("charts"):
            for chart in section["charts"]:
                html.append("<div class='chart'>")
                if chart.get("title"):
                    html.append(f"<div class='meta'>{chart.get('title')}</div>")
                html.append(f"<img src='{chart.get('path')}' alt='{chart.get('title')}' />")
                html.append("</div>")

    html.append("</body>")
    html.append("</html>")

    out_path.write_text("\n".join(html), encoding="utf-8")


def register_cjk_font() -> Optional[str]:
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if not os.path.exists(path):
            continue
        try:
            font = TTFont("CJK", path, subfontIndex=0)
            pdfmetrics.registerFont(font)
            return "CJK"
        except Exception:
            continue
    return None


def scaled_image(path: Path, max_width: float) -> Image:
    with PILImage.open(path) as im:
        width, height = im.size
    scale = max_width / float(width)
    return Image(str(path), width=max_width, height=height * scale)


def render_pdf(report: Dict[str, Any], out_path: Path) -> None:
    font_name = register_cjk_font() or "Helvetica"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCN", fontName=font_name, fontSize=18, leading=22, spaceAfter=12))
    styles.add(ParagraphStyle(name="MetaCN", fontName=font_name, fontSize=10, leading=14, textColor=colors.grey))
    styles.add(ParagraphStyle(name="BodyCN", fontName=font_name, fontSize=11, leading=16))
    styles.add(ParagraphStyle(name="HeadingCN", fontName=font_name, fontSize=14, leading=18, spaceBefore=12, spaceAfter=8))

    doc = SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    story: List[Any] = []

    story.append(Paragraph(report.get("title", ""), styles["TitleCN"]))
    story.append(Paragraph(f"区间：{report.get('range_label')} ｜ 生成时间：{report.get('generated_at')}", styles["MetaCN"]))
    story.append(Spacer(1, 8))

    data_gaps = report.get("data_gaps", [])
    if data_gaps:
        story.append(Paragraph("数据可用性说明", styles["HeadingCN"]))
        for gap in data_gaps:
            story.append(Paragraph(f"- {gap}", styles["BodyCN"]))
        story.append(Spacer(1, 6))

    key_points = report.get("key_points", [])
    if key_points:
        story.append(Paragraph("关键结论", styles["HeadingCN"]))
        for item in key_points:
            story.append(Paragraph(f"- {item}", styles["BodyCN"]))
        story.append(Spacer(1, 6))

    for section in report.get("sections", []):
        story.append(Paragraph(section.get("title", ""), styles["HeadingCN"]))
        for p in section.get("paragraphs", []):
            story.append(Paragraph(p, styles["BodyCN"]))
        table = section.get("table")
        if table:
            headers = table.get("headers")
            rows = table.get("rows", [])
            if headers:
                data = [headers] + rows
            else:
                data = rows
            t = Table(data, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            story.append(Spacer(1, 6))
            story.append(t)
            story.append(Spacer(1, 8))
        for chart in section.get("charts", []):
            chart_path = Path(chart.get("abs_path") or chart.get("path", ""))
            if chart_path.exists():
                story.append(Spacer(1, 6))
                story.append(Paragraph(chart.get("title", "图表"), styles["MetaCN"]))
                max_width = A4[0] - 1.4 * inch
                story.append(scaled_image(chart_path, max_width))
                story.append(Spacer(1, 8))

    doc.build(story)


def build_report_context(
    mode: str,
    start: date,
    end: date,
    market_cap_series: List[Tuple[date, float]],
    volume_series: List[Tuple[date, float]],
    btc_dom_series: List[Tuple[date, float]],
    dvol_btc: List[Tuple[date, float]],
    dvol_eth: List[Tuple[date, float]],
    cmc_latest: Dict[str, Any],
    cg_global: Dict[str, Any],
    cg_categories: List[Dict[str, Any]],
    cg_markets: List[Dict[str, Any]],
    cg_trending: List[Dict[str, Any]],
    cg_deriv_exchanges: List[Dict[str, Any]],
    deribit_metrics: Dict[str, Any],
    data_gaps: List[str],
) -> Dict[str, Any]:
    market_cap_stats = series_stats(market_cap_series) if market_cap_series else None
    volume_stats = series_stats(volume_series) if volume_series else None
    btc_dom_stats = series_stats(btc_dom_series) if btc_dom_series else None
    dvol_stats = series_stats(dvol_btc) if dvol_btc else None

    key_points = build_insights(market_cap_stats, btc_dom_stats, dvol_stats)

    range_label = f"{start.isoformat()} 至 {end.isoformat()}"
    title = "CEX 每日市场脉搏" if mode == "daily" else "CEX 月度市场观察"
    snapshot_market_cap = cmc_latest.get("total_market_cap") or cg_global.get("total_market_cap")
    snapshot_volume = cmc_latest.get("total_volume_24h") or cg_global.get("total_volume_24h")
    snapshot_btc_dom = cmc_latest.get("btc_dominance") or cg_global.get("btc_dominance")

    market_table_rows = []
    if market_cap_stats and market_cap_stats.start is not None:
        market_table_rows.append(["总市值", fmt_usd(market_cap_stats.start), fmt_usd(market_cap_stats.end), fmt_signed(market_cap_stats.change_pct)])
    else:
        market_table_rows.append(["总市值", "N/A", fmt_usd(snapshot_market_cap), "当前值"])
    if volume_stats and volume_stats.avg is not None:
        market_table_rows.append(["24h 成交量", fmt_usd(volume_stats.low), fmt_usd(volume_stats.high), "区间"])
    else:
        market_table_rows.append(["24h 成交量", "N/A", fmt_usd(snapshot_volume), "当前值"])
    if btc_dom_stats and btc_dom_stats.start is not None:
        market_table_rows.append(["BTC 统治力", fmt_pct(btc_dom_stats.start), fmt_pct(btc_dom_stats.end), fmt_signed(btc_dom_stats.change_pct)])
    else:
        market_table_rows.append(["BTC 统治力", "N/A", fmt_pct(snapshot_btc_dom), "当前值"])

    deribit_table_rows = []
    for key, label in [
        ("btc_perp", "BTC 永续"),
        ("eth_perp", "ETH 永续"),
    ]:
        item = deribit_metrics.get(key, {})
        deribit_table_rows.append([
            label,
            fmt_usd(item.get("volume_usd")),
            fmt_usd(item.get("open_interest")),
            fmt_pct((item.get("current_funding") or 0) * 100.0) if item.get("current_funding") is not None else "N/A",
        ])

    summary_rows = []
    for key, label in [
        ("stablecoin_market_cap", "稳定币市值"),
        ("stablecoin_volume_24h", "稳定币 24h 成交量"),
        ("derivatives_volume_24h", "衍生品 24h 成交量"),
    ]:
        val = cmc_latest.get(key)
        summary_rows.append([label, fmt_usd(val) if isinstance(val, (int, float)) else "N/A"])

    global_snapshot_rows: List[List[str]] = []
    if isinstance(cmc_latest.get("active_cryptocurrencies"), int):
        global_snapshot_rows.append(["CMC 活跃币种数", str(cmc_latest.get("active_cryptocurrencies"))])
    if isinstance(cmc_latest.get("active_exchanges"), int):
        global_snapshot_rows.append(["CMC 活跃交易所数", str(cmc_latest.get("active_exchanges"))])
    if isinstance(cmc_latest.get("active_market_pairs"), int):
        global_snapshot_rows.append(["CMC 活跃交易对数", str(cmc_latest.get("active_market_pairs"))])
    if isinstance(cg_global.get("active_cryptocurrencies"), int):
        global_snapshot_rows.append(["CG 活跃币种数", str(cg_global.get("active_cryptocurrencies"))])
    if isinstance(cg_global.get("markets"), int):
        global_snapshot_rows.append(["CG 市场数量", str(cg_global.get("markets"))])
    if cg_global.get("market_cap_change_percentage_24h_usd") is not None:
        global_snapshot_rows.append(["CG 市值 24h 变化", fmt_pct(cg_global.get("market_cap_change_percentage_24h_usd"))])
    if cg_global.get("volume_change_percentage_24h_usd") is not None:
        global_snapshot_rows.append(["CG 成交量 24h 变化", fmt_pct(cg_global.get("volume_change_percentage_24h_usd"))])

    cg_market_rows: List[List[str]] = []
    for item in cg_markets[:10]:
        cg_market_rows.append([
            f"{(item.get('symbol') or '').upper()}",
            fmt_usd(item.get("current_price")),
            fmt_usd(item.get("market_cap")),
            fmt_usd(item.get("total_volume")),
            fmt_pct(item.get("price_change_percentage_24h")),
        ])

    trending_rows: List[List[str]] = []
    for item in cg_trending[:10]:
        rank = item.get("market_cap_rank")
        rank_txt = str(rank) if rank is not None else "N/A"
        trending_rows.append([
            item.get("symbol") or "",
            item.get("name") or "",
            rank_txt,
            f"{item.get('price_btc'):.8f}" if item.get("price_btc") is not None else "N/A",
        ])

    cat_rows = []
    if cg_categories:
        top_cap = sorted(cg_categories, key=lambda x: (x.get("market_cap") or 0), reverse=True)[:10]
        cat_rows = [[c.get("name") or c.get("id"), fmt_usd(c.get("market_cap")), fmt_pct(c.get("market_cap_change_24h")), fmt_usd(c.get("volume_24h"))] for c in top_cap]

    cg_deriv_rows: List[List[str]] = []
    deriv_sorted = sorted(cg_deriv_exchanges, key=lambda x: (x.get("open_interest_btc") or 0), reverse=True)
    for item in deriv_sorted[:10]:
        cg_deriv_rows.append([
            item.get("name") or "",
            f"{item.get('open_interest_btc'):.2f}" if item.get("open_interest_btc") is not None else "N/A",
            f"{item.get('trade_volume_24h_btc'):.2f}" if item.get("trade_volume_24h_btc") is not None else "N/A",
            str(item.get("number_of_perpetual_pairs")) if item.get("number_of_perpetual_pairs") is not None else "N/A",
        ])

    pulse_table_rows = [
        ["市场结构", "总市值变动 / 24h 成交量 / BTC 统治力", "CMC / CG", "成交量决定手续费收入预期，统治力反映资金集中度"],
        ["衍生品", "OI / 资金费率 / DVOL", "Deribit", "高 OI + 正费率可能积累拥挤风险"],
        ["链上资金", "交易所净流入 / 稳定币供给", "N/A", "净流入通常对应抛压"],
        ["情绪指标", "恐惧与贪婪 / 社交主导率", "N/A", "极端贪婪常是短期顶部信号"],
        ["叙事热点", "板块涨幅 / 热门叙事", "CoinGecko", "指引资金偏好与潜在热点"],
    ]

    sections = [
        {
            "title": "市场结构",
            "paragraphs": ["本期总市值、成交量与 BTC 统治力如下。"],
            "table": {
                "headers": ["指标", "起点", "终点", "变化"],
                "rows": market_table_rows,
            },
            "charts": [],
        },
        {
            "title": "全局快照（CMC + CoinGecko）",
            "paragraphs": ["以下是当前套餐可稳定获取的全局快照字段。"],
            "table": {
                "headers": ["指标", "当前值"],
                "rows": global_snapshot_rows or [["全局快照", "N/A"]],
            },
            "charts": [],
        },
        {
            "title": "衍生品（Deribit）",
            "paragraphs": ["永续合约 24h 成交量、OI 与资金费率概览。"],
            "table": {
                "headers": ["品种", "24h 成交量", "未平仓量(OI)", "当前资金费率"],
                "rows": deribit_table_rows,
            },
            "charts": [],
        },
        {
            "title": "指标模板（可扩展）",
            "paragraphs": ["与 PDF 版式一致的 CEX 市场脉搏监测模板，可按数据源补齐。"],
            "table": {
                "headers": ["指标维度", "核心监测数据", "数据源", "业务关联解读"],
                "rows": pulse_table_rows,
            },
            "charts": [],
        },
        {
            "title": "资金与稳定币",
            "paragraphs": ["稳定币与衍生品成交量的最新值（如可用）。"],
            "table": {
                "headers": ["指标", "当前值"],
                "rows": summary_rows,
            },
            "charts": [],
        },
        {
            "title": "CoinGecko Top Coins",
            "paragraphs": ["按市值排序的头部币种快照（Demo 可用）。"],
            "table": {
                "headers": ["Symbol", "价格(USD)", "市值", "24h 成交量", "24h 涨跌"],
                "rows": cg_market_rows or [["N/A", "N/A", "N/A", "N/A", "N/A"]],
            },
            "charts": [],
        },
        {
            "title": "CoinGecko Trending",
            "paragraphs": ["搜索趋势榜（Demo 可用）。"],
            "table": {
                "headers": ["Symbol", "Name", "市值排名", "Price(BTC)"],
                "rows": trending_rows or [["N/A", "N/A", "N/A", "N/A"]],
            },
            "charts": [],
        },
        {
            "title": "CoinGecko Derivatives Exchanges",
            "paragraphs": ["衍生品交易所概览（Demo 可用）。"],
            "table": {
                "headers": ["交易所", "OI(BTC)", "24h 交易量(BTC)", "永续对数量"],
                "rows": cg_deriv_rows or [["N/A", "N/A", "N/A", "N/A"]],
            },
            "charts": [],
        },
    ]

    if cat_rows:
        sections.append({
            "title": "板块热点（CoinGecko）",
            "paragraphs": ["按市值排名的板块热点。"],
            "table": {"headers": ["板块", "市值", "24h 变化", "24h 成交量"], "rows": cat_rows},
            "charts": [],
        })

    report = {
        "title": title,
        "range_label": range_label,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ"),
        "data_gaps": data_gaps,
        "key_points": key_points,
        "sections": sections,
        "charts": [],
        "stats": {
            "market_cap": market_cap_stats.__dict__ if market_cap_stats else {},
            "volume": volume_stats.__dict__ if volume_stats else {},
            "btc_dominance": btc_dom_stats.__dict__ if btc_dom_stats else {},
            "dvol_btc": dvol_stats.__dict__ if dvol_stats else {},
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="CEX daily/monthly report agent")
    parser.add_argument("--mode", choices=["daily", "monthly"], default="daily", help="Report mode")
    parser.add_argument("--date", help="Target date for daily report (YYYY-MM-DD)")
    parser.add_argument("--month", help="Target month for monthly report (YYYY-MM)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--outdir", default="reports", help="Output directory")
    parser.add_argument("--cg-plan", choices=["pro", "demo", "public"], help="CoinGecko plan")
    parser.add_argument("--deribit-base", help="Deribit base URL (default prod)")
    args = parser.parse_args()

    if args.mode == "monthly":
        if args.start and args.end:
            start = parse_date(args.start)
            end = parse_date(args.end)
        elif args.month:
            start, end = parse_month(args.month)
        else:
            start, end = last_full_month()
    else:
        if args.date:
            start = parse_date(args.date)
            end = start
        elif args.start and args.end:
            start = parse_date(args.start)
            end = parse_date(args.end)
        else:
            start = last_full_day()
            end = start

    if start > end:
        print("Start date must be <= end date", file=sys.stderr)
        return 2

    mode = args.mode
    if mode == "monthly":
        outdir = Path(args.outdir) / "monthly" / start.strftime("%Y-%m")
        label = start.strftime("%Y-%m")
    else:
        outdir = Path(args.outdir) / "daily" / start.strftime("%Y-%m-%d")
        label = start.strftime("%Y-%m-%d")
    charts_dir = outdir / "charts"
    outdir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)

    cmc_key = os.getenv("CMC_API_KEY") or os.getenv("CMC_PRO_API_KEY")
    cg_key = os.getenv("COINGECKO_API_KEY") or os.getenv("CG_API_KEY")
    cg_plan = args.cg_plan or os.getenv("COINGECKO_API_PLAN") or os.getenv("CG_PLAN")
    deribit_base = args.deribit_base or os.getenv("DERIBIT_BASE_URL") or DERIBIT_BASE

    data_gaps: List[str] = []

    cmc_latest: Dict[str, Any] = {}
    cmc_hist_series: List[Dict[str, Any]] = []
    if cmc_key:
        latest_res = fetch_cmc_latest(cmc_key)
        if latest_res.error:
            data_gaps.append(f"CMC 最新全局指标获取失败：{latest_res.error}")
        else:
            cmc_latest = extract_cmc_latest(latest_res.data)

        hist_start = start if mode == "monthly" else (start - timedelta(days=29))
        hist_res = fetch_cmc_historical(cmc_key, hist_start, end)
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
    cg_markets: List[Dict[str, Any]] = []
    cg_trending: List[Dict[str, Any]] = []
    cg_deriv_exchanges: List[Dict[str, Any]] = []

    if cg_plan in ("pro", "demo") and not cg_key:
        data_gaps.append(f"CoinGecko 指定了 {cg_plan} 计划但未提供 API Key，已回退 public")
        cg_plan = "public"

    if cg_plan:
        cg_plans = [cg_plan]
    else:
        cg_plans = ["pro", "demo", "public"] if cg_key else ["public"]

    def try_cg(fetch_fn):
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

    cg_start = start if mode == "monthly" else (start - timedelta(days=29))
    cg_res, _, err = try_cg(lambda key, plan: fetch_cg_market_cap_chart(key, cg_start, plan))
    if err:
        data_gaps.append(f"CoinGecko 市值/成交量时间序列获取失败：{err}")
    elif cg_res:
        mc, vol = extract_cg_market_cap_chart(cg_res.data)
        cg_market_cap_series = mc
        cg_volume_series = vol

    cat_res, _, err = try_cg(lambda key, plan: fetch_cg_categories(key, plan))
    if err:
        data_gaps.append(f"CoinGecko 板块分类获取失败：{err}")
    elif cat_res:
        cg_categories = extract_cg_categories(cat_res.data)

    cg_global_res, _, err = try_cg(lambda key, plan: fetch_cg_global(key, plan))
    if err:
        data_gaps.append(f"CoinGecko Global 获取失败：{err}")
    elif cg_global_res:
        cg_global = extract_cg_global(cg_global_res.data)

    markets_res, _, err = try_cg(lambda key, plan: fetch_cg_markets(key, plan, per_page=20, page=1))
    if err:
        data_gaps.append(f"CoinGecko markets 获取失败：{err}")
    elif markets_res:
        cg_markets = extract_cg_markets(markets_res.data)

    trending_res, _, err = try_cg(lambda key, plan: fetch_cg_trending(key, plan))
    if err:
        data_gaps.append(f"CoinGecko trending 获取失败：{err}")
    elif trending_res:
        cg_trending = extract_cg_trending(trending_res.data)

    deriv_ex_res, _, err = try_cg(lambda key, plan: fetch_cg_derivatives_exchanges(key, plan))
    if err:
        data_gaps.append(f"CoinGecko derivatives exchanges 获取失败：{err}")
    elif deriv_ex_res:
        cg_deriv_exchanges = extract_cg_derivatives_exchanges(deriv_ex_res.data)

    # Build series from CMC history if available
    market_cap_series: List[Tuple[date, float]] = []
    volume_series: List[Tuple[date, float]] = []
    btc_dom_series: List[Tuple[date, float]] = []

    if cmc_hist_series:
        market_cap_series = [(x["date"], x["total_market_cap"]) for x in cmc_hist_series if x.get("total_market_cap") is not None]
        volume_series = [(x["date"], x["total_volume_24h"]) for x in cmc_hist_series if x.get("total_volume_24h") is not None]
        btc_dom_series = [(x["date"], x["btc_dominance"]) for x in cmc_hist_series if x.get("btc_dominance") is not None]
    else:
        market_cap_series = cg_market_cap_series
        volume_series = cg_volume_series

    market_cap_series_all = normalize_daily(market_cap_series)
    volume_series_all = normalize_daily(volume_series)
    btc_dom_series_all = normalize_daily(btc_dom_series)

    if mode == "monthly":
        market_cap_series = filter_range(market_cap_series_all, start, end)
        volume_series = filter_range(volume_series_all, start, end)
        btc_dom_series = filter_range(btc_dom_series_all, start, end)
        market_cap_chart_series = market_cap_series
        volume_chart_series = volume_series
        btc_dom_chart_series = btc_dom_series
    else:
        stats_start = start - timedelta(days=1)
        chart_start = start - timedelta(days=29)
        market_cap_series = filter_range(market_cap_series_all, stats_start, end)
        volume_series = filter_range(volume_series_all, stats_start, end)
        btc_dom_series = filter_range(btc_dom_series_all, stats_start, end)
        market_cap_chart_series = filter_range(market_cap_series_all, chart_start, end)
        volume_chart_series = filter_range(volume_series_all, chart_start, end)
        btc_dom_chart_series = filter_range(btc_dom_series_all, chart_start, end)

    # Deribit data
    deribit_metrics: Dict[str, Any] = {}
    dvol_btc: List[Tuple[date, float]] = []
    dvol_eth: List[Tuple[date, float]] = []

    dvol_start = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
    dvol_end = datetime.combine(end, datetime.max.time(), tzinfo=timezone.utc)
    if mode == "daily":
        dvol_start = dvol_start - timedelta(days=29)

    dvol_btc_res = deribit_get_vol_index("BTC", dvol_start, dvol_end, resolution=3600, base_url=deribit_base)
    if dvol_btc_res.error:
        data_gaps.append(f"Deribit DVOL(BTC) 获取失败：{dvol_btc_res.error}")
    else:
        dvol_btc = normalize_daily(
            filter_range(extract_deribit_dvol_series(dvol_btc_res.data), start if mode == "monthly" else dvol_start.date(), end)
        )

    dvol_eth_res = deribit_get_vol_index("ETH", dvol_start, dvol_end, resolution=3600, base_url=deribit_base)
    if dvol_eth_res.error:
        data_gaps.append(f"Deribit DVOL(ETH) 获取失败：{dvol_eth_res.error}")
    else:
        dvol_eth = normalize_daily(
            filter_range(extract_deribit_dvol_series(dvol_eth_res.data), start if mode == "monthly" else dvol_start.date(), end)
        )

    for name, key in [("BTC-PERPETUAL", "btc_perp"), ("ETH-PERPETUAL", "eth_perp")]:
        ticker_res = deribit_get_ticker(name, base_url=deribit_base)
        if ticker_res.error:
            data_gaps.append(f"Deribit ticker {name} 获取失败：{ticker_res.error}")
            continue
        deribit_metrics[key] = extract_deribit_ticker(ticker_res.data)

    # Aggregate summary by currency
    for currency in ["BTC", "ETH"]:
        for kind in ["option", "future"]:
            summary_res = deribit_get_book_summary_by_currency(currency, kind, base_url=deribit_base)
            if summary_res.error:
                data_gaps.append(f"Deribit {currency} {kind} summary 获取失败：{summary_res.error}")
                continue
            deribit_metrics[f"{currency.lower()}_{kind}_summary"] = aggregate_deribit_summary(summary_res.data)

    report = build_report_context(
        mode,
        start,
        end,
        market_cap_series,
        volume_series,
        btc_dom_series,
        dvol_btc,
        dvol_eth,
        cmc_latest,
        cg_global,
        cg_categories,
        cg_markets,
        cg_trending,
        cg_deriv_exchanges,
        deribit_metrics,
        data_gaps,
    )

    # Charts
    market_charts = []
    deriv_charts = []
    cat_charts = []
    mc_chart = charts_dir / f"market_cap_volume_{label}.png"
    plot_market_cap_volume(market_cap_chart_series, volume_chart_series, f"Total Market Cap & 24h Volume ({label})", mc_chart)
    if mc_chart.exists():
        market_charts.append({"title": "总市值与成交量", "path": f"charts/{mc_chart.name}", "abs_path": str(mc_chart)})

    btc_chart = charts_dir / f"btc_dominance_{label}.png"
    plot_line(btc_dom_chart_series, f"BTC Dominance ({label})", "%", btc_chart, color="#00d084")
    if btc_chart.exists():
        market_charts.append({"title": "BTC 统治力", "path": f"charts/{btc_chart.name}", "abs_path": str(btc_chart)})

    dvol_chart = charts_dir / f"dvol_{label}.png"
    plot_dual_line(dvol_btc, dvol_eth, ("BTC DVOL", "ETH DVOL"), f"Deribit DVOL ({label})", "DVOL", dvol_chart)
    if dvol_chart.exists():
        deriv_charts.append({"title": "Deribit DVOL", "path": f"charts/{dvol_chart.name}", "abs_path": str(dvol_chart)})

    if cg_categories and mode == "monthly":
        cat_chart = charts_dir / f"categories_{label}.png"
        plot_categories(cg_categories, cat_chart, "Top Categories by Market Cap")
        if cat_chart.exists():
            cat_charts.append({"title": "板块市值 Top 10", "path": f"charts/{cat_chart.name}", "abs_path": str(cat_chart)})

    # Attach charts to sections (append to first section)
    if report.get("sections"):
        report["sections"][0]["charts"].extend(market_charts)
    if len(report.get("sections", [])) > 1:
        report["sections"][1]["charts"].extend(deriv_charts)
    if cat_charts:
        for section in report.get("sections", []):
            if "板块热点" in section.get("title", ""):
                section["charts"].extend(cat_charts)
                break

    report_path = outdir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    html_path = outdir / "report.html"
    render_html(report, html_path)

    pdf_path = outdir / "report.pdf"
    render_pdf(report, pdf_path)

    print(f"Report JSON: {report_path}")
    print(f"Report HTML: {html_path}")
    print(f"Report PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
