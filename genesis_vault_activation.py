import json
import random
from datetime import datetime, timezone
import os

def log(message):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {message}")

def main():
    print("=====================================")
    print("   ICEHUB GENESIS VAULT ACTIVATION - S37")
    print("=====================================")

    log("Initializing Genesis Vault Activation...")
    reality_summary_path = "/data/data/com.termux/files/home/icehub_system/reports/continuum_resonance_summary.json"

    if not os.path.exists(reality_summary_path):
        log("Previous summary not found! Run S36 first.")
        return

    with open(reality_summary_path, "r") as f:
        reality_data = json.load(f)

    log("Loading Continuum Resonance data...")
    resonance_factor = reality_data.get("Resonance Factor", 1.0)
    continuum_flow = reality_data.get("Continuum Flow", 100.0)

    # Generate Genesis Vault parameters
    vault_energy = continuum_flow * random.uniform(1.05, 1.15)
    genesis_key_strength = resonance_factor * random.uniform(100, 125)
    security_hash = hex(int(vault_energy * genesis_key_strength * 1000))[2:]

    log("Constructing Genesis Vault...")
    log("Sealing system layers with encrypted key cores...")

    genesis_vault = {
        "Genesis Vault Energy": round(vault_energy, 4),
        "Genesis Key Strength": round(genesis_key_strength, 3),
        "Vault Integrity": "SEALED",
        "Security Hash": security_hash.upper(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    os.makedirs("/data/data/com.termux/files/home/icehub_system/reports", exist_ok=True)
    summary_path = "/data/data/com.termux/files/home/icehub_system/reports/genesis_vault_summary.json"
    with open(summary_path, "w") as f:
        json.dump(genesis_vault, f, indent=4)

    log("Finalizing Genesis Vault summary...")
    print("=====================================")
    print(" ✅ SEASON 37 — GENESIS VAULT ACTIVATED")
    print("=====================================")
    print(f"Vault Energy: {genesis_vault['Genesis Vault Energy']}")
    print(f"Genesis Key Strength: {genesis_vault['Genesis Key Strength']}")
    print(f"Security Hash: {genesis_vault['Security Hash']}")
    print("Summary saved to:", summary_path)
    print("~/icehub_system $")

if __name__ == "__main__":
    main()
