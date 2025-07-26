import asyncio
import time
from datetime import datetime, timezone
from services.hyperliquid.funding_rates import get_live_asset_context
from logic.funding_rates import average_funding_rate, get_funding_rates
from logic.ml_data import append_live_funding_row, append_historic_asset_ctxs


# Format today's date as MM-DD-YYYY
today_str = datetime.now().strftime("%m-%d-%Y")

def annualize_funding_rate(rate):
    return float(rate) * 24 * 365

if __name__ == "__main__": 
#     # target_coin = "BTC"
    append_historic_asset_ctxs("ETH", "2023-10-25", "2025-06-25")
#     append_live_funding_row("BTC")

# if __name__ == "__main__":
#     target_coin = "BTC"
#     last_minute = None
#     while True:
#         now = datetime.now(timezone.utc)
#         current_minute = now.replace(second=0, microsecond=0)
#         if last_minute != current_minute:
#             append_live_funding_row(target_coin)
#             print(f"Appended row for {target_coin} at {now.isoformat()}")
#             last_minute = current_minute
#         # Always sleep a little (not 60s, just a bit) to avoid CPU spinning
#         time.sleep(0.5)