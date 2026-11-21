from datetime import datetime, timezone

import requests

INFO_URL = "https://api.hyperliquid.xyz/info"


def month_bounds_ms(year: int, month: int) -> tuple[int, int]:
    # first millisecond of the month and last millisecond of the month, in UTC
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)
    end = datetime(next_year, next_month, 1, tzinfo=timezone.utc)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000) - 1


def post_info(payload: dict):
    # send one POST request with a JSON message and return the JSON reply
    response = requests.post(INFO_URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def funding_history(coin: str, start_ms: int, end_ms: int) -> list[dict]:
    rows = []
    cursor = start_ms
    while cursor < end_ms:
        batch = post_info({
            "type": "fundingHistory",
            "coin": coin,
            "startTime": cursor,
            "endTime": end_ms,
        })
        if not batch:
            break
        rows.extend(batch)
        # next page starts 1 millisecond after the last row we got
        cursor = batch[-1]["time"] + 1
    return rows