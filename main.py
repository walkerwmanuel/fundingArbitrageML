from datetime import datetime, timezone
from services.funding_rates import get_funding_rates, get_live_asset_context
from logic.funding_rates import average_funding_rate


# Format today's date as MM-DD-YYYY
today_str = datetime.now().strftime("%m-%d-%Y")

def annualize_funding_rate(rate):
    return float(rate) * 24 * 365

# For finding historical funding rates
# if __name__ == "__main__":
#     rates = get_funding_rates("ETH", "07-01-2025", today_str)
#     for entry in rates:
#         ts = datetime.fromtimestamp(entry["time"]/1000, tz=timezone.utc)
#         rate = float(entry['fundingRate'])
#         rate_annualized = annualize_funding_rate(rate)
#         print(f"{ts.isoformat()} → rate: {rate:.8f}, annualized: {rate_annualized:.4%}, premium: {entry['premium']}")

# For finding average funding rates
if __name__ == "__main__":
    avg_data = average_funding_rate("ETH", "07-01-2024", today_str)
    avg = avg_data["averageFundingRate"]
    annualized = avg_data["annualizedAverageFundingRate"]
    print(f"Average funding rate for ETH: {avg:.8f}")
    print(f"Annualized average funding rate: {annualized:.4%}")

# For live funding rates
# if __name__ == "__main__":
#     live_information = get_live_asset_context("ETH")
#     funding_rate = float(live_information['funding'])

#     print("Current funding rate:", funding_rate)
#     print(f"Current annual funding rate: {annualize_funding_rate(funding_rate):.4%}")

