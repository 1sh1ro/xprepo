#!/usr/bin/env python3
"""BTC 10 minute direction model and chronological backtest."""
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


COINBASE_CANDLES = "https://api.exchange.coinbase.com/products/{product}/candles"
OKX_HISTORY_CANDLES = "https://www.okx.com/api/v5/market/history-candles"
BINANCE_FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines"
BITSTAMP_OHLC = "https://www.bitstamp.net/api/v2/ohlc/{pair}/"
DEFAULT_PRODUCT = "BTC-USD"
DEFAULT_OKX_INST_ID = "BTC-USDT-SWAP"
DEFAULT_BINANCE_SYMBOL = "BTCUSDT"
DEFAULT_BITSTAMP_PAIR = "btcusd"
DEFAULT_GRANULARITY_SECONDS = 60
DEFAULT_HORIZON_MINUTES = 10


FEATURE_COLUMNS = [
    "ret_1m",
    "ret_2m",
    "ret_3m",
    "ret_5m",
    "ret_10m",
    "ret_15m",
    "ret_30m",
    "ret_60m",
    "ret_90m",
    "ret_120m",
    "rv_5m",
    "rv_10m",
    "rv_30m",
    "rv_60m",
    "rv_120m",
    "rv_ratio_10_60",
    "rv_ratio_30_120",
    "mom_slope_10m",
    "mom_slope_30m",
    "mom_slope_60m",
    "ema_gap_5_20",
    "ema_gap_10_60",
    "close_z_20m",
    "close_z_60m",
    "range_mean_10m",
    "range_mean_30m",
    "range_pct",
    "body_pct",
    "body_sum_5m",
    "body_sum_10m",
    "upper_wick_pct",
    "lower_wick_pct",
    "close_pos_in_range",
    "close_pos_30m",
    "close_pos_60m",
    "drawdown_30m",
    "drawdown_60m",
    "rebound_30m",
    "rebound_60m",
    "rsi_14m",
    "volume_chg_1m",
    "volume_ratio_10m",
    "volume_ratio_30m",
    "volume_z_30m",
    "volume_z_60m",
    "minute_sin",
    "minute_cos",
    "hour_sin",
    "hour_cos",
]


@dataclass
class RunConfig:
    source: str
    product: str
    days: int
    horizon_minutes: int
    outdir: Path
    input_csv: Optional[Path]
    probability_threshold: float
    min_train_rows: int
    test_fraction: float
    validation_fraction: float
    model_name: str
    threshold_mode: str
    min_threshold_coverage: float


def utc_now_floor_minute() -> datetime:
    now = datetime.now(timezone.utc)
    return now.replace(second=0, microsecond=0)


def http_get_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 30, retries: int = 4) -> Any:
    if params:
        url = f"{url}?{urlencode(params)}"
    last_exc: Optional[BaseException] = None
    for attempt in range(retries + 1):
        req = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "btc-10m-event-model/0.1",
            },
        )
        try:
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_exc = exc
            if isinstance(exc, HTTPError) and exc.code in {400, 401, 403, 404}:
                raise
            if attempt >= retries:
                break
            time.sleep(min(8.0, 0.75 * (2**attempt)))
    raise RuntimeError(f"GET failed after {retries + 1} attempts: {url}: {last_exc}") from last_exc


ProgressCallback = Optional[Callable[[int, int, Optional[datetime]], None]]


def fetch_coinbase_1m_candles(
    product: str,
    start: datetime,
    end: datetime,
    progress: ProgressCallback = None,
) -> pd.DataFrame:
    """Fetch Coinbase candles in 300 row chunks.

    Coinbase returns rows as [time, low, high, open, close, volume] in reverse
    chronological order. We request non-overlapping UTC windows and de-duplicate.
    """
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    if start >= end:
        raise ValueError("start must be before end")

    chunk = timedelta(seconds=DEFAULT_GRANULARITY_SECONDS * 300)
    rows: List[Dict[str, Any]] = []
    cursor = start
    url = COINBASE_CANDLES.format(product=product)

    while cursor < end:
        chunk_end = min(cursor + chunk, end)
        params = {
            "granularity": str(DEFAULT_GRANULARITY_SECONDS),
            "start": cursor.isoformat().replace("+00:00", "Z"),
            "end": chunk_end.isoformat().replace("+00:00", "Z"),
        }
        try:
            payload = http_get_json(url, params=params)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f"Coinbase candle fetch failed at {cursor.isoformat()}: {exc}") from exc
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected Coinbase response at {cursor.isoformat()}: {payload!r}")

        for item in payload:
            if not isinstance(item, list) or len(item) < 6:
                continue
            ts, low, high, open_, close, volume = item[:6]
            rows.append(
                {
                    "timestamp_utc": datetime.fromtimestamp(int(ts), tz=timezone.utc),
                    "open": float(open_),
                    "high": float(high),
                    "low": float(low),
                    "close": float(close),
                    "volume": float(volume),
                    "source": "coinbase",
                    "product": product,
                }
            )

        cursor = chunk_end
        if progress:
            progress(len(rows), -1, cursor)
        time.sleep(0.08)

    if not rows:
        raise RuntimeError("No Coinbase candles returned")

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["timestamp_utc"]).sort_values("timestamp_utc").reset_index(drop=True)
    return df


