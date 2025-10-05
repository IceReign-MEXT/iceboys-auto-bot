#!/usr/bin/env python3
"""
generate_wallets.py
Generates:
 - Ethereum account (private key + address)
 - Solana keypair (secret/keypair file + public key)
Saves outputs to ~/icehub_system/wallets/
WARNING: private keys are extremely sensitive. Back them up offline immediately.
"""

import os, json
from pathlib import Path
from eth_account import Account
from solana.keypair import Keypair
from datetime import datetime

BASE = Path.home() / "icehub_system"
WALLETS_DIR = BASE / "wallets"
WALLETS_DIR.mkdir(parents=True, exist_ok=True)

def save_json(path, obj, mode=0o600):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    os.chmod(path, mode)

def gen_eth():
    print("[*] Generating Ethereum account...")
    acct = Account.create()
    eth = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "datetime": datetime.utcnow().isoformat() + "Z"
    }
    save_json(WALLETS_DIR / "eth_account.json", eth)
    # Save a plaintext backup (user should move offline)
    with open(WALLETS_DIR / "eth_account_private_backup.txt", "w") as f:
        f.write(f"ADDRESS: {acct.address}\nPRIVATE_KEY: {acct.key.hex()}\n")
    os.chmod(WALLETS_DIR / "eth_account_private_backup.txt", 0o600)
    print(f"[+] Ethereum address: {acct.address}")
    return eth

def gen_solana():
    print("[*] Generating Solana keypair...")
    kp = Keypair()
    secret = list(kp.secret_key)
    sol = {
        "public_key": str(kp.public_key),
        "secret_key": secret,
        "datetime": datetime.utcnow().isoformat() + "Z"
    }
    save_json(WALLETS_DIR / "sol_account.json", sol)
    # Save secret as raw bytes file for backup
    with open(WALLETS_DIR / "sol_account_secret.raw", "wb") as f:
        f.write(bytes(secret))
    os.chmod(WALLETS_DIR / "sol_account_secret.raw", 0o600)
    print(f"[+] Solana public key: {kp.public_key}")
    return sol

def main():
    print("=== Wallet Generator for IceHub ===")
    print("WARNING: Back up the private keys immediately to an offline place.")
    eth = gen_eth()
    sol = gen_solana()
    summary = {
        "eth_address": eth["address"],
        "sol_pubkey": sol["public_key"],
        "note": "Private keys stored in ~/icehub_system/wallets/ (secure them offline)"
    }
    save_json(WALLETS_DIR / "wallets_summary.json", summary)
    print("[*] Saved wallet files to:", WALLETS_DIR)
    print("=== DONE ===")

if __name__ == "__main__":
    main()
