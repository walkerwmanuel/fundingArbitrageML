import csv
import os
from datetime import datetime
from services.hyperliquid.funding_rates import get_funding_rates_max_19, get_live_asset_context
from services.hyperliquid.candles import get_candle_snapshot, candle_websocket
from logic.funding_rates import get_funding_rates
from datetime import datetime

os.makedirs("historic_data", exist_ok=True)


def find_nearest_candle(funding_time, candles, tolerance=5000):  # ±5 seconds
    best_candle = None
    min_diff = float('inf')
    for candle in candles:
        close_time = int(candle["T"])
        diff = abs(close_time - funding_time)
        if diff <= tolerance and diff < min_diff:
            min_diff = diff
            best_candle = candle
    return best_candle

def get_all_historic_ml_data(coin: str, start_date: str, end_date: str):
    print(f"Fetching historic ml data for {coin}!")
    funding_records = get_funding_rates(coin, start_date, end_date)
    if not funding_records:
        print("Error getting records")
    dt_start = datetime.strptime(start_date, "%m-%d-%Y")
    dt_end = datetime.strptime(end_date, "%m-%d-%Y")
    start_ms = int(dt_start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    end_ms = int(dt_end.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp() * 1000)
    candles = get_candle_snapshot(coin, "1h", start_ms, end_ms)
    if not funding_records:
        print("Error getting candles")

    csv_file = os.path.join("historic_data", f"{coin}_funding_data.csv")
    headers = [
        "closing_time_of_funding_and_candle",
        "hourly_funding_rate",
        "annualized_funding_rate",
        "premium",
        "openPrice",
        "closingPrice",
        "volume"
    ]

    with open(csv_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if f.tell() == 0:
            writer.writeheader()

        for rec in funding_records:
            funding_time = int(rec["time"])
            hourly_funding = float(rec["fundingRate"])
            annualized_funding = hourly_funding * 24 * 365
            premium = float(rec["premium"])

            # Find the candle whose closing time is within ±5 seconds of funding time
            candle = find_nearest_candle(funding_time, candles, tolerance=5000)
            if candle:
                closingPrice = float(candle["c"])
                openPrice = float(candle["o"])
                volume = float(candle["v"])
            else:
                closingPrice = None
                openPrice = None
                volume = None

            row = {
                "closing_time_of_funding_and_candle": funding_time,
                "hourly_funding_rate": hourly_funding,
                "annualized_funding_rate": annualized_funding,
                "premium": premium,
                "openPrice": openPrice,
                "closingPrice": closingPrice,
                "volume": volume
            }
            writer.writerow(row)

async def live_data_gathering_1h(coin: str):
    last_close_time = None
    async for candles in candle_websocket(coin, "1h"):
        print(f"Received candle data for {coin}: {candles}")
        close_time = int(candles["T"])
        if last_close_time is None:
            last_close_time = close_time  # Initialize and skip first received candle
            continue
        if close_time != last_close_time:
            append_live_funding_row(coin, candles, close_time)
            last_close_time = close_time

def append_live_funding_row(coin: str, candle: dict, funding_time: int):
    print("Runnign append live funding row function")
    live_ctx = get_live_asset_context(coin)
    if not live_ctx:
        print(f"Could not fetch asset context for {coin}")
        return

    # Gather features (use the same structure as get_all_historic_ml_data)
    hourly_funding = float(live_ctx.get("funding", 0))
    annualized_funding = hourly_funding * 24 * 365
    premium = float(live_ctx.get("premium", 0))
    openPrice = float(candle.get("o", 0))
    closingPrice = float(candle.get("c", 0))
    volume = float(candle.get("v", 0))

    # Format for CSV (match headers to your ML model requirements)
    row = {
        "closing_time_of_funding_and_candle": funding_time,
        "hourly_funding_rate": hourly_funding,
        "annualized_funding_rate": annualized_funding,
        "premium": premium,
        "openPrice": openPrice,
        "closingPrice": closingPrice,
        "volume": volume,
    }

    csv_file = os.path.join("historic_data", f"{coin}_funding_data.csv")
    headers = list(row.keys())

    # Append to CSV, add header if file is empty
    try:
        with open(csv_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

