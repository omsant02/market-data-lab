import json

import pandas as pd

from market_data_lab.defillama.tvl import check_tvl, load_tvl


def write_json(tmp_path, rows):
    path = tmp_path / "tvl.json"
    path.write_text(json.dumps(rows))
    return path


def test_load_reads_dates_as_seconds(tmp_path):
    # 1790812800 SECONDS is 1 Oct 2026, 00:00 UTC (milliseconds would give 1970)
    path = write_json(tmp_path, [{"date": 1790812800, "tvl": 100}])
    df = load_tvl(path)
    assert df["date"].iloc[0] == pd.Timestamp("2026-10-01", tz="UTC")


def test_check_finds_a_missing_day(tmp_path):
    # days 1, 2 and 4: day 3 is missing, so one step is 2 days long
    rows = [
        {"date": 1790812800, "tvl": 100},
        {"date": 1790899200, "tvl": 101},
        {"date": 1791072000, "tvl": 102},
    ]
    df = load_tvl(write_json(tmp_path, rows))
    assert check_tvl(df) == {
        "rows": 3,
        "first_day": "2026-10-01",
        "last_day": "2026-10-04",
        "duplicates": 0,
        "not_daily": 1,
    }
