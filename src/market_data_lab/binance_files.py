import zipfile
from pathlib import Path

import requests

BASE_URL = "https://data.binance.vision/data/futures/um/monthly"


def kline_url(symbol: str, interval: str, year_month: str) -> str:
    return f"{BASE_URL}/klines/{symbol}/{interval}/{symbol}-{interval}-{year_month}.zip"


def funding_url(symbol: str, year_month: str) -> str:
    return f"{BASE_URL}/fundingRate/{symbol}/{symbol}-fundingRate-{year_month}.zip"


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    dest.write_bytes(response.content)
    return dest


def unzip(zip_path: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out_dir)
        return [out_dir / name for name in z.namelist()]