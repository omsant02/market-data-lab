from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from market_data_lab.binance.funding import load_funding
from market_data_lab.common.report import section
from market_data_lab.hyperliquid.funding import load_hl_funding

BINANCE_FILE = Path("data/binance/raw/BTCUSDT-fundingRate-2026-10.csv")
HL_FILE = Path("data/hyperliquid/raw/hyperliquid-BTC-funding-2026-10.json")
CHART_FILE = Path("data/compare/charts/funding_binance_vs_hyperliquid_oct_2026.png")

binance = load_funding(BINANCE_FILE)
hl = load_hl_funding(HL_FILE)

# one number per UTC day: the mean yearly rate (in percent) of that day's payments
binance_daily = binance.set_index("calc_time")["annualised"].resample("1D").mean() * 100
hl_daily = hl.set_index("time")["annualised"].resample("1D").mean() * 100

daily = pd.DataFrame({"binance": binance_daily, "hyperliquid": hl_daily})
daily["gap"] = daily["hyperliquid"] - daily["binance"]

section("1. First 5 days, yearly rate in percent (gap = hyperliquid minus binance)")
# both venues now have one row per day, so they line up
print(daily.head(5).round(2))

section("2. Row check (expect 31 days, 0 missing in each column)")
print(f"days: {len(daily)}")
print(daily.isna().sum())

section("3. Month summary (the two means must be 4.77 and 8.79)")
# the mean of the daily means equals the mean of all payments, because
# every day has the same number of payments
print(daily.mean().round(2))
higher = int((daily["gap"] > 0).sum())
print(f"days where hyperliquid was higher: {higher} of {len(daily)}")

section("4. Chart")
CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(daily.index, daily["binance"], label="Binance")
ax.plot(daily.index, daily["hyperliquid"], label="Hyperliquid")
ax.set_title("BTC funding, daily average, Oct 2026 (yearly rate, percent)")
ax.set_ylabel("percent per year")
ax.legend()
fig.autofmt_xdate()
fig.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
print(f"saved: {CHART_FILE}")
