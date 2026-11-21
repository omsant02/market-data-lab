from pathlib import Path

import matplotlib.pyplot as plt

from market_data_lab.hyperliquid.funding import check_hl_funding, load_hl_funding
from market_data_lab.common.report import section

RAW_FILE = Path("data/hyperliquid/raw/hyperliquid-BTC-funding-2026-10.json")
CHART_FILE = Path("data/hyperliquid/charts/funding_oct_2026.png")

df = load_hl_funding(RAW_FILE)

section("1. First 3 rows (time is readable, in UTC)")
# shows the converted time and the numbers as real numbers
print(df[["time", "funding_rate", "premium", "annualised"]].head(3))

section("2. Column types (rates should be float64, not object)")
# 'object' here would mean the text was never converted
print(df.dtypes)

section("3. Quality check (expect rows 744, duplicates 0, not_evenly_spaced 0)")
# negative_rates is a finding, not an error
print(check_hl_funding(df))

section("4. Yearly funding rate summary, in percent")
# annualised is a fraction, so * 100 gives percent
print((df["annualised"] * 100).describe())

section("5. Chart")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["time"], df["annualised"] * 100)
ax.set_title("Hyperliquid BTC funding, Oct 2026 (yearly rate, percent)")
ax.set_ylabel("percent per year")
fig.autofmt_xdate()
CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
print(f"saved: {CHART_FILE}")
