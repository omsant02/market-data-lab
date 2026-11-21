import json
from pathlib import Path

from market_data_lab.hyperliquid.api import funding_history, month_bounds_ms
from market_data_lab.common.report import section

coin = "BTC"
year, month = 2026, 10
out_path = Path(f"data/raw/hyperliquid-{coin}-funding-{year}-{month:02d}.json")

start_ms, end_ms = month_bounds_ms(year, month)

section("1. Time window we ask for (milliseconds since 1970, UTC)")
print("start:", start_ms)
print("end:  ", end_ms)

rows = funding_history(coin, start_ms, end_ms)

section("2. How many rows came back (expect 744 for a 31-day month, hourly)")
print("rows:", len(rows))

section("3. First 3 rows, exactly as the server sent them")
for row in rows[:3]:
    print(row)

section("4. Last row")
print(rows[-1])

out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    json.dump(rows, f)

section("5. Saved")
print(out_path)