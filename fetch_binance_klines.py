from pathlib import Path

from binance_files import download, kline_url, unzip

symbol = "BTCUSDT"
interval = "1h"
month = "2026-10"

raw_dir = Path("data/raw")

url = kline_url(symbol, interval, month)
print(url)

zip_path = download(url, raw_dir / f"{symbol}-{interval}-{month}.zip")
print(zip_path)

files = unzip(zip_path, raw_dir)
print(files)

with open(files[0]) as f:
    for _ in range(3):
        print(f.readline().strip())