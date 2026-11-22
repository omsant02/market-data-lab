import json

import pandas as pd
import pytest

from market_data_lab.hyperliquid.funding import check_hl_funding, load_hl_funding

# two rows shaped like the real API reply: numbers as text, times with noise
ROWS = [
    {"coin": "BTC", "fundingRate": "0.0000125", "premium": "-0.0000947", "time": 1790812800051},
    {"coin": "BTC", "fundingRate": "-0.0001", "premium": "0.0002", "time": 1790816400041},
]


def write_json(tmp_path):
    # tmp_path is a throwaway folder that pytest creates for each test
    path = tmp_path / "hl.json"
    path.write_text(json.dumps(ROWS))
    return path


def test_load_converts_text_to_numbers(tmp_path):
    df = load_hl_funding(write_json(tmp_path))
    assert df["funding_rate"].dtype == "float64"
    assert df["funding_rate"].iloc[0] == pytest.approx(0.0000125)
    # 0.0000125 * 24 * 365 = 0.1095
    assert df["annualised"].iloc[0] == pytest.approx(0.1095)


def test_load_rounds_time_noise_away(tmp_path):
    df = load_hl_funding(write_json(tmp_path))
    assert df["time"].iloc[0] == pd.Timestamp("2026-10-01 00:00:00", tz="UTC")
    assert df["time"].iloc[1] == pd.Timestamp("2026-10-01 01:00:00", tz="UTC")


def test_check_counts_negative_rates(tmp_path):
    df = load_hl_funding(write_json(tmp_path))
    assert check_hl_funding(df) == {
        "rows": 2,
        "duplicates": 0,
        "not_evenly_spaced": 0,
        "negative_rates": 1,
    }
