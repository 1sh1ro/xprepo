# CEX 二级市场月度报告生成器

根据 CoinMarketCap (CMC) 与 CoinGecko (CG) 数据生成月度报告与图表。

新增：`scripts/cex_report_agent.py` 支持每日与每月报告，输出 HTML + PDF，并接入 Deribit 公共 API。

## 依赖
- Python 3.9+
- matplotlib（已安装）
- reportlab（用于 PDF 输出）

## 使用
建议使用环境变量传入 API Key（避免写入文件）：

```bash
export COINGECKO_API_KEY="你的_coingecko_key"
export CMC_API_KEY="你的_cmc_key"

python3 scripts/cex_monthly_report.py --month 2026-01
```

每日与每月（HTML + PDF）：

```bash
# 每日（默认昨天 UTC）
python3 scripts/cex_report_agent.py --mode daily

# 指定日期
python3 scripts/cex_report_agent.py --mode daily --date 2026-02-15

# 每月（默认上一个完整月）
python3 scripts/cex_report_agent.py --mode monthly

# 指定月份
python3 scripts/cex_report_agent.py --mode monthly --month 2026-01
```

可选参数：
- `--start YYYY-MM-DD --end YYYY-MM-DD` 指定区间
- `--month YYYY-MM` 指定月份（默认上一个完整月份）
- `--outdir` 输出目录（默认 `reports/`）
- `--cg-plan pro|demo|public` 指定 CoinGecko 套餐（免费版用 `demo`）
- `--deribit-base` 指定 Deribit Base URL（默认生产环境）

输出：
- `reports/<YYYY-MM>/cex_monthly_report.md`
- `reports/<YYYY-MM>/cex_monthly_charts.png`

Agent 输出：
- `reports/daily/<YYYY-MM-DD>/report.html`
- `reports/daily/<YYYY-MM-DD>/report.pdf`
- `reports/daily/<YYYY-MM-DD>/charts/*.png`
- `reports/monthly/<YYYY-MM>/report.html`
- `reports/monthly/<YYYY-MM>/report.pdf`
- `reports/monthly/<YYYY-MM>/charts/*.png`

## 说明
- 若 CMC 历史数据不可用，会自动回退使用 CoinGecko 的总市值/成交量序列。
- BTC 统治力的月度序列依赖 CMC 历史数据；若不可用，会仅展示最新值。
- 若 CoinGecko Pro 访问失败，会自动回退到公开 API（可能限频或受限）。
