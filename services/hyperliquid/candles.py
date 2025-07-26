import requests
from dotenv import load_dotenv
import os
import asyncio
import json
import websockets

load_dotenv()  # Load variables from .env file
hyperliquid_api_url = "https://api.hyperliquid.xyz"

def get_candle_snapshot(coin: str, interval: str, start_time_ms: int, end_time_ms: int):
    hl_url = f"{hyperliquid_api_url}/info"
    headers = {"Content-Type": "application/json"}
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_time_ms,
            "endTime": end_time_ms
        }
    }
    resp = requests.post(hl_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

# For the candle websocket
async def candle_websocket(coin: str, interval: str):
    uri = "wss://api.hyperliquid.xyz/ws"
    subscribe_msg = {
        "method": "subscribe",
        "subscription": {"type": "candle", "coin": coin, "interval": interval}
    }

    retry_count = 0
    base_delay = 1
    max_retries = 10

    while retry_count < max_retries:
        try:
            print(f"Connecting to websocket for {coin} {interval} candles...")
            async with websockets.connect(uri, ping_interval=30, close_timeout=5) as ws:
                await ws.send(json.dumps(subscribe_msg))
                print(f"Subscribed to {coin} {interval} candles.")
                retry_count = 0  # Reset retry on success

                # Periodic ping
                async def keep_ping():
                    try:
                        while True:
                            await asyncio.sleep(25)
                            await ws.ping()
                    except asyncio.CancelledError:
                        pass
                ping_task = asyncio.create_task(keep_ping())

                try:
                    while True:
                        msg = await asyncio.wait_for(ws.recv(), timeout=40)
                        data = json.loads(msg)
                        if data.get("channel") == "candle":
                            candles = data["data"]
                            if isinstance(candles, dict):
                                yield candles
                            elif isinstance(candles, list):
                                for candle in candles:
                                    yield candle
                except (asyncio.TimeoutError, websockets.ConnectionClosed):
                    print("No data/ping timeout or connection closed. Reconnecting...")
                finally:
                    ping_task.cancel()
                    try:
                        await ping_task
                    except Exception:
                        pass
        except Exception as e:
            retry_count += 1
            delay = min(60, base_delay * (2 ** (retry_count - 1)))
            print(f"Websocket error: {e} (retry {retry_count}/{max_retries}) - reconnecting in {delay:.1f}s...")
            await asyncio.sleep(delay)

    print("WebSocket exited: reached max retries.")
