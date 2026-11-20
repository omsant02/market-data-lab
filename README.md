# market-data-lab

Small Python scripts that fetch and explore real crypto market data
(Binance public files, Hyperliquid API, DefiLlama API).
Downloaded data is not stored in this repo.

## Scripts

- `fetch_binance_klines.py` downloads one month of BTCUSDT 1-hour futures
  candles from data.binance.vision and unzips it into `data/raw`.
- `explore_klines.py` loads the file, checks it for duplicates and gaps,
  computes hourly returns and saves a price chart.

## Run

    uv sync
    uv run python fetch_binance_klines.py
    uv run python explore_klines.py