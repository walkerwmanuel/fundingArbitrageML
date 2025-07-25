import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()
HYPERLIQUID_API_URL = os.getenv("HYPERLIQUID_API_URL")
hl_url = f"{HYPERLIQUID_API_URL}/info"


def get_funding_rates_max_19(coin: str, start_date: str, end_date: str):
    # the hyperliquid api restricts the request to 19 days max
    payload = {
        "type": "fundingHistory",
        "coin": coin,
        "startTime": to_ms(start_date),
        "endTime": to_ms(end_date)
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(hl_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        print(f"Error: No funding data found for {coin} between {start_date} and {end_date}")
    return data

def get_live_asset_context(coin: str):
    headers = {"Content-Type": "application/json"}
    payload = {"type": "metaAndAssetCtxs"}
    resp = requests.post(hl_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # data is [meta, asset_contexts], where asset_contexts is a list
    # The order matches between meta["universe"] and asset_contexts
    meta = data[0]
    asset_contexts = data[1]
    # Find the index for the given coin
    for i, coin_meta in enumerate(meta["universe"]):
        if coin_meta["name"].upper() == coin.upper():
            return asset_contexts[i]
    return None  # Not found

def to_ms(dt_str):
    # parse as midnight UTC of that date
    dt = datetime.strptime(dt_str, "%m-%d-%Y")
    # force to UTC and get milliseconds
    return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
