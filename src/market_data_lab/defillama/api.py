import requests

BASE_URL = "https://api.llama.fi"


def get_json(path: str):
    # send one GET request (just an address, nothing in the body) and return the JSON reply
    response = requests.get(f"{BASE_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.json()


def historical_tvl() -> list[dict]:
    # total DeFi TVL across all chains, one row per day: {"date": seconds, "tvl": dollars}
    return get_json("/v2/historicalChainTvl")
