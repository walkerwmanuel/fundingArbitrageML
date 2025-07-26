import csv
import os
from datetime import datetime, timezone, timedelta
import subprocess
import pandas as pd

from services.hyperliquid.funding_rates import get_live_asset_context

os.makedirs("historic_data", exist_ok=True)

def append_historic_asset_ctxs(coin, start_date, end_date):
    bucket = "hyperliquid-archive"
    s3_prefix = "asset_ctxs"

    output_csv = os.path.join("historic_data", f"{coin}_funding_data.csv")
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    all_rows = []

    while dt <= end:
        dstr = dt.strftime("%Y%m%d")
        s3_path = f"s3://{bucket}/{s3_prefix}/{dstr}.csv.lz4"
        local_lz4 = f"./{dstr}.csv.lz4"
        local_csv = f"./{dstr}.csv"

        print(f"Downloading {s3_path} ...")
        code = subprocess.call([
            "aws", "s3", "cp", s3_path, local_lz4, "--request-payer", "requester"
        ])
        if code != 0:
            print(f"Failed to download {s3_path}, skipping.")
            dt += timedelta(days=1)
            continue

        print(f"Decompressing {local_lz4} ...")
        code = subprocess.call(["unlz4", "-f", local_lz4, local_csv])
        if code != 0:
            print(f"Failed to decompress {local_lz4}, skipping.")
            os.remove(local_lz4)
            dt += timedelta(days=1)
            continue

        print(f"Reading {local_csv} ...")
        try:
            df = pd.read_csv(local_csv)
            df = df[df['coin'] == coin]

            # Keep only timestamps that are on the hour
            df['time'] = pd.to_datetime(df['time'], errors='coerce')
            df = df[df['time'].dt.minute == 0]
            df = df[df['time'].dt.second == 0]

            all_rows.append(df)
        except Exception as e:
            print(f"Failed to load or filter {local_csv}: {e}")

        try:
            os.remove(local_lz4)
            os.remove(local_csv)
        except Exception:
            pass

        dt += timedelta(days=1)

    if all_rows:
        out_df = pd.concat(all_rows, ignore_index=True)
        file_exists = os.path.isfile(output_csv)
        if file_exists:
            old_df = pd.read_csv(output_csv)
            out_df = pd.concat([old_df, out_df], ignore_index=True, sort=False)
        out_df.to_csv(output_csv, index=False)
        print(f"Saved/updated {output_csv} with merged asset ctx data.")
    else:
        print("No data files were successfully loaded for your coin and date range.")


def append_live_funding_row(coin: str):
    print("Running append_live_funding_row function")
    live_ctx = get_live_asset_context(coin)
    if not live_ctx:
        print(f"Could not fetch asset context for {coin}")
        return

    # Prepare the row, matching the historical data format
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    row = {
        "time": now,
        "coin": coin,
        "funding": live_ctx.get("funding", ""),
        "open_interest": live_ctx.get("openInterest", ""),
        "prev_day_px": live_ctx.get("prevDayPx", ""),
        "day_ntl_vlm": live_ctx.get("dayNtlVlm", ""),
        "premium": live_ctx.get("premium", ""),
        "oracle_px": live_ctx.get("oraclePx", ""),
        "mark_px": live_ctx.get("markPx", ""),
        "mid_px": live_ctx.get("midPx", ""),
        "impact_bid_px": "",
        "impact_ask_px": "",
    }
    # Parse impactPxs as bid/ask if present
    impact_pxs = live_ctx.get("impactPxs", [])
    if isinstance(impact_pxs, list):
        if len(impact_pxs) > 0:
            row["impact_bid_px"] = impact_pxs[0]
        if len(impact_pxs) > 1:
            row["impact_ask_px"] = impact_pxs[1]

    csv_file = os.path.join("historic_data", f"{coin}_funding_data.csv")
    headers = [
        "time", "coin", "funding", "open_interest", "prev_day_px", "day_ntl_vlm",
        "premium", "oracle_px", "mark_px", "mid_px", "impact_bid_px", "impact_ask_px"
    ]

    file_exists = os.path.isfile(csv_file)
    try:
        with open(csv_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists or os.stat(csv_file).st_size == 0:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

