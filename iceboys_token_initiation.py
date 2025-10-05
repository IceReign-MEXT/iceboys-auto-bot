import json
import random
from datetime import datetime
from pathlib import Path

def log(message):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {message}")

def main():
    print("=====================================")
    print("   ICEHUB ICEBOYS TOKEN INITIATION - S38")
    print("=====================================")

    log("Initializing IceBoys Token Core...")
    data_dir = Path("/data/data/com.termux/files/home/icehub_system/reports")
    vault_path = data_dir / "genesis_vault_summary.json"

    if not vault_path.exists():
        print("[ERROR] Genesis Vault summary not found. Run S37 first.")
        return

    with open(vault_path, "r") as f:
        vault_data = json.load(f)

    vault_energy = vault_data.get("Vault Energy", 100)
    token_supply = round(vault_energy * random.uniform(85000, 125000), 3)
    token_price = round(random.uniform(0.0009, 0.0023), 6)
    total_value = round(token_supply * token_price, 3)

    log("Generating IceBoys Token specifications...")
    token_details = {
        "Token Name": "IceBoys",
        "Symbol": "ICEB",
        "Supply": token_supply,
        "Initial Price (USD)": token_price,
        "Total Genesis Value (USD)": total_value,
        "Genesis Energy Link": vault_energy,
        "Launch Timestamp": datetime.utcnow().isoformat() + "Z",
    }

    log("Finalizing token initiation process...")
    summary_path = data_dir / "iceboys_token_summary.json"
    with open(summary_path, "w") as f:
        json.dump(token_details, f, indent=4)

    print("=====================================")
    print(" ✅ SEASON 38 — ICEBOYS TOKEN INITIATION COMPLETE")
    print("=====================================")
    for k, v in token_details.items():
        print(f"{k}: {v}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
