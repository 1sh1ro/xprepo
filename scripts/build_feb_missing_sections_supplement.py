#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from pytrends.request import TrendReq

MONTH = "2026-02"
START = date(2026, 2, 1)
END = date(2026, 2, 28)

OUTDIR = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/supplement")
OUTDIR.mkdir(parents=True, exist_ok=True)

CG_PUBLIC_BASE = "https://api.coingecko.com/api/v3"
CMC_GLOBAL_HIST = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"
OKX_FUNDING_HIST = "https://www.okx.com/api/v5/public/funding-rate-history"
ALT_FNG = "https://api.alternative.me/fng/"


def _get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
    full = url if not params else f"{url}?{urlencode({k: v for k, v in params.items() if v is not None})}"
    req_headers = {"User-Agent": "feb-supplement/1.0", "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    req = Request(full, headers=req_headers)
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _cg_headers_from_secret() -> Dict[str, str]:
    secret = Path("/Users/my/.codex/skills/.coingecko.local.json")
    if not secret.exists():
        return {}
    try:
        raw = json.loads(secret.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}
    key = raw.get("api_key")
    plan = str(raw.get("plan") or "").lower().strip()
    if isinstance(key, str) and key.strip():
        if plan == "pro":
            return {"x-cg-pro-api-key": key.strip()}
        return {"x-cg-demo-api-key": key.strip()}
    return {}


def fetch_okx_funding(inst_id: str, start: date, end: date) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    before: Optional[str] = None
    seen = set()
    for _ in range(30):
        payload = _get_json(OKX_FUNDING_HIST, {"instId": inst_id, "limit": "100", "before": before})
        arr = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(arr, list) or not arr:
            break
        stop = False
        for row in arr:
            if not isinstance(row, dict):
                continue
            ts = row.get("fundingTime")
            fr = row.get("fundingRate")
            if not (isinstance(ts, str) and ts.isdigit() and isinstance(fr, str)):
                continue
            if ts in seen:
                continue
            seen.add(ts)
            d = datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc).date()
            try:
                v = float(fr)
            except Exception:
                continue
            if d < start:
                stop = True
                continue
            if d > end:
                continue
            out.append({"date": d.isoformat(), "funding_rate": v, "instId": inst_id})
        before = arr[-1].get("fundingTime") if isinstance(arr[-1], dict) else None
        if stop or not before:
            break
    out.sort(key=lambda x: x["date"])
    return out