def fetch_okx_1m_candles(
    inst_id: str,
    start: datetime,
    end: datetime,
    progress: ProgressCallback = None,
    checkpoint_csv: Optional[Path] = None,
    checkpoint_every_pages: int = 10,
    max_page_failures: int = 20,
) -> pd.DataFrame:
    """Fetch OKX 1 minute history candles by paging backward from the latest candle.

    OKX rows are newest first:
    [ts, open, high, low, close, volume_contracts, volume_currency, volume_quote, confirm].
    The history endpoint pages older rows with the `after` cursor.
    """
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    if start >= end:
        raise ValueError("start must be before end")

    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)
    expected_rows = max(1, int((end_ms - start_ms) / 60_000) + 1)
    rows: List[Dict[str, Any]] = []
    seen: set[str] = set()
    cursor: Optional[str] = None

    if checkpoint_csv and checkpoint_csv.exists():
        checkpoint_df = load_candles(checkpoint_csv)
        checkpoint_df = checkpoint_df[
            (checkpoint_df["timestamp_utc"] >= start) & (checkpoint_df["timestamp_utc"] <= end)
        ].copy()
        if not checkpoint_df.empty:
            rows = checkpoint_df.to_dict("records")
            seen = set(
                (checkpoint_df["timestamp_utc"].astype("int64") // 1_000_000)
                .astype(str)
                .tolist()
            )
            oldest_ms = int(checkpoint_df["timestamp_utc"].min().timestamp() * 1000)
            cursor = str(oldest_ms)
            print(
                f"resuming OKX fetch from {len(rows)} checkpoint rows, "
                f"oldest_cursor={checkpoint_df['timestamp_utc'].min().isoformat()}",
                flush=True,
            )

    for page in range(1000):
        params = {"instId": inst_id, "bar": "1m", "limit": "300"}
        if cursor:
            params["after"] = cursor

        page_failures = 0
        while True:
            try:
                payload = http_get_json(OKX_HISTORY_CANDLES, params=params, retries=6)
                break
            except Exception:
                page_failures += 1
                if checkpoint_csv and rows:
                    save_candles(pd.DataFrame(rows), checkpoint_csv)
                    print(f"checkpoint saved after transient OKX fetch failure: {checkpoint_csv}", flush=True)
                if page_failures >= max_page_failures:
                    raise
                time.sleep(min(90.0, 5.0 * page_failures))

        if not isinstance(payload, dict) or payload.get("code") != "0":
            raise RuntimeError(f"Unexpected OKX response: {payload!r}")
        data = payload.get("data")
        if not isinstance(data, list) or not data:
            break

        oldest_ts: Optional[int] = None
        for item in data:
            if not isinstance(item, list) or len(item) < 8:
                continue
            ts = int(item[0])
            oldest_ts = ts if oldest_ts is None else min(oldest_ts, ts)
            if ts < start_ms or ts > end_ms:
                continue
            if item[0] in seen:
                continue
            seen.add(item[0])
            rows.append(
                {
                    "timestamp_utc": datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc),
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[7]),
                    "volume_contracts": float(item[5]),
                    "source": "okx",
                    "product": inst_id,
                    "confirmed": item[8] if len(item) > 8 else None,
                }
            )

        cursor = str(oldest_ts) if oldest_ts is not None else None
        if progress:
            oldest_dt = datetime.fromtimestamp(oldest_ts / 1000.0, tz=timezone.utc) if oldest_ts else None
            progress(len(rows), expected_rows, oldest_dt)
        if checkpoint_csv and rows and page % checkpoint_every_pages == 0:
            save_candles(pd.DataFrame(rows), checkpoint_csv)
        if oldest_ts is None or oldest_ts <= start_ms:
            break
        time.sleep(0.05)

    if not rows:
        raise RuntimeError("No OKX candles returned")

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["timestamp_utc"]).sort_values("timestamp_utc").reset_index(drop=True)
    if checkpoint_csv:
        save_candles(df, checkpoint_csv)
    return df


def fetch_binance_1m_candles(
    symbol: str,
    start: datetime,
    end: datetime,
    progress: ProgressCallback = None,
    checkpoint_csv: Optional[Path] = None,
    checkpoint_every_pages: int = 10,
) -> pd.DataFrame:
    """Fetch Binance USD-M futures 1 minute klines by paging forward."""
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    if start >= end:
        raise ValueError("start must be before end")

    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)
    expected_rows = max(1, int((end_ms - start_ms) / 60_000) + 1)
    rows: List[Dict[str, Any]] = []
    seen: set[str] = set()
    cursor = start_ms

    if checkpoint_csv and checkpoint_csv.exists():
        checkpoint_df = load_candles(checkpoint_csv)
        checkpoint_df = checkpoint_df[
            (checkpoint_df["timestamp_utc"] >= start) & (checkpoint_df["timestamp_utc"] <= end)
        ].copy()
        if not checkpoint_df.empty:
            rows = checkpoint_df.to_dict("records")
            seen = set(
                (checkpoint_df["timestamp_utc"].astype("int64") // 1_000_000)
                .astype(str)
                .tolist()
            )
            newest_ms = int(checkpoint_df["timestamp_utc"].max().timestamp() * 1000)
            cursor = newest_ms + 60_000
            print(
                f"resuming Binance fetch from {len(rows)} checkpoint rows, "
                f"newest_cursor={checkpoint_df['timestamp_utc'].max().isoformat()}",
                flush=True,
            )

    page = 0
    while cursor <= end_ms:
        page += 1
        params = {
            "symbol": symbol,
            "interval": "1m",
            "startTime": str(cursor),
            "endTime": str(end_ms),
            "limit": "1500",
        }
        payload = http_get_json(BINANCE_FAPI_KLINES, params=params, timeout=20, retries=8)
        if not isinstance(payload, list) or not payload:
            break

        newest_ts: Optional[int] = None
        for item in payload:
            if not isinstance(item, list) or len(item) < 8:
                continue
            ts = int(item[0])
            newest_ts = ts if newest_ts is None else max(newest_ts, ts)
            if ts < start_ms or ts > end_ms:
                continue
            ts_key = str(ts)
            if ts_key in seen:
                continue
            seen.add(ts_key)
            rows.append(
                {
                    "timestamp_utc": datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc),
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[7]),
                    "volume_base": float(item[5]),
                    "source": "binance",
                    "product": symbol,
                }
            )

        if newest_ts is None:
            break
        cursor = newest_ts + 60_000
        if progress:
            progress(len(rows), expected_rows, datetime.fromtimestamp(newest_ts / 1000.0, tz=timezone.utc))
        if checkpoint_csv and rows and page % checkpoint_every_pages == 0:
            save_candles(pd.DataFrame(rows), checkpoint_csv)
        time.sleep(0.08)

    if not rows:
        raise RuntimeError("No Binance candles returned")

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["timestamp_utc"]).sort_values("timestamp_utc").reset_index(drop=True)
    if checkpoint_csv:
        save_candles(df, checkpoint_csv)
    return df


