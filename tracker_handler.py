import asyncio
import httpx
from datetime import datetime

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens"

ICEB_TOKEN = "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"
CHECK_INTERVAL = 120  # seconds


async def get_sol_balance(pubkey: str):
    """Fetch SOL balance of any Solana wallet."""
    try:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [pubkey]}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(SOLANA_RPC, json=payload)
        balance = r.json()["result"]["value"]
        return balance / 1_000_000_000
    except Exception as e:
        print(f"[!] Balance fetch failed: {e}")
        return None


async def get_token_data():
    """Fetch ICEB token data from Dexscreener if available."""
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(f"{DEXSCREENER_URL}/{ICEB_TOKEN}")
        data = r.json()
        pairs = data.get("pairs", [])
        if not pairs:
            return None
        p = pairs[0]
        return {
            "pair": p["pairAddress"],
            "dex": p.get("dexId", "Unknown"),
            "price": p["priceUsd"],
            "liquidity": p["liquidity"]["usd"],
            "volume24h": p["volume"]["h24"],
        }
    except Exception as e:
        print(f"[!] Dex data fetch failed: {e}")
        return None


async def tracker_cycle():
    """Main cycle to pull info and display results."""
    while True:
        print("\n========================================")
        print(" ICEBOYS — Tracker Cycle Started")
        print(f" Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("========================================")

        sol_balance = await get_sol_balance(ICEB_TOKEN)
        token_data = await get_token_data()

        print(f" Wallet: {ICEB_TOKEN}")
        print(f" SOL Balance: {sol_balance} SOL")

        if token_data:
            print(f" DEX: {token_data['dex']}")
            print(f" Price: ${token_data['price']}")
            print(f" Liquidity: ${token_data['liquidity']}")
            print(f" 24h Volume: ${token_data['volume24h']}")
        else:
            print(" ⚠️ ICEB token data not found on DexScreener yet.")

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(tracker_cycle())
    except KeyboardInterrupt:
        print("\nTracker stopped by user.")
