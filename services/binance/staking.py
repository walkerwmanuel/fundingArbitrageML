import urllib.parse
import hashlib
import hmac
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

API_URL = os.getenv("BINANCE_US_API_URL")
API_KEY = os.getenv("BINANCE_US_API_KEY")
SECRET_KEY = os.getenv("BINANCE_US_SECRET_KEY")

def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

def get_staking_info(coin_name):
    uri_path = "/sapi/v1/staking/asset"
    data = {
        "timestamp": int(round(time.time() * 1000))
    }
    if coin_name:
        data["stakingAsset"] = coin_name

    signature = get_binanceus_signature(data, SECRET_KEY)
    headers = {'X-MBX-APIKEY': API_KEY}
    payload = {**data, "signature": signature}
    resp = requests.post(API_URL + uri_path, data=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