def fetch_bitstamp_1m_candles(
    pair: str,
    start: datetime,
    end: datetime,
    progress: ProgressCallback = None,
    checkpoint_csv: Optional[Path] = None,
    checkpoint_every_pages: int = 10,
) -> pd.DataFrame:
    """Fetch Bitstamp 1 minute OHLC candles by paging forward."""
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    if start >= end:
        raise ValueError("start must be before end")

    start_s = int(start.timestamp())
    end_s = int(end.timestamp())
    expected_rows = max(1, int((end_s - start_s) / 60) + 1)
    rows: List[Dict[str, Any]] = []
    seen: set[str] = set()
    cursor = end_s

    if checkpoint_csv and checkpoint_csv.exists():
        checkpoint_df = load_candles(checkpoint_csv)
        checkpoint_df = checkpoint_df[
            (checkpoint_df["timestamp_utc"] >= start) & (checkpoint_df["timestamp_utc"] <= end)
        ].copy()
        if not checkpoint_df.empty:
            rows = checkpoint_df.to_dict("records")
            seen = set(
                (checkpoint_df["timestamp_utc"].astype("int64") // 1_000_000_000)
                .astype(str)
                .tolist()
            )
            oldest_s = int(checkpoint_df["timestamp_utc"].min().timestamp())
            cursor = oldest_s - 60
            print(
                f"resuming Bitstamp fetch from {len(rows)} checkpoint rows, "
                f"oldest_cursor={checkpoint_df['timestamp_utc'].min().isoformat()}",
                flush=True,
            )

    page = 0
    url = BITSTAMP_OHLC.format(pair=pair.lower())
    while cursor >= start_s:
        page += 1
        params = {
            "step": "60",
            "limit": "1000",
            "start": str(start_s),
            "end": str(cursor),
        }
        payload = http_get_json(url, params=params, timeout=20, retries=8)
        data = payload.get("data", {}).get("ohlc") if isinstance(payload, dict) else None
        if not isinstance(data, list) or not data:
            break

        oldest_ts: Optional[int] = None
        for item in data:
            if not isinstance(item, dict):
                continue
            ts = int(item["timestamp"])
            oldest_ts = ts if oldest_ts is None else min(oldest_ts, ts)
            if ts < start_s or ts > end_s:
                continue
            ts_key = str(ts)
            if ts_key in seen:
                continue
            seen.add(ts_key)
            rows.append(
                {
                    "timestamp_utc": datetime.fromtimestamp(ts, tz=timezone.utc),
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"]),
                    "volume": float(item["volume"]),
                    "source": "bitstamp",
                    "product": pair.lower(),
                }
            )

        if oldest_ts is None:
            break
        cursor = oldest_ts - 60
        if progress:
            progress(len(rows), expected_rows, datetime.fromtimestamp(oldest_ts, tz=timezone.utc))
        if checkpoint_csv and rows and page % checkpoint_every_pages == 0:
            save_candles(pd.DataFrame(rows), checkpoint_csv)
        time.sleep(0.08)

    if not rows:
        raise RuntimeError("No Bitstamp candles returned")

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["timestamp_utc"]).sort_values("timestamp_utc").reset_index(drop=True)
    if checkpoint_csv:
        save_candles(df, checkpoint_csv)
    return df


