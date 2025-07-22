from services.funding_rates import get_funding_rates

def average_funding_rate(coin: str, start_date: str, end_date: str) -> float:

    records = get_funding_rates(coin, start_date, end_date)
    rates = [float(r["fundingRate"]) for r in records if "fundingRate" in r]

    if not rates:
        return 0.0
    avg =  sum(rates) / len(rates)

    return {
        "averageFundingRate": avg,
        "annualizedAverageFundingRate": avg * 365 * 24
    }