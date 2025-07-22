import requests
from datetime import datetime, timezone

def get_funding_rates(coin: str, start_date: str, end_date: str):

    payload = {
        "type": "fundingHistory",
        "coin": coin,
        "startTime": to_ms(start_date),
        "endTime": to_ms(end_date)
    }
    url = "https://api.hyperliquid.xyz/info"
    headers = {"Content-Type": "application/json"}

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_live_asset_context(coin: str):
    
    url = "https://api.hyperliquid.xyz/info"
    headers = {"Content-Type": "application/json"}
    payload = {"type": "metaAndAssetCtxs"}
    
    resp = requests.post(url, json=payload, headers=headers)
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