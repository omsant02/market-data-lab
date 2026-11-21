# market-data-lab

Small Python scripts that fetch and explore real crypto market data:
Binance public files and the Hyperliquid API now, DefiLlama next.
Downloaded data is never stored in this repo.

## The story in plain words

There are two ways we get data, and the scripts follow the same habits for both.

Binance publishes historical data as zip files on data.binance.vision.
Every file covers one symbol, one kind of data and one month:

1. Build the address from the symbol, the kind of data and the month.
2. Download the zip file into data/raw.
3. Unzip it. Inside is one CSV file.
4. Peek at the raw lines first. Never assume the format: the real
   files differ from what the documentation sample shows.
5. Load the CSV with pandas and turn the time numbers into real UTC times.
6. Check the data before trusting it: row count, duplicates, gaps.
7. Calculate (returns, yearly funding rates) and plot.

Hyperliquid has no files to download. We ask its API instead:

1. Send one POST request to https://api.hyperliquid.xyz/info with a small
   JSON message saying what we want (type, coin, start and end time).
2. The reply is JSON: a list of rows. One request returns a limited
   number of rows, so we ask again starting 1 millisecond after the last
   row we received, until the month is covered (pagination).
3. Numbers such as the funding rate arrive as text (for example
   "0.0000125"), so they must be converted to numbers before any maths.
4. Save the raw reply to data/raw, then load and check it like the
   Binance data.

A browser address bar sends GET requests. This endpoint expects POST,
so opening the address in a browser shows an error. That is expected.

## Which tool does which job

| Tool | Job |
| --- | --- |
| uv | Creates the private Python environment and locks exact versions (pyproject.toml and uv.lock), so anyone gets the same setup |
| requests | Fetches a file or API reply from the internet |
| zipfile (standard library) | Unzips downloaded files |
| json (standard library) | Saves and reads the raw API replies |
| pandas | Loads tables, converts times, checks quality, calculates returns and yearly rates |
| matplotlib | Draws and saves charts |
| Git and GitHub | Tracks changes and publishes the code. Data and the private environment are ignored |

## Layout

    src/market_data_lab/   library code, imported by the scripts
    scripts/               the things you run
    data/                  downloaded data (ignored by git)

The library is installed into the project environment by uv
(see the build-system section in pyproject.toml), so scripts import it
with `from market_data_lab.klines import load_klines`.

## Files

| File | What it does |
| --- | --- |
| src/market_data_lab/binance_files.py | Toolbox: build addresses, download, unzip |
| src/market_data_lab/klines.py | Loads candles and checks for gaps and duplicates |
| src/market_data_lab/funding.py | Loads Binance funding, converts to a yearly rate, checks spacing |
| src/market_data_lab/hyperliquid_api.py | Toolbox: month boundaries, POST requests, paged funding history |
| src/market_data_lab/report.py | Prints readable section dividers |
| scripts/fetch_binance_klines.py | Downloads one month of BTCUSDT 1h candles |
| scripts/explore_klines.py | Summary of hourly returns and a price chart |
| scripts/fetch_binance_funding.py | Downloads one month of BTCUSDT funding rates |
| scripts/explore_funding.py | Summary of yearly funding rates and a chart |
| scripts/fetch_hyperliquid_funding.py | Fetches one month of BTC funding history and saves the raw JSON |

## What the data looks like

Candles (Binance USD-M futures, 1 hour):
- Files have a header line, even though the documentation sample shows none.
- Times are milliseconds since 1970, in UTC.
- October 2026: 744 hourly rows, no gaps, no duplicates.
- A typical hourly move was about 0.35 percent.

Funding rates (Binance BTCUSDT perpetual):
- Columns: calc_time, funding_interval_hours, last_funding_rate.
- Paid every 8 hours: 93 payments in October 2026, evenly spaced.
- A positive rate means longs pay shorts. 15 of 93 payments were negative.
- Converted to a yearly rate (rate x 3 x 365), the month averaged about
  4.8 percent, ranging from -4.5 to +10.95 percent.
- One month on one venue only, so no conclusion about carry yet.

Funding rates (Hyperliquid BTC, fetched from the API):
- October 2026: 744 rows, one per hour. Each row has coin, fundingRate,
  premium and time.
- fundingRate and premium arrive as text; time is a number in milliseconds.
- Not analysed yet. Because payments are hourly, the yearly rate is
  rate x 24 x 365 (Binance pays every 8 hours, so it uses x 3 x 365).

## Next steps

- Load the Hyperliquid funding, convert the text to numbers, check it.
- Compare Hyperliquid and Binance funding for October 2026.
- Add a DefiLlama script (a GET request).
- Add tests (pytest) for the quality checks.
- Redo the analysis in Polars, then explore the same files with SQL in DuckDB.

## Run

Run these from the repo root.

    uv sync
    uv run python scripts/fetch_binance_klines.py
    uv run python scripts/explore_klines.py
    uv run python scripts/fetch_binance_funding.py
    uv run python scripts/explore_funding.py
    uv run python scripts/fetch_hyperliquid_funding.py