def load_candles(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp_utc" not in df.columns:
        raise ValueError(f"{path} missing timestamp_utc")
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    required = {"open", "high", "low", "close", "volume"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    return df.sort_values("timestamp_utc").drop_duplicates("timestamp_utc").reset_index(drop=True)


def save_candles(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    out["timestamp_utc"] = pd.to_datetime(out["timestamp_utc"], utc=True)
    out = out.sort_values("timestamp_utc").drop_duplicates("timestamp_utc").reset_index(drop=True)
    out["timestamp_utc"] = out["timestamp_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    out.to_csv(tmp_path, index=False)
    tmp_path.replace(path)


def add_features_and_label(candles: pd.DataFrame, horizon_minutes: int = DEFAULT_HORIZON_MINUTES) -> pd.DataFrame:
    df = candles.copy()
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df = df.sort_values("timestamp_utc").drop_duplicates("timestamp_utc").reset_index(drop=True)

    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    open_ = df["open"].astype(float)
    volume = df["volume"].astype(float)
    log_close = np.log(close)

    for n in [1, 2, 3, 5, 10, 15, 30, 60, 90, 120]:
        df[f"ret_{n}m"] = log_close.diff(n)

    ret_1m = log_close.diff()
    for n in [5, 10, 30, 60, 120]:
        df[f"rv_{n}m"] = ret_1m.rolling(n).std() * math.sqrt(n)
    df["rv_ratio_10_60"] = df["rv_10m"] / df["rv_60m"].replace(0, np.nan)
    df["rv_ratio_30_120"] = df["rv_30m"] / df["rv_120m"].replace(0, np.nan)

    df["mom_slope_10m"] = df["ret_10m"] / 10.0
    df["mom_slope_30m"] = df["ret_30m"] / 30.0
    df["mom_slope_60m"] = df["ret_60m"] / 60.0

    ema_5 = close.ewm(span=5, adjust=False).mean()
    ema_10 = close.ewm(span=10, adjust=False).mean()
    ema_20 = close.ewm(span=20, adjust=False).mean()
    ema_60 = close.ewm(span=60, adjust=False).mean()
    df["ema_gap_5_20"] = (ema_5 / ema_20) - 1.0
    df["ema_gap_10_60"] = (ema_10 / ema_60) - 1.0

    for n in [20, 60]:
        close_mean = close.rolling(n).mean()
        close_std = close.rolling(n).std().replace(0, np.nan)
        df[f"close_z_{n}m"] = (close - close_mean) / close_std

    price_denom = close.replace(0, np.nan)
    candle_range = (high - low).replace(0, np.nan)
    df["range_pct"] = (high - low) / price_denom
    df["body_pct"] = (close - open_) / price_denom
    df["range_mean_10m"] = df["range_pct"].rolling(10).mean()
    df["range_mean_30m"] = df["range_pct"].rolling(30).mean()
    df["body_sum_5m"] = df["body_pct"].rolling(5).sum()
    df["body_sum_10m"] = df["body_pct"].rolling(10).sum()
    df["upper_wick_pct"] = (high - np.maximum(open_, close)) / price_denom
    df["lower_wick_pct"] = (np.minimum(open_, close) - low) / price_denom
    df["close_pos_in_range"] = (close - low) / candle_range

    for n in [30, 60]:
        rolling_high = high.rolling(n).max()
        rolling_low = low.rolling(n).min()
        rolling_range = (rolling_high - rolling_low).replace(0, np.nan)
        df[f"close_pos_{n}m"] = (close - rolling_low) / rolling_range
        df[f"drawdown_{n}m"] = (close / rolling_high.replace(0, np.nan)) - 1.0
        df[f"rebound_{n}m"] = (close / rolling_low.replace(0, np.nan)) - 1.0

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi_14m"] = 100.0 - (100.0 / (1.0 + rs))

    df["volume_chg_1m"] = np.log1p(volume).diff()
    for n in [10, 30]:
        df[f"volume_ratio_{n}m"] = (volume / volume.rolling(n).mean().replace(0, np.nan)) - 1.0
    for n in [30, 60]:
        vol_mean = volume.rolling(n).mean()
        vol_std = volume.rolling(n).std().replace(0, np.nan)
        df[f"volume_z_{n}m"] = (volume - vol_mean) / vol_std

    minute_of_day = df["timestamp_utc"].dt.hour * 60 + df["timestamp_utc"].dt.minute
    df["minute_sin"] = np.sin(2 * np.pi * minute_of_day / 1440.0)
    df["minute_cos"] = np.cos(2 * np.pi * minute_of_day / 1440.0)
    df["hour_sin"] = np.sin(2 * np.pi * df["timestamp_utc"].dt.hour / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["timestamp_utc"].dt.hour / 24.0)

    future_close = close.shift(-horizon_minutes)
    df["future_close"] = future_close
    df["future_return"] = np.log(future_close / close)
    df["target_up"] = (future_close > close).astype(float)

    # Remove rows where the horizon is incomplete. Feature NaNs are handled by the pipeline imputer.
    df = df[df["future_close"].notna()].reset_index(drop=True)
    return df


def make_model(model_name: str) -> Any:
    if model_name == "logistic":
        base = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.25,
                        class_weight="balanced",
                        solver="lbfgs",
                    ),
                ),
            ]
        )
        return CalibratedClassifierCV(base, method="sigmoid", cv=3)

    if model_name == "logistic_raw":
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.03,
                        class_weight=None,
                        solver="lbfgs",
                    ),
                ),
            ]
        )

    if model_name == "hgb":
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "clf",
                    HistGradientBoostingClassifier(
                        max_iter=300,
                        learning_rate=0.035,
                        max_leaf_nodes=15,
                        min_samples_leaf=80,
                        l2_regularization=0.08,
                        early_stopping=True,
                        random_state=42,
                    ),
                ),
            ]
        )

    if model_name == "extra_trees":
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "clf",
                    ExtraTreesClassifier(
                        n_estimators=350,
                        max_depth=7,
                        min_samples_leaf=60,
                        max_features=0.6,
                        class_weight="balanced_subsample",
                        n_jobs=-1,
                        random_state=42,
                    ),
                ),
            ]
        )

    raise ValueError(f"Unsupported model: {model_name}")


