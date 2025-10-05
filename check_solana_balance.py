#!/usr/bin/env python3
"""
check_solana_balance.py
Safe Solana public-balance checker for Termux / IceHub.
Uses public RPC (or SOL_RPC_URL from .env).
No private keys / no secrets required.
"""

import os
import sys
from datetime import datetime

# prefer python-solana client
try:
    from solana.rpc.api import Client
    from solana.publickey import PublicKey
except Exception as e:
    print("ERROR: python 'solana' package not available or import failed.")
    print("Install recommended version: pip install solana==0.18.3")
    print("Import error:", e)
    sys.exit(1)

# optional: load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # no dotenv — that's fine
    pass

# CONFIG
DEFAULT_RPC = os.environ.get("SOL_RPC_URL", "https://api.mainnet-beta.solana.com")
# Replace with the public address you want to check (or pass as an arg)
PUBLIC_ADDRESS = os.environ.get("SOL_WALLET", "") or "HxmywH2gW9ezQ2nBXwurpaWsZS6YvdmLF23R9WgMAM7p"

def pretty_lamports(lamports: int) -> str:
    # 1 SOL = 1_000_000_000 lamports
    sol = lamports / 1_000_000_000
    return f"{lamports} lamports = {sol:.9f} SOL"

def main():
    print("========================================")
    print(" IceHub — Solana Public Balance Checker ")
    print(f" Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("========================================\n")

    rpc_url = DEFAULT_RPC
    print("Using RPC:", rpc_url)
    print("Checking address:", PUBLIC_ADDRESS, "\n")

    # validate address
    try:
        pub = PublicKey(PUBLIC_ADDRESS)
    except Exception as e:
        print("ERROR: Invalid public key:", e)
        sys.exit(1)

    client = Client(rpc_url)

    try:
        res = client.get_balance(pub)
    except Exception as e:
        print("ERROR: RPC call failed:", e)
        sys.exit(1)

    if not res or "result" not in res:
        print("ERROR: Unexpected RPC response:", res)
        sys.exit(1)

    # parse result
    try:
        lamports = res["result"]["value"]
        print("Balance result:")
        print(" ", pretty_lamports(lamports))
    except Exception as e:
        print("ERROR: Could not parse balance:", e)
        print("Full response:", res)
        sys.exit(1)

    # also print recent blockhash info (optional)
    try:
        recent = client.get_recent_blockhash()
        if recent and "result" in recent:
            bh = recent["result"].get("value", {}).get("blockhash", "n/a")
            print("\nRecent blockhash (sample):", bh)
    except Exception:
        pass

    print("\nDone.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
