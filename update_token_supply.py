#!/usr/bin/env python3
"""
update_token_supply.py
Updates the iceboys_token_summary.json to use a new supply (3,000,000,000),
recalculates Genesis Value in USD and estimated NGN & ETH (user sets USD->NGN and ETH price).
"""

import json
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "icehub_system" / "reports"
BASE.mkdir(parents=True, exist_ok=True)

OUT_FILE = BASE / "iceboys_token_update_summary.json"

# Configurable values:
NEW_SUPPLY = 3_000_000_000           # 3 billion
UNIT_PRICE_USD = 0.002105            # token price in USD (change if you want)
USD_TO_NGN = 1472.0                  # set to current rate - update manually if needed
ETH_PRICE_USD = 4051.33              # set to current ETH price (update manually)

def main():
    token = {
        "Token Name": "IceBoys",
        "Symbol": "ICEB",
        "Supply": float(NEW_SUPPLY),
        "Initial Price (USD)": float(UNIT_PRICE_USD)
    }
    total_usd = NEW_SUPPLY * UNIT_PRICE_USD
    total_ngn = total_usd * USD_TO_NGN
    total_eth = total_usd / ETH_PRICE_USD

    token.update({
        "Total Genesis Value (USD)": round(total_usd, 3),
        "Total Genesis Value (NGN)": round(total_ngn, 2),
        "Total Genesis Value (ETH)": round(total_eth, 6),
        "updated_at": datetime.utcnow().isoformat() + "Z"
    })

    with open(OUT_FILE, "w") as f:
        json.dump(token, f, indent=4)

    print("=== IceBoys Token Update Summary ===")
    print(f"Supply: {token['Supply']}")
    print(f"Unit Price (USD): {token['Initial Price (USD)']}")
    print(f"Total USD: {token['Total Genesis Value (USD)']}")
    print(f"Total NGN: {token['Total Genesis Value (NGN)']}")
    print(f"Total ETH: {token['Total Genesis Value (ETH)']}")
    print("Saved to:", OUT_FILE)

if __name__ == "__main__":
    main()
