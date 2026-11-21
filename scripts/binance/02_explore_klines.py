from pathlib import Path

import matplotlib.pyplot as plt

from market_data_lab.binance.klines import check_hourly, load_klines


def section(title: str) -> None:
    # prints a blank line, a divider, the title, and another divider
    print()
    print("-" * 50)
    print(title)
    print("-" * 50)


# load the October file: times become readable, useless column removed
df = load_klines(Path("data/binance/raw/BTCUSDT-1h-2026-10.csv"))

section("1. First 3 rows (time is readable, in UTC)")
# we pick 4 columns so the table is not cut off with "..."
print(df[["open_time", "open", "close", "volume"]].head(3))

section("2. Column types (prices should be float64, count int64)")
print(df.dtypes)

section("3. Quality check (expect rows 744, duplicates 0, gaps 0)")
print(check_hourly(df))

# hourly return as a fraction, e.g. 0.0035 means +0.35 percent
df["return"] = df["close"].pct_change()

section("4. Hourly return summary, in percent (743 values, 1st hour has none)")
# multiply by 100 to turn fractions into percent
print((df["return"] * 100).describe())

section("5. Chart")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["open_time"], df["close"])
ax.set_title("BTCUSDT close, 1h candles, Oct 2026")
ax.set_xlabel("time (UTC)")
ax.set_ylabel("close")
Path("data/binance/charts").mkdir(parents=True, exist_ok=True)
fig.savefig("data/binance/charts/close_oct_2026.png")
plt.close(fig)
print("saved: data/binance/charts/close_oct_2026.png")