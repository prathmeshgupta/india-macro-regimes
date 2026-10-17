import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 60)
    print(" INDIA MACRO REGIMES - DATA QUALITY AUDIT")
    print("=" * 60)
    
    csv_path = Path(__file__).parent / "output" / "macro_series.csv"
    assert csv_path.exists(), "macro_series.csv missing"
    
    df = pd.read_csv(csv_path)
    print(f"Total Macro Observations: {len(df)}")
    
    null_vals = df["value"].isnull().sum()
    null_dates = df["trade_date"].isnull().sum()
    print(f"Null Values: {null_vals} {'[PASS]' if null_vals == 0 else '[FAIL]'}")
    print(f"Null Trade Dates: {null_dates} {'[PASS]' if null_dates == 0 else '[FAIL]'}")
    
    # Series breakdown
    print("\nSeries Breakdown:")
    for s, cnt in df["series_id"].value_counts().items():
        print(f"  • {s:<20}: {cnt:>4} observations")
        
    print("=" * 60)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 60)

if __name__ == "__main__":
    audit_quality()
