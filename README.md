# market-data-lab

Small Python scripts that fetch and explore real crypto market data
(Binance public files now; Hyperliquid and DefiLlama APIs next).
Downloaded data is never stored in this repo.

## The story in plain words

Binance publishes its historical market data as zip files on
data.binance.vision. Every file covers one symbol, one kind of data
and one month. Our scripts always follow the same steps:

1. Build the address from the symbol, the kind of data and the month.
2. Download the zip file into data/raw.
3. Unzip it. Inside is one CSV file.
4. Peek at the raw lines first. Never assume the format: the real
   files differ from what the documentation sample shows.
5. Load the CSV with pandas and turn the time numbers into real UTC times.
6. Check the data before trusting it: row count, duplicates, gaps.
7. Calculate (returns, yearly funding rates) and plot.

## Which tool does which job

| Tool | Job |
| --- | --- |
| uv | Creates the private Python environment and locks exact versions (pyproject.toml and uv.lock), so anyone gets the same setup |
| requests | Fetches a file or API reply from the internet |
| zipfile (standard library) | Unzips downloaded files |
| pandas | Loads tables, converts times, checks quality, calculates returns and yearly rates |
| matplotlib | Draws and saves charts |
| Git and GitHub | Tracks changes and publishes the code. Data and the private environment are ignored |

## Files

| File | What it does |
| --- | --- |
| binance_files.py | Toolbox: build addresses, download, unzip |
| report.py | Prints readable section dividers |
| fetch_binance_klines.py | Downloads one month of BTCUSDT 1h candles |
| klines.py | Loads candles and checks for gaps and duplicates |
| explore_klines.py | Summary of hourly returns and a price chart |
| fetch_binance_funding.py | Downloads one month of BTCUSDT funding rates |
| funding.py | Loads funding, converts to a yearly rate, checks spacing |
| explore_funding.py | Summary of yearly funding rates and a chart |

## What the data looks like

Candles (USD-M futures, 1 hour):
- Files have a header line, even though the documentation sample shows none.
- Times are milliseconds since 1970, in UTC.
- October 2026: 744 hourly rows, no gaps, no duplicates.
- A typical hourly move was about 0.35 percent.

Funding rates (BTCUSDT perpetual):
- Columns: calc_time, funding_interval_hours, last_funding_rate.
- Paid every 8 hours: 93 payments in October 2026, evenly spaced.
- A positive rate means longs pay shorts. 15 of 93 payments were negative.
- Converted to a yearly rate (rate x 3 x 365), the month averaged about
  4.8 percent, ranging from -4.5 to +10.95 percent.
- One month on one venue only, so no conclusion about carry yet.

## Run

    uv sync
    uv run python fetch_binance_klines.py
    uv run python explore_klines.py
    uv run python fetch_binance_funding.py
    uv run python explore_funding.py