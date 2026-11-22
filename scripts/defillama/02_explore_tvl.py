from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from market_data_lab.common.report import section
from market_data_lab.defillama.tvl import check_tvl, load_tvl

RAW_FILE = Path("data/defillama/raw/total-defi-tvl.json")
CHART_FILE = Path("data/defillama/charts/total_tvl_oct_2026.png")

df = load_tvl(RAW_FILE)

section("1. Last 3 rows (date is readable, in UTC; tvl is dollars)")
print(df.tail(3))

section("2. Column types (tvl should be a number, date a UTC datetime)")
print(df.dtypes)

section("3. Quality check on the whole history (expect duplicates 0, not_daily 0)")
# a not_daily above 0 would be a finding: some days are missing
print(check_tvl(df))

# keep only October 2026, to match the other sources
start = pd.Timestamp("2026-10-01", tz="UTC")
end = pd.Timestamp("2026-11-01", tz="UTC")
oct_df = df[(df["date"] >= start) & (df["date"] < end)].copy()
oct_df["tvl_billions"] = oct_df["tvl"] / 1e9

section("4. October 2026 summary (expect 31 days), in billions of dollars")
first = oct_df["tvl_billions"].iloc[0]
last = oct_df["tvl_billions"].iloc[-1]
print(f"days: {len(oct_df)}")
print(f"first day: {first:.2f}")
print(f"last day:  {last:.2f}")
print(f"change over the month: {(last / first - 1) * 100:.2f} percent")
print(f"lowest: {oct_df['tvl_billions'].min():.2f}")
print(f"highest: {oct_df['tvl_billions'].max():.2f}")

section("5. Chart")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(oct_df["date"], oct_df["tvl_billions"])
ax.set_title("Total DeFi TVL, Oct 2026 (billions of dollars)")
ax.set_ylabel("billions of dollars")
fig.autofmt_xdate()
CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
print(f"saved: {CHART_FILE}")