def summarize_funding(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {"count": 0}
    vals = [(r["date"], float(r["funding_rate"])) for r in rows]
    hi = max(vals, key=lambda x: x[1])
    lo = min(vals, key=lambda x: x[1])
    avg = sum(v for _, v in vals) / len(vals)
    return {
        "count": len(vals),
        "high_date": hi[0],
        "high": hi[1],
        "low_date": lo[0],
        "low": lo[1],
        "avg": avg,
    }


def read_deribit_dvol() -> List[Tuple[date, float, float]]:
    p = Path("/Users/my/xp/reports/2026-02/secondary_orchestrated/packages/deribit/deribit_dvol_daily.csv")
    out: List[Tuple[date, float, float]] = []
    with p.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = datetime.strptime(row["date"], "%Y-%m-%d").date()
                b = float(row["btc_dvol_close"])
                e = float(row["eth_dvol_close"])
            except Exception:
                continue
            if START <= d <= END:
                out.append((d, b, e))
    return out


def summarize_dvol_phases(rows: List[Tuple[date, float, float]]) -> Dict[str, Any]:
    if not rows:
        return {}
    btc = [(d, b) for d, b, _ in rows]
    eth = [(d, e) for d, _, e in rows]

    def phase(series: List[Tuple[date, float]]) -> Dict[str, Any]:
        lo = min(series, key=lambda x: x[1])
        hi = max(series, key=lambda x: x[1])
        start_v = series[0][1]
        end_v = series[-1][1]
        # For this month we define:
        # Complacency: from month start to local min (risk underpricing)
        # Panic: min -> max (rapid repricing)
        # Normalization: max -> month end
        return {
            "min_date": lo[0].isoformat(),
            "min": lo[1],
            "max_date": hi[0].isoformat(),
            "max": hi[1],
            "start": start_v,
            "end": end_v,
        }

    return {"btc": phase(btc), "eth": phase(eth)}


def fetch_fng_month() -> List[Tuple[date, int, str]]:
    payload = _get_json(ALT_FNG, {"limit": "120"})
    arr = payload.get("data") if isinstance(payload, dict) else None
    out: List[Tuple[date, int, str]] = []
    if not isinstance(arr, list):
        return out
    for row in arr:
        if not isinstance(row, dict):
            continue
        v = row.get("value")
        ts = row.get("timestamp")
        cls = str(row.get("value_classification") or "")
        if not (isinstance(v, str) and v.isdigit() and isinstance(ts, str) and ts.isdigit()):
            continue
        d = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
        if START <= d <= END:
            out.append((d, int(v), cls))
    out.sort(key=lambda x: x[0])
    return out


def summarize_fng(rows: List[Tuple[date, int, str]]) -> Dict[str, Any]:
    if not rows:
        return {}
    maxp = max(rows, key=lambda x: x[1])
    minp = min(rows, key=lambda x: x[1])
    diffs = []
    for i in range(1, len(rows)):
        diffs.append((rows[i][0], rows[i][1] - rows[i - 1][1]))
    up = max(diffs, key=lambda x: x[1]) if diffs else None
    down = min(diffs, key=lambda x: x[1]) if diffs else None
    return {
        "max_date": maxp[0].isoformat(),
        "max": maxp[1],
        "max_class": maxp[2],
        "min_date": minp[0].isoformat(),
        "min": minp[1],
        "min_class": minp[2],
        "largest_up_date": up[0].isoformat() if up else None,
        "largest_up": up[1] if up else None,
        "largest_down_date": down[0].isoformat() if down else None,
        "largest_down": down[1] if down else None,
    }


def fetch_google_trends() -> Dict[str, Any]:
    pytrends = TrendReq(hl="en-US", tz=0, retries=2, backoff_factor=0.5)
    kw = ["Bitcoin", "Ethereum", "Memecoin"]
    pytrends.build_payload(kw_list=kw, timeframe="2026-02-01 2026-02-28", geo="")
    df = pytrends.interest_over_time()
    if df is None or df.empty:
        return {"ok": False, "reason": "empty"}
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    phases = {
        "phase_1": (date(2026, 2, 1), date(2026, 2, 10)),
        "phase_2": (date(2026, 2, 11), date(2026, 2, 20)),
        "phase_3": (date(2026, 2, 21), date(2026, 2, 28)),
    }

    out: Dict[str, Any] = {"ok": True, "phases": {}}
    for pname, (s, e) in phases.items():
        part = df[(df.index.date >= s) & (df.index.date <= e)]
        block: Dict[str, Any] = {}
        for k in kw:
            if k not in part.columns:
                continue
            vals = [int(v) for v in part[k].tolist()]
            if not vals:
                continue
            block[k] = {
                "avg": sum(vals) / len(vals),
                "max": max(vals),
                "min": min(vals),
            }
        out["phases"][pname] = block
    # store daily for csv
    daily_rows = []
    for idx, row in df.iterrows():
        d = idx.date()
        if not (START <= d <= END):
            continue
        daily_rows.append({
            "date": d.isoformat(),
            "Bitcoin": int(row.get("Bitcoin", 0)),
            "Ethereum": int(row.get("Ethereum", 0)),
            "Memecoin": int(row.get("Memecoin", 0)),
        })
    out["daily"] = daily_rows
    return out


def fetch_cg_total_volume_daily(coin_id: str, cg_headers: Dict[str, str]) -> Dict[date, float]:
    payload = _get_json(
        f"{CG_PUBLIC_BASE}/coins/{coin_id}/market_chart",
        {"vs_currency": "usd", "days": "120"},
        headers=cg_headers,
    )
    arr = payload.get("total_volumes") if isinstance(payload, dict) else None
    out: Dict[date, float] = {}
    if not isinstance(arr, list):
        return out
    for row in arr:
        if not (isinstance(row, list) and len(row) >= 2):
            continue
        ts, v = row[0], row[1]
        if not isinstance(ts, (int, float)) or not isinstance(v, (int, float)):
            continue
        d = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).date()
        if START <= d <= END:
            out[d] = float(v)
    return out


def weekly_aggregate(vol_map: Dict[date, float]) -> List[Tuple[date, float]]:
    wk: Dict[date, float] = defaultdict(float)
    for d, v in vol_map.items():
        monday = d - timedelta(days=d.weekday())
        wk[monday] += v
    return sorted(wk.items(), key=lambda x: x[0])


