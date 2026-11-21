import json
from pathlib import Path

import pandas as pd


def load_hl_funding(json_path: Path) -> pd.DataFrame:
    # open the saved reply and turn the JSON text into a Python list of dicts
    with open(json_path) as f:
        rows = json.load(f)

    df = pd.DataFrame(rows)
    df = df.rename(columns={"fundingRate": "funding_rate"})

    # the API sends these numbers as text, so convert them to real numbers
    df["funding_rate"] = df["funding_rate"].astype(float)
    df["premium"] = df["premium"].astype(float)

    # milliseconds since 1970 -> UTC time, rounded to whole seconds
    # (the API adds a few milliseconds of noise, like 00:00:00.051)
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True).dt.round("1s")

    # payments are hourly, so a year has 24 * 365 payments
    df["annualised"] = df["funding_rate"] * 24 * 365
    return df


def check_hl_funding(df: pd.DataFrame, hours: int = 1) -> dict:
    # time between each row and the row before it
    steps = df["time"].diff().dropna()
    return {
        "rows": len(df),
        "duplicates": int(df["time"].duplicated().sum()),
        "not_evenly_spaced": int((steps != pd.Timedelta(hours=hours)).sum()),
        "negative_rates": int((df["funding_rate"] < 0).sum()),
    }
