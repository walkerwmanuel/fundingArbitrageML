import requests 

def get_total_account_state(address):
    body = {
        "type": "clearinghouseState",
        "user": address
    }
    resp = requests.post("https://api.hyperliquid.xyz/info", json=body)
    resp.raise_for_status()
    return resp.json()
