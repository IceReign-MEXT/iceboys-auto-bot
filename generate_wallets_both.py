#!/usr/bin/env python3
"""
generate_wallets_both.py
Creates:
 - Solana-style keypair (ed25519) and saves secret as raw bytes + JSON
 - Ethereum account (private key + address) using eth-account
Saves output in ~/icehub_system/wallets/
WARNING: back up private keys immediately and secure them offline.
"""

import os, json, binascii
from pathlib import Path
from datetime import datetime
from eth_account import Account
import nacl.signing

BASE = Path.home() / "icehub_system"
WALLETS_DIR = BASE / "wallets"
WALLETS_DIR.mkdir(parents=True, exist_ok=True)

def save_json(path, obj, mode=0o600):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    os.chmod(path, mode)

def gen_eth():
    acct = Account.create()  # eth-account
    eth = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    save_json(WALLETS_DIR / "eth_account.json", eth)
    # plaintext backup (user should move offline)
    with open(WALLETS_DIR / "eth_account_private_backup.txt", "w") as f:
        f.write(f"ADDRESS: {acct.address}\nPRIVATE_KEY: {acct.key.hex()}\n")
    os.chmod(WALLETS_DIR / "eth_account_private_backup.txt", 0o600)
    return eth

def gen_solana_like():
    # Use ed25519 to create a keypair compatible with Solana format (secret_key = 64 bytes)
    signer = nacl.signing.SigningKey.generate()
    verify_key = signer.verify_key
    secret_key = signer._seed + verify_key.encode()  # 32 seed + 32 pub = 64 bytes
    pubkey_bytes = verify_key.encode()
    sol = {
        "public_key_hex": binascii.hexlify(pubkey_bytes).decode(),
        "public_key_base58": None,  # we compute base58 below
        "secret_key_bytes_hex": binascii.hexlify(secret_key).decode(),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    # optional: compute base58 pubkey (Solana uses base58). Do a safe fallback if base58 not installed
    try:
        import base58
        sol["public_key_base58"] = base58.b58encode(pubkey_bytes).decode()
    except Exception:
        sol["public_key_base58"] = None

    save_json(WALLETS_DIR / "sol_account.json", sol)
    # save raw secret bytes file
    with open(WALLETS_DIR / "sol_account_secret.raw", "wb") as f:
        f.write(secret_key)
    os.chmod(WALLETS_DIR / "sol_account_secret.raw", 0o600)
    return sol

def main():
    print("=== IceHub wallet generator — Solana-style + Ethereum ===")
    eth = gen_eth()
    sol = gen_solana_like()
    summary = {
        "eth_address": eth["address"],
        "sol_public_base58": sol.get("public_key_base58"),
        "sol_public_hex": sol.get("public_key_hex"),
        "notes": "Back up eth_account_private_backup.txt and sol_account_secret.raw offline immediately."
    }
    save_json(WALLETS_DIR / "wallets_summary.json", summary)
    print("[+] ETH address:", eth["address"])
    if sol.get("public_key_base58"):
        print("[+] SOL public key (base58):", sol["public_key_base58"])
    else:
        print("[+] SOL public key (hex):", sol["public_key_hex"])
    print("[*] Files saved to:", WALLETS_DIR)
    print("=== DONE ===")

if __name__ == '__main__':
    main()
