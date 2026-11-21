# market-data-lab

Small Python scripts that fetch and explore real crypto market data
(Binance public files now; Hyperliquid and DefiLlama APIs next).
Downloaded data is never stored in this repo.

## The story in plain words

Binance publishes its historical market data as zip files on
data.binance.vision. Every file covers one symbol, one kind of data
and one month. Our scripts always follow the same steps:

1. Build the address. The address is made of the symbol (BTCUSDT),
   the kind of data (candles or funding) and the month (2026-10).
2. Download the zip file into data/raw.
3. Unzip it. Inside is one CSV file.
4. Peek at the raw lines first. Never assume the format: the real
   files differ from what the documentation sample shows.
5. Load the CSV with pandas and turn the time numbers into real
   UTC times.
6. Check the data before trusting it: row count, duplicates, gaps.
7. Calculate and plot (hourly returns for candles).

## Files

| File | What it does |
| --- | --- |
| binance_files.py | Toolbox: build addresses, download, unzip |
| fetch_binance_klines.py | Downloads one month of BTCUSDT 1h candles |
| klines.py | Loads candles into pandas and checks for gaps and duplicates |
| explore_klines.py | Prints a summary of hourly returns and saves a price chart |
| fetch_binance_funding.py | Downloads one month of BTCUSDT funding rates |

## What the data looks like

Candles (futures, 1 hour):
- Files have a header line, even though the documentation sample shows none.
- Times are milliseconds since 1970, in UTC.
- October 2026: 744 hourly rows, no gaps, no duplicates.
- A typical hourly move was about 0.35 percent.

Funding rates (perpetual futures):
- Columns: calc_time, funding_interval_hours, last_funding_rate.
- Paid every 8 hours, so about 93 rows in a 31-day month.
- A positive rate means longs pay shorts.
- A rate of 0.00007981 per payment, if it stayed constant for a year,
  is about 8.7 percent a year (0.00007981 x 3 x 365).

## Run

    uv sync
    uv run python fetch_binance_klines.py
    uv run python explore_klines.py
    uv run python fetch_binance_funding.py