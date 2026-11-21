from pathlib import Path

from market_data_lab.binance_files import download, funding_url, unzip

symbol = "BTCUSDT"
month = "2026-10"
raw_dir = Path("data/raw")


def section(title: str) -> None:
    print()
    print("-" * 50)
    print(title)
    print("-" * 50)


section("1. Address we download from")
url = funding_url(symbol, month)
print(url)

# download the zip, then unzip it into data/raw
zip_path = download(url, raw_dir / f"{symbol}-fundingRate-{month}.zip")
files = unzip(zip_path, raw_dir)

section("2. Files inside the zip")
print(files)

# read every line as plain text, we do not assume a header yet
with open(files[0]) as f:
    lines = f.readlines()

section("3. How many lines in the file")
print("total lines:", len(lines))

section("4. First 4 lines, exactly as they are in the file")
for line in lines[:4]:
    print(line.strip())