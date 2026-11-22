import pandas as pd

from market_data_lab.binance.funding import check_funding


def make_df(times, rates):
    # a tiny funding table with only the two columns the check needs
    return pd.DataFrame(
        {
            "calc_time": pd.to_datetime(times, utc=True),
            "last_funding_rate": rates,
        }
    )


def test_clean_data_has_no_problems():
    df = make_df(
        ["2026-10-01 00:00", "2026-10-01 08:00", "2026-10-01 16:00"],
        [0.0001, 0.00005, 0.00007],
    )
    assert check_funding(df) == {
        "rows": 3,
        "duplicates": 0,
        "not_evenly_spaced": 0,
        "negative_rates": 0,
    }


def test_duplicate_time_is_counted():
    # 08:00 appears twice: one duplicate, and the 0-hour step is also uneven
    df = make_df(
        ["2026-10-01 00:00", "2026-10-01 08:00", "2026-10-01 08:00"],
        [0.0001, 0.0001, 0.0001],
    )
    result = check_funding(df)
    assert result["duplicates"] == 1
    assert result["not_evenly_spaced"] == 1


def test_missing_payment_is_counted():
    # 08:00 is missing, so the step from 00:00 to 16:00 is 16 hours, not 8
    df = make_df(["2026-10-01 00:00", "2026-10-01 16:00"], [0.0001, 0.0001])
    assert check_funding(df)["not_evenly_spaced"] == 1


def test_negative_rates_are_counted():
    df = make_df(
        ["2026-10-01 00:00", "2026-10-01 08:00", "2026-10-01 16:00"],
        [-0.0001, 0.0001, -0.00005],
    )
    assert check_funding(df)["negative_rates"] == 2