def write_csv_rows(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    cg_headers = _cg_headers_from_secret()

    # 1) OKX funding extremes
    btc_okx = fetch_okx_funding("BTC-USDT-SWAP", START, END)
    eth_okx = fetch_okx_funding("ETH-USDT-SWAP", START, END)
    btc_okx_sum = summarize_funding(btc_okx)
    eth_okx_sum = summarize_funding(eth_okx)
    write_csv_rows(OUTDIR / "okx_funding_btc_feb2026.csv", btc_okx, ["date", "funding_rate", "instId"])
    write_csv_rows(OUTDIR / "okx_funding_eth_feb2026.csv", eth_okx, ["date", "funding_rate", "instId"])

    # 2) DVOL phases
    dvol_rows = read_deribit_dvol()
    dvol_sum = summarize_dvol_phases(dvol_rows)

    # 3) F&G key timestamps
    fng_rows = fetch_fng_month()
    fng_sum = summarize_fng(fng_rows)
    write_csv_rows(
        OUTDIR / "fng_daily_feb2026.csv",
        [{"date": d.isoformat(), "value": v, "classification": c} for d, v, c in fng_rows],
        ["date", "value", "classification"],
    )

    # 4) Google trends 3-stage
    trends = fetch_google_trends()
    if trends.get("ok"):
        write_csv_rows(OUTDIR / "google_trends_daily_feb2026.csv", trends.get("daily", []), ["date", "Bitcoin", "Ethereum", "Memecoin"])

    # 5) Stablecoin weekly trend (USDT vs USDC)
    usdt = fetch_cg_total_volume_daily("tether", cg_headers)
    usdc = fetch_cg_total_volume_daily("usd-coin", cg_headers)
    usdt_w = weekly_aggregate(usdt)
    usdc_w = weekly_aggregate(usdc)
    weeks = sorted(set([d for d, _ in usdt_w] + [d for d, _ in usdc_w]))
    usdt_map = {d: v for d, v in usdt_w}
    usdc_map = {d: v for d, v in usdc_w}
    st_rows = []
    for w in weeks:
        u1 = usdt_map.get(w, 0.0)
        u2 = usdc_map.get(w, 0.0)
        tot = u1 + u2
        st_rows.append(
            {
                "week_start": w.isoformat(),
                "usdt_weekly_volume_usd": u1,
                "usdc_weekly_volume_usd": u2,
                "total_usdt_usdc_weekly_volume_usd": tot,
                "usdt_share_pct": (u1 / tot * 100.0) if tot > 0 else None,
                "usdc_share_pct": (u2 / tot * 100.0) if tot > 0 else None,
            }
        )
    write_csv_rows(
        OUTDIR / "stablecoin_weekly_usdt_usdc_feb2026.csv",
        st_rows,
        [
            "week_start",
            "usdt_weekly_volume_usd",
            "usdc_weekly_volume_usd",
            "total_usdt_usdc_weekly_volume_usd",
            "usdt_share_pct",
            "usdc_share_pct",
        ],
    )

    # markdown supplement
    md = []
    md.append("# 2026-02 缺口补齐补充（可并入月报）")
    md.append("")
    md.append("- 目标：补齐与 1 月版式对比中缺失的 5 项模块。")
    md.append(f"- 区间：{START.isoformat()} 至 {END.isoformat()}。")
    md.append("")

    md.append("## 1) 单一交易所 Funding 极值时序复盘（OKX）")
    md.append("数据来源：OKX `public/funding-rate-history`（BTC-USDT-SWAP / ETH-USDT-SWAP）")
    if btc_okx_sum.get("count", 0) > 0:
        md.append(
            f"- BTC：高点 {btc_okx_sum['high']:+.6f}（{btc_okx_sum['high_date']}），低点 {btc_okx_sum['low']:+.6f}（{btc_okx_sum['low_date']}），月均 {btc_okx_sum['avg']:+.6f}。"
        )
    if eth_okx_sum.get("count", 0) > 0:
        md.append(
            f"- ETH：高点 {eth_okx_sum['high']:+.6f}（{eth_okx_sum['high_date']}），低点 {eth_okx_sum['low']:+.6f}（{eth_okx_sum['low_date']}），月均 {eth_okx_sum['avg']:+.6f}。"
        )
    md.append("- 结论：该项可补齐（已产出明细 CSV）。")
    md.append("")

    md.append("## 2) DVOL 分阶段叙事（Complacency / Panic）")
    md.append("数据来源：Deribit `public/get_volatility_index_data`（月内日线）")
    if dvol_sum:
        b = dvol_sum["btc"]
        e = dvol_sum["eth"]
        md.append(
            f"- BTC：低波阶段低点 {b['min']:.2f}（{b['min_date']}）-> 恐慌阶段高点 {b['max']:.2f}（{b['max_date']}）-> 月末 {b['end']:.2f}。"
        )
        md.append(
            f"- ETH：低波阶段低点 {e['min']:.2f}（{e['min_date']}）-> 恐慌阶段高点 {e['max']:.2f}（{e['max_date']}）-> 月末 {e['end']:.2f}。"
        )
    md.append("- 结论：该项可补齐（已形成阶段化叙事模板）。")
    md.append("")

    md.append("## 3) F&G 关键时点映射")
    md.append("数据来源：Alternative.me `fng`")
    if fng_sum:
        md.append(
            f"- 月内高点：{fng_sum['max']}（{fng_sum['max_class']}，{fng_sum['max_date']}）；月内低点：{fng_sum['min']}（{fng_sum['min_class']}，{fng_sum['min_date']}）。"
        )
        md.append(
            f"- 最大单日上行：{fng_sum['largest_up']:+d}（{fng_sum['largest_up_date']}）；最大单日下行：{fng_sum['largest_down']:+d}（{fng_sum['largest_down_date']}）。"
        )
    md.append("- 结论：该项可补齐（已从“区间值”升级为“关键时点”）。")
    md.append("")

    md.append("## 4) Google Trends 搜索热度三阶段")
    md.append("数据来源：Google Trends（pytrends），关键词 `Bitcoin / Ethereum / Memecoin`，全球。")
    if trends.get("ok"):
        p = trends.get("phases", {})
        for k in ["phase_1", "phase_2", "phase_3"]:
            block = p.get(k, {})
            if not block:
                continue
            label = {"phase_1": "阶段一（1-10日）", "phase_2": "阶段二（11-20日）", "phase_3": "阶段三（21-28日）"}[k]
            md.append(
                f"- {label}：Bitcoin 均值 {block.get('Bitcoin',{}).get('avg',0):.1f}，Ethereum 均值 {block.get('Ethereum',{}).get('avg',0):.1f}，Memecoin 均值 {block.get('Memecoin',{}).get('avg',0):.1f}。"
            )
        md.append("- 结论：该项可补齐（已产出日频 CSV 与三阶段汇总）。")
    else:
        md.append("- 结论：该项当前未稳定补齐（Google Trends 请求受限，需重试或更换网络出口）。")
    md.append("")

    md.append("## 5) 稳定币周度趋势（USDT vs USDC）")
    md.append("数据来源：CoinGecko `coins/{id}/market_chart` 的 `total_volumes`（USDT/USDC）")
    if st_rows:
        first = st_rows[0]
        last = st_rows[-1]
        md.append(
            f"- 周初（{first['week_start']}）：USDT 占比 {first['usdt_share_pct']:.2f}%，USDC 占比 {first['usdc_share_pct']:.2f}%。"
        )
        md.append(
            f"- 周末（{last['week_start']}）：USDT 占比 {last['usdt_share_pct']:.2f}%，USDC 占比 {last['usdc_share_pct']:.2f}%。"
        )
        md.append("- 结论：该项可补齐（已产出周频对比 CSV）。")
    else:
        md.append("- 结论：该项暂不可用。")
    md.append("")

    md.append("## 产出文件")
    md.append("- `okx_funding_btc_feb2026.csv`")
    md.append("- `okx_funding_eth_feb2026.csv`")
    md.append("- `fng_daily_feb2026.csv`")
    md.append("- `google_trends_daily_feb2026.csv`（若成功）")
    md.append("- `stablecoin_weekly_usdt_usdc_feb2026.csv`")

    (OUTDIR / "feb_missing_sections_supplement.md").write_text("\n".join(md), encoding="utf-8")

    print("[ok] supplement:", OUTDIR / "feb_missing_sections_supplement.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
