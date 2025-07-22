from services.hyperliquid.funding_rates import get_funding_rates_max_19
from services.hyperliquid.candles import get_candle_snapshot
from logic.funding_rates import get_funding_rates
from datetime import datetime

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

def get_all_ml_data(coin: str, start_date: str, end_date: str):
    funding_records = get_funding_rates(coin, start_date, end_date)
    dt_start = datetime.strptime(start_date, "%m-%d-%Y")
    dt_end = datetime.strptime(end_date, "%m-%d-%Y")
    start_ms = int(dt_start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    end_ms = int(dt_end.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp() * 1000)
    candles = get_candle_snapshot(coin, "1h", start_ms, end_ms)

    ml_data = []
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

        ml_data.append({
            "closing_time_of_funding_and_candle": funding_time,
            "hourly_funding_rate": hourly_funding,
            "annualized_funding_rate": annualized_funding,
            "premium": premium,
            "openPrice": openPrice,
            "closingPrice": closingPrice,
            "volume": volume
        })
    return ml_data
