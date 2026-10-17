"""India Macro Regimes & Risk-Free Hurdle Weekly Dataset Updater.

Fetches updated RBI Policy Repo Rates, India VIX daily volatility bars,
US 10Y benchmark yields, and cash equivalent ETF bars (LIQUIDBEES),
deduplicating observations and writing to both CSV and Apache Parquet.
"""

import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add local src to path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from india_macro_regimes.fetcher import MacroFetcher

def update_macro_regimes():
    print(f"[{datetime.now().isoformat()}] Starting India Macro Regimes dataset update...")
    fetcher = MacroFetcher()
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "macro_series.csv"
    parquet_file = output_dir / "macro_series.parquet"

    existing_df = pd.DataFrame()
    if csv_file.exists():
        existing_df = pd.read_csv(csv_file)
        print(f"Loaded {len(existing_df)} existing records from {csv_file.name}")

    series_dfs = []

    # 1. RBI Repo Rates
    try:
        print("Fetching RBI repo rate policy milestones...")
        df_repo = fetcher.fetch_rbi_repo_rates()
        if not df_repo.empty:
            series_dfs.append(df_repo)
    except Exception as e:
        print(f"Warning: Failed to fetch RBI repo rates: {e}")

    # 2. India VIX
    try:
        print("Fetching India VIX series...")
        df_vix = fetcher.fetch_india_vix(period="1y")
        if not df_vix.empty:
            series_dfs.append(df_vix)
    except Exception as e:
        print(f"Warning: Failed to fetch India VIX: {e}")

    # 3. US 10Y Yield
    try:
        print("Fetching US 10Y Yield series...")
        df_us10y = fetcher.fetch_us_10y(period="1y")
        if not df_us10y.empty:
            series_dfs.append(df_us10y)
    except Exception as e:
        print(f"Warning: Failed to fetch US 10Y Yield: {e}")

    # 4. Cash Equivalent (LIQUIDBEES)
    try:
        print("Fetching LIQUIDBEES cash proxy series...")
        df_liq = fetcher.fetch_liquidbees(period="1y")
        if not df_liq.empty:
            series_dfs.append(df_liq)
    except Exception as e:
        print(f"Warning: Failed to fetch LIQUIDBEES: {e}")

    if not series_dfs and existing_df.empty:
        raise RuntimeError("No macro series retrieved and no existing data available.")

    combined = list(series_dfs)
    if not existing_df.empty:
        combined.insert(0, existing_df)

    merged = pd.concat(combined, ignore_index=True)

    # Ensure required columns
    for col in ["high", "low"]:
        if col not in merged.columns:
            merged[col] = merged["value"]

    # Drop any nulls in core keys
    merged = merged.dropna(subset=["series_id", "trade_date", "value"])

    # Deduplicate on series_id and trade_date
    merged = merged.drop_duplicates(subset=["series_id", "trade_date"], keep="last")

    # Sort deterministically
    merged = merged.sort_values(by=["trade_date", "series_id"], ascending=[False, True]).reset_index(drop=True)

    if "created_at" not in merged.columns or merged["created_at"].isnull().any():
        merged["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save
    merged.to_csv(csv_file, index=False)
    merged.to_parquet(parquet_file, index=False)

    print(f"Saved {len(merged)} macro observations to {csv_file.name} and {parquet_file.name}")

    # Audit quality
    from evaluate_quality import audit_quality
    audit_quality()
    print("India Macro Regimes update completed successfully.")

if __name__ == "__main__":
    update_macro_regimes()
