from pathlib import Path

import matplotlib.pyplot as plt

from market_data_lab.binance.funding import check_funding, load_funding
from market_data_lab.common.report import section

df = load_funding(Path("data/raw/BTCUSDT-fundingRate-2026-10.csv"))

section("1. First 3 rows (rate per payment, then as a yearly figure)")
print(df[["calc_time", "last_funding_rate", "annualised"]].head(3))

section("2. Quality check (expect rows 93, duplicates 0, not_evenly_spaced 0)")
print(check_funding(df))

section("3. Yearly funding rate summary, in percent")
# multiply by 100: 0.0874 becomes 8.74
print((df["annualised"] * 100).describe())

section("4. Chart")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["calc_time"], df["annualised"] * 100)
ax.axhline(0, color="grey", linewidth=1)  # the zero line: below it, shorts pay longs
ax.set_title("BTCUSDT funding rate, annualised %, Oct 2026")
ax.set_xlabel("time (UTC)")
ax.set_ylabel("percent per year")
fig.savefig("data/funding_oct_2026.png")
plt.close(fig)
print("saved: data/funding_oct_2026.png")