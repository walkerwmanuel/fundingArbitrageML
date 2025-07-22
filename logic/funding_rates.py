from services.funding_rates import get_funding_rates_max_19
from datetime import datetime, timedelta

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

def get_funding_rates(coin: str, start_date: str, end_date: str, chunk_days=19):
    all_records = []
    cur_start = datetime.strptime(start_date, "%m-%d-%Y")
    cur_end = datetime.strptime(end_date, "%m-%d-%Y")
    delta = timedelta(days=chunk_days)

    while cur_start < cur_end:
        chunk_end = min(cur_start + delta, cur_end)
        records = get_funding_rates_max_19(
            coin,
            cur_start.strftime("%m-%d-%Y"),
            chunk_end.strftime("%m-%d-%Y")
        )
        if not records:
            break
        all_records.extend(records)
        cur_start = chunk_end
    return all_records