def chronological_split(df: pd.DataFrame, test_fraction: float, min_train_rows: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if not 0.05 <= test_fraction <= 0.5:
        raise ValueError("test_fraction must be between 0.05 and 0.5")
    split = int(len(df) * (1.0 - test_fraction))
    split = max(split, min_train_rows)
    split = min(split, len(df) - 1)
    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()
    if len(train) < min_train_rows:
        raise ValueError(f"Need at least {min_train_rows} training rows, got {len(train)}")
    if len(test) < 100:
        raise ValueError(f"Need at least 100 test rows, got {len(test)}")
    return train, test


def train_validation_split(train: pd.DataFrame, validation_fraction: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if not 0.05 <= validation_fraction <= 0.4:
        raise ValueError("validation_fraction must be between 0.05 and 0.4")
    split = int(len(train) * (1.0 - validation_fraction))
    split = min(max(split, 500), len(train) - 100)
    fit = train.iloc[:split].copy()
    validation = train.iloc[split:].copy()
    if len(validation) < 100:
        raise ValueError(f"Need at least 100 validation rows, got {len(validation)}")
    return fit, validation


def calibration_buckets(y_true: np.ndarray, p_up: np.ndarray, bucket_count: int = 10) -> List[Dict[str, Any]]:
    buckets: List[Dict[str, Any]] = []
    edges = np.linspace(0, 1, bucket_count + 1)
    for i in range(bucket_count):
        lo, hi = edges[i], edges[i + 1]
        if i == bucket_count - 1:
            mask = (p_up >= lo) & (p_up <= hi)
        else:
            mask = (p_up >= lo) & (p_up < hi)
        n = int(mask.sum())
        if n == 0:
            continue
        buckets.append(
            {
                "p_low": round(float(lo), 2),
                "p_high": round(float(hi), 2),
                "rows": n,
                "avg_pred_up": float(p_up[mask].mean()),
                "actual_up_rate": float(y_true[mask].mean()),
            }
        )
    return buckets


def threshold_slices(y_true: np.ndarray, p_up: np.ndarray, thresholds: Iterable[float]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    pred_up = p_up >= 0.5
    confidence = np.where(pred_up, p_up, 1.0 - p_up)
    correct = pred_up.astype(int) == y_true.astype(int)
    for threshold in thresholds:
        mask = confidence >= threshold
        n = int(mask.sum())
        out.append(
            {
                "confidence_threshold": float(threshold),
                "rows": n,
                "coverage": float(n / len(y_true)) if len(y_true) else 0.0,
                "accuracy": float(correct[mask].mean()) if n else None,
                "avg_confidence": float(confidence[mask].mean()) if n else None,
            }
        )
    return out


def tune_confidence_threshold(
    y_true: np.ndarray,
    p_up: np.ndarray,
    default_threshold: float,
    min_coverage: float,
) -> Dict[str, Any]:
    slices = threshold_slices(y_true, p_up, np.round(np.arange(0.50, 0.701, 0.01), 2))
    best: Optional[Dict[str, Any]] = None
    for row in slices:
        if row["rows"] < 100 or row["coverage"] < min_coverage or row["accuracy"] is None:
            continue
        edge = row["accuracy"] - 0.5
        utility = edge * row["coverage"]
        candidate = {**row, "edge": float(edge), "utility": float(utility)}
        if best is None or candidate["utility"] > best["utility"]:
            best = candidate

    if best is None or best["utility"] <= 0:
        fallback = next((r for r in slices if abs(r["confidence_threshold"] - default_threshold) < 1e-9), None)
        return {
            "threshold": float(default_threshold),
            "reason": "fallback_default_no_positive_validation_utility",
            "selected_slice": fallback,
            "all_slices": slices,
        }

    return {
        "threshold": float(best["confidence_threshold"]),
        "reason": "max_validation_edge_times_coverage",
        "selected_slice": best,
        "all_slices": slices,
    }


def evaluate_predictions(
    test: pd.DataFrame,
    p_up: np.ndarray,
    probability_threshold: float,
    thresholds: Optional[Iterable[float]] = None,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    y_true = test["target_up"].astype(int).to_numpy()
    pred_up = (p_up >= 0.5).astype(int)
    confidence = np.where(pred_up == 1, p_up, 1.0 - p_up)
    direction = np.where(pred_up == 1, "UP", "DOWN")

    predictions = test[
        ["timestamp_utc", "open", "high", "low", "close", "future_close", "future_return", "target_up"]
    ].copy()
    predictions["p_up"] = p_up
    predictions["direction"] = direction
    predictions["confidence"] = confidence
    predictions["trade_signal"] = predictions["confidence"] >= probability_threshold
    predictions["correct"] = pred_up == y_true

    metrics: Dict[str, Any] = {
        "rows": int(len(test)),
        "up_rate": float(y_true.mean()),
        "accuracy_all": float(accuracy_score(y_true, pred_up)),
        "brier_score": float(brier_score_loss(y_true, p_up)),
        "log_loss": float(log_loss(y_true, np.column_stack([1.0 - p_up, p_up]), labels=[0, 1])),
        "avg_confidence": float(confidence.mean()),
        "threshold": probability_threshold,
        "threshold_slices": threshold_slices(
            y_true,
            p_up,
            thresholds or [0.50, 0.52, 0.55, 0.58, 0.60, 0.65, 0.70],
        ),
        "calibration_buckets": calibration_buckets(y_true, p_up),
    }
    try:
        metrics["auc"] = float(roc_auc_score(y_true, p_up))
    except ValueError:
        metrics["auc"] = None

    selected = predictions[predictions["trade_signal"]]
    metrics["selected_rows"] = int(len(selected))
    metrics["selected_coverage"] = float(len(selected) / len(predictions)) if len(predictions) else 0.0
    metrics["selected_accuracy"] = float(selected["correct"].mean()) if len(selected) else None
    metrics["selected_avg_confidence"] = float(selected["confidence"].mean()) if len(selected) else None
    metrics["selected_avg_future_return_abs"] = (
        float(selected["future_return"].abs().mean()) if len(selected) else None
    )
    return predictions, metrics


def validation_candidate_result(
    model_name: str,
    model: Any,
    validation: pd.DataFrame,
    cfg: RunConfig,
) -> Dict[str, Any]:
    p_up = model.predict_proba(validation[FEATURE_COLUMNS])[:, 1]
    y_true = validation["target_up"].astype(int).to_numpy()
    threshold_info = tune_confidence_threshold(
        y_true,
        p_up,
        default_threshold=cfg.probability_threshold,
        min_coverage=cfg.min_threshold_coverage,
    )
    threshold = (
        threshold_info["threshold"]
        if cfg.threshold_mode == "auto"
        else cfg.probability_threshold
    )
    _, metrics = evaluate_predictions(validation, p_up, threshold)
    selected_acc = metrics["selected_accuracy"] or 0.0
    selected_coverage = metrics["selected_coverage"] or 0.0
    utility = (selected_acc - 0.5) * selected_coverage
    return {
        "model_name": model_name,
        "auc": metrics.get("auc"),
        "accuracy_all": metrics["accuracy_all"],
        "brier_score": metrics["brier_score"],
        "log_loss": metrics["log_loss"],
        "selected_threshold": threshold,
        "selected_accuracy": metrics["selected_accuracy"],
        "selected_coverage": metrics["selected_coverage"],
        "selected_rows": metrics["selected_rows"],
        "utility": float(utility),
        "threshold_tuning": threshold_info,
    }


def choose_model_and_threshold(
    fit: pd.DataFrame,
    validation: pd.DataFrame,
    cfg: RunConfig,
) -> Tuple[str, Any, float, List[Dict[str, Any]]]:
    candidates = ["logistic", "logistic_raw", "hgb", "extra_trees"] if cfg.model_name == "auto" else [cfg.model_name]
    results: List[Dict[str, Any]] = []
    fitted: Dict[str, Any] = {}
    for name in candidates:
        model = make_model(name)
        model.fit(fit[FEATURE_COLUMNS], fit["target_up"].astype(int))
        fitted[name] = model
        results.append(validation_candidate_result(name, model, validation, cfg))

    def sort_key(row: Dict[str, Any]) -> Tuple[float, float, float]:
        auc = row["auc"] if row["auc"] is not None else 0.5
        selected_acc = row["selected_accuracy"] if row["selected_accuracy"] is not None else 0.0
        return (row["utility"], selected_acc, auc)

    best = max(results, key=sort_key)
    return best["model_name"], fitted[best["model_name"]], float(best["selected_threshold"]), results


def train_and_backtest(features: pd.DataFrame, cfg: RunConfig) -> Tuple[Any, pd.DataFrame, Dict[str, Any]]:
    usable = features.dropna(subset=["target_up"]).copy()
    train, test = chronological_split(usable, cfg.test_fraction, cfg.min_train_rows)
    fit, validation = train_validation_split(train, cfg.validation_fraction)

    selected_model_name, _validation_model, selected_threshold, candidate_results = choose_model_and_threshold(fit, validation, cfg)
    model = make_model(selected_model_name)
    model.fit(train[FEATURE_COLUMNS], train["target_up"].astype(int))
    p_up = model.predict_proba(test[FEATURE_COLUMNS])[:, 1]
    predictions, metrics = evaluate_predictions(test, p_up, selected_threshold)
    metrics.update(
        {
            "product": cfg.product,
            "horizon_minutes": cfg.horizon_minutes,
            "feature_columns": FEATURE_COLUMNS,
            "model_name": selected_model_name,
            "requested_model_name": cfg.model_name,
            "threshold_mode": cfg.threshold_mode,
            "validation_fraction": cfg.validation_fraction,
            "min_threshold_coverage": cfg.min_threshold_coverage,
            "fit_rows": int(len(fit)),
            "validation_rows": int(len(validation)),
            "fit_start": fit["timestamp_utc"].iloc[0].isoformat(),
            "fit_end": fit["timestamp_utc"].iloc[-1].isoformat(),
            "validation_start": validation["timestamp_utc"].iloc[0].isoformat(),
            "validation_end": validation["timestamp_utc"].iloc[-1].isoformat(),
            "candidate_results": candidate_results,
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "train_start": train["timestamp_utc"].iloc[0].isoformat(),
            "train_end": train["timestamp_utc"].iloc[-1].isoformat(),
            "test_start": test["timestamp_utc"].iloc[0].isoformat(),
            "test_end": test["timestamp_utc"].iloc[-1].isoformat(),
        }
    )
    return model, predictions, metrics


def write_summary(path: Path, metrics: Dict[str, Any]) -> None:
    lines = [
        "# BTC 10m Event Model Run",
        "",
        f"- Product: `{metrics['product']}`",
        f"- Horizon: `{metrics['horizon_minutes']} minutes`",
        f"- Model: `{metrics.get('model_name', 'N/A')}`",
        f"- Train rows: `{metrics['train_rows']}` from `{metrics['train_start']}` to `{metrics['train_end']}`",
        f"- Fit rows: `{metrics.get('fit_rows', 'N/A')}`",
        f"- Validation rows: `{metrics.get('validation_rows', 'N/A')}`",
        f"- Test rows: `{metrics['test_rows']}` from `{metrics['test_start']}` to `{metrics['test_end']}`",
        f"- Test up rate: `{metrics['up_rate']:.4f}`",
        f"- Accuracy all: `{metrics['accuracy_all']:.4f}`",
        f"- AUC: `{metrics['auc']:.4f}`" if metrics.get("auc") is not None else "- AUC: `N/A`",
        f"- Brier score: `{metrics['brier_score']:.4f}`",
        f"- Average confidence: `{metrics['avg_confidence']:.4f}`",
        f"- Selected threshold: `{metrics['threshold']:.2f}`",
        f"- Selected rows: `{metrics['selected_rows']}` (`{metrics['selected_coverage']:.2%}` coverage)",
        (
            f"- Selected accuracy: `{metrics['selected_accuracy']:.4f}`"
            if metrics.get("selected_accuracy") is not None
            else "- Selected accuracy: `N/A`"
        ),
        "",
        "## Threshold Slices",
        "",
        "| Confidence >= | Rows | Coverage | Accuracy | Avg confidence |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in metrics["threshold_slices"]:
        acc = "N/A" if row["accuracy"] is None else f"{row['accuracy']:.4f}"
        avg_conf = "N/A" if row["avg_confidence"] is None else f"{row['avg_confidence']:.4f}"
        lines.append(
            f"| {row['confidence_threshold']:.2f} | {row['rows']} | {row['coverage']:.2%} | {acc} | {avg_conf} |"
        )
    lines.extend(
        [
            "",
            "## Calibration Buckets",
            "",
            "| P(up) bucket | Rows | Avg predicted up | Actual up rate |",
            "|---:|---:|---:|---:|",
        ]
    )
    for row in metrics["calibration_buckets"]:
        lines.append(
            f"| {row['p_low']:.2f}-{row['p_high']:.2f} | {row['rows']} | {row['avg_pred_up']:.4f} | {row['actual_up_rate']:.4f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_pipeline(cfg: RunConfig) -> Dict[str, Any]:
    cfg.outdir.mkdir(parents=True, exist_ok=True)

    if cfg.input_csv:
        candles = load_candles(cfg.input_csv)
    else:
        end = utc_now_floor_minute() - timedelta(minutes=2)
        start = end - timedelta(days=cfg.days)
        if cfg.source == "okx":
            candles = fetch_okx_1m_candles(cfg.product, start, end)
        elif cfg.source == "binance":
            candles = fetch_binance_1m_candles(cfg.product, start, end)
        elif cfg.source == "bitstamp":
            candles = fetch_bitstamp_1m_candles(cfg.product, start, end)
        elif cfg.source == "coinbase":
            candles = fetch_coinbase_1m_candles(cfg.product, start, end)
        else:
            raise ValueError(f"Unsupported source: {cfg.source}")

    raw_path = cfg.outdir / "data" / "btc_usd_1m.csv"
    save_candles(candles, raw_path)

    features = add_features_and_label(candles, cfg.horizon_minutes)
    features_path = cfg.outdir / "features" / "features.csv"
    features_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(features_path, index=False)

    model, predictions, metrics = train_and_backtest(features, cfg)
    model_dir = cfg.outdir / "model"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
            "horizon_minutes": cfg.horizon_minutes,
            "product": cfg.product,
            "source": cfg.source,
            "model_name": metrics.get("model_name"),
            "threshold": metrics.get("threshold"),
            "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        model_dir / "model.joblib",
    )

    backtest_dir = cfg.outdir / "backtest"
    backtest_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(backtest_dir / "predictions.csv", index=False)
    (backtest_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    write_summary(cfg.outdir / "summary.md", metrics)
    return metrics


def print_fetch_progress(rows: int, expected_rows: int, cursor: Optional[datetime]) -> None:
    if expected_rows > 0:
        pct = min(100.0, rows / expected_rows * 100.0)
        cursor_text = cursor.isoformat() if cursor else "N/A"
        print(f"fetched {rows}/{expected_rows} rows ({pct:.1f}%), oldest_cursor={cursor_text}", flush=True)
    else:
        cursor_text = cursor.isoformat() if cursor else "N/A"
        print(f"fetched {rows} rows, cursor={cursor_text}", flush=True)


def fetch_only(source: str, product: str, days: int, output_csv: Path) -> None:
    end = utc_now_floor_minute() - timedelta(minutes=2)
    start = end - timedelta(days=days)
    if source == "okx":
        candles = fetch_okx_1m_candles(
            product,
            start,
            end,
            progress=print_fetch_progress,
            checkpoint_csv=output_csv,
        )
    elif source == "binance":
        candles = fetch_binance_1m_candles(
            product,
            start,
            end,
            progress=print_fetch_progress,
            checkpoint_csv=output_csv,
        )
    elif source == "bitstamp":
        candles = fetch_bitstamp_1m_candles(
            product,
            start,
            end,
            progress=print_fetch_progress,
            checkpoint_csv=output_csv,
        )
    elif source == "coinbase":
        candles = fetch_coinbase_1m_candles(product, start, end, progress=print_fetch_progress)
    else:
        raise ValueError(f"Unsupported source: {source}")
    save_candles(candles, output_csv)
    print(f"saved {len(candles)} rows to {output_csv}", flush=True)


def load_model_bundle(model_dir: Path) -> Dict[str, Any]:
    model_path = model_dir / "model" / "model.joblib"
    if not model_path.exists():
        model_path = model_dir / "model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"No model.joblib found under {model_dir}")
    return joblib.load(model_path)


def latest_prediction(model_dir: Path, source: str, product: str, recent_minutes: int) -> Dict[str, Any]:
    bundle = load_model_bundle(model_dir)
    horizon = int(bundle.get("horizon_minutes", DEFAULT_HORIZON_MINUTES))
    end = utc_now_floor_minute() - timedelta(minutes=2)
    start = end - timedelta(minutes=max(recent_minutes, 180))
    if source == "okx":
        candles = fetch_okx_1m_candles(product, start, end)
    elif source == "binance":
        candles = fetch_binance_1m_candles(product, start, end)
    elif source == "bitstamp":
        candles = fetch_bitstamp_1m_candles(product, start, end)
    elif source == "coinbase":
        candles = fetch_coinbase_1m_candles(product, start, end)
    else:
        raise ValueError(f"Unsupported source: {source}")

    # add_features_and_label drops the final horizon rows because labels are unknown.
    # Recompute an unlabeled latest row for live inference.
    live_features = add_live_features(candles)
    row = live_features.iloc[[-1]]
    p_up = float(bundle["model"].predict_proba(row[bundle["feature_columns"]])[:, 1][0])
    direction = "UP" if p_up >= 0.5 else "DOWN"
    confidence = p_up if direction == "UP" else 1.0 - p_up
    return {
        "timestamp_utc": row["timestamp_utc"].iloc[0].isoformat(),
        "product": product,
        "source": source,
        "last_close": float(row["close"].iloc[0]),
        "horizon_minutes": horizon,
        "p_up": p_up,
        "direction": direction,
        "confidence": confidence,
    }


def add_live_features(candles: pd.DataFrame) -> pd.DataFrame:
    df = candles.copy()
    df["future_close"] = df["close"]
    df["target_up"] = 0
    features = add_features_and_label(df, horizon_minutes=1)
    # The final row is still removed by the artificial one-minute label. Build features directly by
    # appending a duplicate close one minute forward, then keep the last real candle.
    last = df.iloc[-1].copy()
    next_row = last.copy()
    next_row["timestamp_utc"] = pd.to_datetime(last["timestamp_utc"], utc=True) + pd.Timedelta(minutes=1)
    df2 = pd.concat([df, pd.DataFrame([next_row])], ignore_index=True)
    features2 = add_features_and_label(df2, horizon_minutes=1)
    return features2.iloc[:-1].reset_index(drop=True)


def positive_int(value: str) -> int:
    out = int(value)
    if out <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return out


def default_product_for_source(source: str, product: Optional[str] = None) -> str:
    if product:
        return product
    if source == "okx":
        return DEFAULT_OKX_INST_ID
    if source == "binance":
        return DEFAULT_BINANCE_SYMBOL
    if source == "bitstamp":
        return DEFAULT_BITSTAMP_PAIR
    if source == "coinbase":
        return DEFAULT_PRODUCT
    raise ValueError(f"Unsupported source: {source}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BTC 10 minute event contract model")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="fetch 1m candles and save CSV")
    fetch.add_argument("--source", choices=["okx", "binance", "bitstamp", "coinbase"], default="okx")
    fetch.add_argument("--product", help="OKX instId, Binance symbol, Bitstamp pair, or Coinbase product. Defaults by source.")
    fetch.add_argument("--days", type=positive_int, required=True)
    fetch.add_argument("--output-csv", type=Path, required=True)

    run = sub.add_parser("run", help="fetch/load candles, train, and backtest")
    run.add_argument("--source", choices=["okx", "binance", "bitstamp", "coinbase"], default="okx")
    run.add_argument("--product", help="OKX instId, Binance symbol, Bitstamp pair, or Coinbase product. Defaults by source.")
    run.add_argument("--days", type=positive_int, default=30)
    run.add_argument("--horizon-minutes", type=positive_int, default=DEFAULT_HORIZON_MINUTES)
    run.add_argument("--outdir", type=Path, required=True)
    run.add_argument("--input-csv", type=Path)
    run.add_argument("--probability-threshold", type=float, default=0.55)
    run.add_argument("--min-train-rows", type=positive_int, default=1000)
    run.add_argument("--test-fraction", type=float, default=0.30)
    run.add_argument("--validation-fraction", type=float, default=0.25)
    run.add_argument("--model", choices=["auto", "logistic", "logistic_raw", "hgb", "extra_trees"], default="logistic")
    run.add_argument("--threshold-mode", choices=["auto", "fixed"], default="auto")
    run.add_argument("--min-threshold-coverage", type=float, default=0.05)

    pred = sub.add_parser("predict", help="fetch recent candles and emit latest model prediction")
    pred.add_argument("--model-dir", type=Path, required=True)
    pred.add_argument("--source", choices=["okx", "binance", "bitstamp", "coinbase"])
    pred.add_argument("--product", help="OKX instId, Binance symbol, Bitstamp pair, or Coinbase product. Defaults from model bundle or source.")
    pred.add_argument("--recent-minutes", type=positive_int, default=240)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "fetch":
        product = default_product_for_source(args.source, args.product)
        fetch_only(args.source, product, args.days, args.output_csv)
    elif args.command == "run":
        product = default_product_for_source(args.source, args.product)
        cfg = RunConfig(
            source=args.source,
            product=product,
            days=args.days,
            horizon_minutes=args.horizon_minutes,
            outdir=args.outdir,
            input_csv=args.input_csv,
            probability_threshold=args.probability_threshold,
            min_train_rows=args.min_train_rows,
            test_fraction=args.test_fraction,
            validation_fraction=args.validation_fraction,
            model_name=args.model,
            threshold_mode=args.threshold_mode,
            min_threshold_coverage=args.min_threshold_coverage,
        )
        metrics = run_pipeline(cfg)
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
    elif args.command == "predict":
        bundle = load_model_bundle(args.model_dir)
        source = args.source or bundle.get("source") or "okx"
        product = default_product_for_source(source, args.product or bundle.get("product"))
        print(json.dumps(latest_prediction(args.model_dir, source, product, args.recent_minutes), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
