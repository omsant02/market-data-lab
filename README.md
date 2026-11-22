# market-data-lab

Small Python scripts that fetch and explore real crypto market data:
Binance public files, the Hyperliquid API and DefiLlama.
Downloaded data is never stored in this repo.

## The story in plain words

There are two ways we get data, and the scripts follow the same habits
for both.

Binance publishes historical data as zip files on data.binance.vision.
Every file covers one symbol, one kind of data and one month:

1. Build the address from the symbol, the kind of data and the month.
2. Download the zip file into data/binance/raw.
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
   "0.0000125"), so they are converted to numbers before any maths.
4. Save the raw reply to data/hyperliquid/raw, then load and check it
   like the Binance data.

A browser address bar sends GET requests. This endpoint expects POST,
so opening the address in a browser shows an error. That is expected.

DefiLlama is a third way: a plain GET request. It is just an address with
no message body, so a browser can open it too. The reply is a list of
days with a TVL value for each. Its dates are in seconds, not
milliseconds like the other two sources.

## Layout

    src/market_data_lab/     library code, imported by the scripts
      common/                shared helpers (readable printing)
      binance/               address building, loading and checking Binance data
      hyperliquid/           API requests, loading and checking Hyperliquid data
      defillama/             GET request, loading and checking DefiLlama data
    scripts/                 the things you run, numbered in flow order
      binance/
      hyperliquid/
      defillama/
      compare/               scripts that use more than one source
    tests/                   automatic checks (pytest) on tiny tables with known answers
    data/                    downloaded data and charts, grouped by source
                             (ignored by git)

Library files have plain names because Python cannot import a name that
starts with a digit. Scripts are only run, never imported, so their
numbers show the order of the flow: fetch first, then explore.

The library is installed into the project environment by uv
(see the build-system section in pyproject.toml), so scripts import it
with lines like `from market_data_lab.binance.klines import load_klines`.

## Which tool does which job

| Tool | Job |
| --- | --- |
| uv | Creates the private Python environment and locks exact versions (pyproject.toml and uv.lock), so anyone gets the same setup |
| requests | Fetches a file or API reply from the internet |
| zipfile (standard library) | Unzips downloaded files |
| json (standard library) | Saves and reads the raw API replies |
| pandas | Loads tables, converts times, checks quality, calculates returns and yearly rates |
| matplotlib | Draws and saves charts |
| pytest | Runs the automatic checks in tests/ |
| Git and GitHub | Tracks changes and publishes the code. Data and the private environment are ignored |

## Scripts, in flow order

| Script | What it does |
| --- | --- |
| scripts/binance/01_fetch_klines.py | Downloads one month of BTCUSDT 1h candles |
| scripts/binance/02_explore_klines.py | Loads and checks candles, hourly return summary, price chart |
| scripts/binance/03_fetch_funding.py | Downloads one month of BTCUSDT funding rates |
| scripts/binance/04_explore_funding.py | Loads and checks funding, yearly rate summary, chart |
| scripts/hyperliquid/01_fetch_funding.py | Fetches one month of BTC funding history, saves the raw JSON |
| scripts/hyperliquid/02_explore_funding.py | Loads and checks it, converts text to numbers, summary, chart |
| scripts/compare/01_funding_binance_vs_hyperliquid.py | Daily average yearly funding of both venues side by side, the gap, a chart |
| scripts/defillama/01_fetch_tvl.py | Downloads the daily history of total DeFi TVL, saves the raw JSON |
| scripts/defillama/02_explore_tvl.py | Loads and checks it, October 2026 summary, chart |

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

Funding rates (Hyperliquid BTC, from the API):
- October 2026: 744 rows, exactly one per hour, no duplicates, no gaps.
- fundingRate and premium arrive as text; time is a number in milliseconds
  (with a few milliseconds of noise, rounded away).
- Converted to a yearly rate (rate x 24 x 365), the month averaged about
  8.8 percent, ranging from -12.2 to +10.95 percent.
- 46 of 744 payments were negative. More than half of all hours sat at
  exactly 10.95 percent a year (0.0000125 per hour). The reason is not
  yet checked against the documentation.

Comparison (daily averages, October 2026):
- Binance 4.77 percent, Hyperliquid 8.79 percent a year. Hyperliquid was higher on 28 of 31 days.
- Both sit at exactly 10.95 percent a year when the market is calm. That is the fixed
  interest component both exchanges document: 0.01 percent per 8 hours, which is
  0.00125 percent per hour.

Total DeFi TVL (DefiLlama, all chains, one GET request):
- The full history has 3344 daily rows, from 27 Sep 2017 to 22 Nov 2026, with no
  duplicates and no missing days. The first rows are 0, from before DeFi existed.
- October 2026: TVL went from 91.6 to 81.6 billion dollars (down 10.9 percent),
  with a low of 80.8 and a high of 93.4.
- TVL is counted in dollars, so falling coin prices push it down too. That
  effect is not separated yet.

One month, one coin, two venues with different payment rhythms: no
conclusion about carry yet.

## Next steps

- Add tests (pytest) for the quality checks.
- Redo the analysis in Polars, then explore the same files with SQL in DuckDB.

## Run

Run these from the repo root.

    uv sync
    uv run python scripts/binance/01_fetch_klines.py
    uv run python scripts/binance/02_explore_klines.py
    uv run python scripts/binance/03_fetch_funding.py
    uv run python scripts/binance/04_explore_funding.py
    uv run python scripts/hyperliquid/01_fetch_funding.py
    uv run python scripts/hyperliquid/02_explore_funding.py
    uv run python scripts/compare/01_funding_binance_vs_hyperliquid.py
    uv run python scripts/defillama/01_fetch_tvl.py
    uv run python scripts/defillama/02_explore_tvl.py

Run the automatic checks:

    uv run pytest
