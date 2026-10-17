import io
import pandas as pd
from typing import Optional

class MacroFetcher:
    """Fetches benchmark RBI policy rates, India VIX daily bars, and cash equivalents."""

    @staticmethod
    def fetch_rbi_repo_rates() -> pd.DataFrame:
        repo_schedule = [
            ("2020-03-27", 4.40),
            ("2020-05-22", 4.00),
            ("2022-05-04", 4.40),
            ("2022-06-08", 4.90),
            ("2022-08-05", 5.40),
            ("2022-09-30", 5.90),
            ("2022-12-07", 6.25),
            ("2023-02-08", 6.50),
        ]
        records = []
        for dt, rate in repo_schedule:
            records.append({
                "series_id": "RBI_REPO_RATE",
                "trade_date": dt,
                "value": rate,
                "source": "RBI_POLICY_CIRCULAR"
            })
        return pd.DataFrame(records)

    @staticmethod
    def fetch_india_vix(period: str = "1y") -> pd.DataFrame:
        import yfinance as yf
        t = yf.Ticker("^INDIAVIX")
        hist = t.history(period=period)
        records = []
        for dt, row in hist.iterrows():
            records.append({
                "series_id": "INDIA_VIX",
                "trade_date": dt.strftime("%Y-%m-%d"),
                "value": float(row["Close"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "source": "YFINANCE_VIX"
            })
        return pd.DataFrame(records)
