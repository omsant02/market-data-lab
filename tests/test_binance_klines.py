import pandas as pd

from market_data_lab.binance.klines import check_hourly


def make_df(times):
    # a tiny candle table with only the column the check needs
    return pd.DataFrame({"open_time": pd.to_datetime(times, utc=True)})


def test_clean_hours_have_no_problems():
    df = make_df(["2026-10-01 00:00", "2026-10-01 01:00", "2026-10-01 02:00"])
    assert check_hourly(df) == {"rows": 3, "duplicates": 0, "gaps": 0}


def test_missing_hour_is_a_gap():
    # 02:00 is missing, so the step from 01:00 to 03:00 is 2 hours
    df = make_df(["2026-10-01 00:00", "2026-10-01 01:00", "2026-10-01 03:00"])
    assert check_hourly(df)["gaps"] == 1


def test_duplicate_hour_is_counted():
    df = make_df(["2026-10-01 00:00", "2026-10-01 01:00", "2026-10-01 01:00"])
    assert check_hourly(df)["duplicates"] == 1
