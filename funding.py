from pathlib import Path

import pandas as pd


def load_funding(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # millisecond count -> real UTC time, rounded to the nearest second
    df["calc_time"] = pd.to_datetime(df["calc_time"], unit="ms", utc=True).dt.round("1s")
    # payments per day = 24 hours / hours between payments (3 for 8-hour funding)
    payments_per_day = 24 / df["funding_interval_hours"]
    df["annualised"] = df["last_funding_rate"] * payments_per_day * 365
    return df


def check_funding(df: pd.DataFrame, hours: int = 8) -> dict:
    steps = df["calc_time"].diff().dropna()
    return {
        "rows": len(df),
        "duplicates": int(df["calc_time"].duplicated().sum()),
        "not_evenly_spaced": int((steps != pd.Timedelta(hours=hours)).sum()),
        "negative_rates": int((df["last_funding_rate"] < 0).sum()),
    }