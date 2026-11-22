import json
from pathlib import Path

import pandas as pd


def load_tvl(json_path: Path) -> pd.DataFrame:
    # open the saved reply and turn the JSON text into a Python list of dicts
    with open(json_path) as f:
        rows = json.load(f)

    df = pd.DataFrame(rows)

    # DefiLlama dates are SECONDS since 1970 (Binance and Hyperliquid use milliseconds)
    df["date"] = pd.to_datetime(df["date"], unit="s", utc=True)
    return df


def check_tvl(df: pd.DataFrame) -> dict:
    # time between each row and the row before it
    steps = df["date"].diff().dropna()
    return {
        "rows": len(df),
        "first_day": str(df["date"].iloc[0].date()),
        "last_day": str(df["date"].iloc[-1].date()),
        "duplicates": int(df["date"].duplicated().sum()),
        "not_daily": int((steps != pd.Timedelta(days=1)).sum()),
    }
