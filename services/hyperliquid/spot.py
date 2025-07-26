# Just does api call to buy

import requests

HYPERLIQUID_API_URL = "https://api.hyperliquid.xyz/info"

def get_spot_meta_and_asset_ctxs():
    body = {"type": "spotMetaAndAssetCtxs"}
    resp = requests.post(HYPERLIQUID_API_URL, json=body)
    resp.raise_for_status()
    return resp.json()

def get_user_spot_balances(address):
    """
    address: Your wallet address, e.g. "0x0000000000000000000000000000000000000000"
    """
    body = {
        "type": "spotClearinghouseState",
        "user": address
    }
    resp = requests.post(HYPERLIQUID_API_URL, json=body)
    resp.raise_for_status()
    return resp.json()