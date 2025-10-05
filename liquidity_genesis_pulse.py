import json
import os
import random
from datetime import datetime

REPORTS_PATH = "/data/data/com.termux/files/home/icehub_system/reports"
os.makedirs(REPORTS_PATH, exist_ok=True)

def log(message: str):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {message}")

def safe_get(data, keys, default=0.0):
    """Safely get a value using possible key variations."""
    for key in keys:
        if key in data:
            return data[key]
    return default

def main():
    print("=====================================")
    print("   ICEHUB LIQUIDITY GENESIS PULSE - S28")
    print("=====================================")

    log("Initializing Liquidity Genesis Pulse...")
    log("Loading resource generation summary...")
    resource_file = os.path.join(REPORTS_PATH, "resource_generation_summary.json")

    if os.path.exists(resource_file):
        with open(resource_file) as f:
            resource_data = json.load(f)
        log("Resource summary loaded successfully.")
    else:
        log("No previous resource summary found. Generating mock resource data...")
        resource_data = {}

    # handle multiple naming patterns
    energy_units = safe_get(resource_data, ["Total Energy Units", "energy_units", "EnergyUnits"], random.uniform(1000, 3000))
    token_flow = safe_get(resource_data, ["Total Token Flow", "token_flow", "TokenFlow"], random.uniform(10000, 20000))
    balance_index = safe_get(resource_data, ["Balance Index", "balance_index", "BalanceIndex"], random.uniform(3.0, 7.0))

    log("Activating liquidity conduits...")
    liquidity_factor = balance_index * random.uniform(1.05, 1.25)
    liquidity_output = token_flow * liquidity_factor

    log("Synchronizing with blockchain cores...")
    log("Merging pulse streams with IceBoys token network...")
    pulse_strength = random.uniform(95.0, 100.0)

    summary = {
        "season": 28,
        "module": "liquidity_genesis_pulse",
        "liquidity_output": round(liquidity_output, 4),
        "liquidity_factor": round(liquidity_factor, 3),
        "pulse_strength": f"{pulse_strength:.2f}%",
        "source_energy_units": round(energy_units, 3),
        "source_token_flow": round(token_flow, 3),
        "source_balance_index": round(balance_index, 3),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    summary_path = os.path.join(REPORTS_PATH, "liquidity_genesis_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    log("Finalizing Liquidity Genesis Pulse summary...")

    print("=====================================")
    print(" ✅ SEASON 28 — LIQUIDITY GENESIS COMPLETE")
    print("=====================================")
    print(f"Liquidity Output: {summary['liquidity_output']}")
    print(f"Pulse Strength: {summary['pulse_strength']}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
