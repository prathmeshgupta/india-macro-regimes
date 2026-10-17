import argparse
import pandas as pd
from pathlib import Path
from india_macro_regimes.regime import MacroRegimeEvaluator

def main():
    parser = argparse.ArgumentParser(description="India Macro Regimes & Risk-Free Hurdle Agent")
    parser.add_argument("--vix", action="store_true", help="Inspect latest India VIX reading & regime")
    args = parser.parse_args()

    csv_path = Path(__file__).parent / "output" / "macro_series.csv"
    if not csv_path.exists():
        print("Output file not found.")
        return

    df = pd.read_csv(csv_path)
    if args.vix:
        vix_rows = df[df["series_id"] == "INDIA_VIX"].sort_values("trade_date", ascending=False)
        if not vix_rows.empty:
            latest = vix_rows.iloc[0]
            val = float(latest["value"])
            regime = MacroRegimeEvaluator.classify_vix(val)
            print(f"\n--- India VIX Status as of {latest['trade_date']} ---")
            print(f"  • Level: {val:.2f}")
            print(f"  • Regime: {regime}")
    else:
        print(f"Loaded {len(df)} macro observations. Use --vix to inspect current volatility regime.")

if __name__ == "__main__":
    main()
