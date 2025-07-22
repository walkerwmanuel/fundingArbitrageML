from datetime import datetime, timezone
from services.hyperliquid.funding_rates import get_live_asset_context
from logic.funding_rates import average_funding_rate, get_funding_rates
from logic.ml_data import get_all_ml_data


# Format today's date as MM-DD-YYYY
today_str = datetime.now().strftime("%m-%d-%Y")

def annualize_funding_rate(rate):
    return float(rate) * 24 * 365

# For finding historical funding rates (output may be long so do python3 main.py > output.txt)
# if __name__ == "__main__":
#     rates = get_funding_rates("ETH", "07-01-2025", today_str)
#     for entry in rates:
#         ts = datetime.fromtimestamp(entry["time"]/1000, tz=timezone.utc)
#         rate = float(entry['fundingRate'])
#         rate_annualized = annualize_funding_rate(rate)
#         print(f"{ts.isoformat()} → rate: {rate:.8f}, annualized: {rate_annualized:.4%}, premium: {entry['premium']}, coin: {entry['coin']}")

# For finding average funding rates
# if __name__ == "__main__":
#     avg_data = average_funding_rate("FARTCOIN", "07-01-2025", today_str)
#     avg = avg_data["averageFundingRate"]
#     annualized = avg_data["annualizedAverageFundingRate"]
#     print(f"Average funding rate for coin: {avg:.8f}")
#     print(f"Annualized average funding rate: {annualized:.4%}")

# For live funding rates
# if __name__ == "__main__":
#     live_information = get_live_asset_context("VINE")
#     print(live_information)
#     funding_rate = float(live_information['funding'])

#     print("Current funding rate:", funding_rate)
#     print(f"Current annual funding rate: {annualize_funding_rate(funding_rate):.4%}")

# For machine learning training data
if __name__ == "__main__": 
    ml_data = get_all_ml_data("ETH", "07-01-2024", today_str)
    for row in ml_data:
        print(row)
