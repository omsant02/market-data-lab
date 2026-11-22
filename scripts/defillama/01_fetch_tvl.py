import json
from pathlib import Path

from market_data_lab.common.report import section
from market_data_lab.defillama.api import historical_tvl

out_path = Path("data/defillama/raw/total-defi-tvl.json")
out_path.parent.mkdir(parents=True, exist_ok=True)

section("1. Fetch total DeFi TVL history (one GET request)")
rows = historical_tvl()
# the whole history since the start, one row per day
print(f"rows: {len(rows)}")
print(f"first row: {rows[0]}")
print(f"last row:  {rows[-1]}")

section("2. Save the raw reply")
with open(out_path, "w") as f:
    json.dump(rows, f)
print(f"saved: {out_path}")
