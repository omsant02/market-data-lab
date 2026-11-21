from pathlib import Path

import pandas as pd


def load_klines(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
    return df.drop(columns=["ignore"])


def check_hourly(df: pd.DataFrame) -> dict:
    steps = df["open_time"].diff().dropna()
    return {
        "rows": len(df),
        "duplicates": int(df["open_time"].duplicated().sum()),
        "gaps": int((steps != pd.Timedelta(hours=1)).sum()),
    }