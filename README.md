# India Macro Regimes, Risk-Free Hurdle Rates & Volatility Gating

Indian macroeconomic risk-free benchmarks (Reserve Bank of India Repo Rate history, 91-day T-Bill yields, G-Sec yields, LiquidBeES returns) and India VIX (`^INDIAVIX`) volatility regime state models for systematic strategies.

Companion repository to [`prathmeshgupta/nifty-pit-universe`](https://github.com/prathmeshgupta/nifty-pit-universe).

---

## 📊 Summary of Datasets

All processed datasets are saved in [`output/`](output/):

| Dataset | Observations | Series Covered | Formats |
| :--- | :---: | :--- | :--- |
| **Macro Series** | **752** | RBI Repo, India VIX, LiquidBeES, US 10Y | [`macro_series.parquet`](output/macro_series.parquet), [`macro_series.csv`](output/macro_series.csv) |

---

## 💡 Why This Exists: The Hurdle Rate & Regime Shift Trap

In absolute momentum and systematic dual-momentum portfolios (such as Vriksha Dual Momentum and Smallcase mandates), cash-defense rules dictate when to exit equities and allocate to safe assets:
1. **The Arbitrary Hurdle Problem**: Comparing an asset's 6-month or 12-month return against zero ("positive nominal return") ignores the cost of capital. In India, where the risk-free rate historically oscillated between $4.0\%\text{--}8.5\%$, an asset returning $+2\%$ is an economic loss compared to parking cash in overnight TREPS or LiquidBeES.
2. **Volatility Regime Gates**: During market crashes (e.g. March 2020), volatility spikes preceding trend breakdowns. By monitoring India VIX regimes ($<15$ bull regime, $15\text{--}22$ normal, $>22$ elevated drawdown risk), systematic models can activate defensive EMA trailing gates or portfolio-level hedging.

This dataset provides the historical ground truth for macroeconomic hurdle rates and volatility thresholds.

---

## 🧱 Data Schema

### `macro_series`
| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `series_id` | String | Macro series code | `INDIA_VIX` |
| `trade_date` | Date | Observation date | `2026-10-16` |
| `value` | Float | Closing index level, rate, or price | `14.06` |
| `high` | Float | Intraday high | `14.50` |
| `low` | Float | Intraday low | `13.80` |
| `source` | String | Source attribution | `YFINANCE_VIX` |

---

## 🔍 How to Query

### 1. Using Python & Pandas
```python
import pandas as pd

df = pd.read_parquet("output/macro_series.parquet")

# Inspect historical RBI Repo rate changes
repo = df[df["series_id"] == "RBI_REPO_RATE"].sort_values("trade_date", ascending=False)
print("Latest Effective RBI Repo Rates:")
print(repo[["trade_date", "value"]])
```

### 2. Using the CLI Helper
```bash
python runner.py --vix
```

---

## 🧪 Quality Audit
```bash
python evaluate_quality.py
```
* **Series Integrity**: 0 null values, 0 null dates ([PASS]).
* **Coverage**: Complete 1-year India VIX bars and full RBI policy cycle ([PASS]).

---

## 📄 License
MIT License. Copyright (c) 2026 Prathmesh Gupta.
