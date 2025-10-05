import os
import asyncio
from datetime import datetime, timezone
from telegram import Bot
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens"
ICEB_TOKEN = "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"
CHECK_INTERVAL = 300  # every 5 minutes


async def get_sol_balance(pubkey: str):
    try:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [pubkey]}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(SOLANA_RPC, json=payload)
        balance = r.json()["result"]["value"]
        return balance / 1_000_000_000
    except Exception as e:
        print(f"[!] Balance fetch failed: {e}")
        return 0.0


async def get_token_data():
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


async def send_update(bot: Bot):
    sol_balance = await get_sol_balance(ICEB_TOKEN)
    token_data = await get_token_data()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    msg = (
        f"🚀 <b>ICEBOYS Tracker Update</b>\n"
        f"🕒 {now}\n\n"
        f"💎 Wallet: <code>{ICEB_TOKEN}</code>\n"
        f"💰 SOL Balance: {sol_balance:.9f} SOL\n\n"
    )

    if token_data:
        msg += (
            f"📊 DEX: {token_data['dex']}\n"
            f"💵 Price: ${token_data['price']}\n"
            f"💧 Liquidity: ${token_data['liquidity']}\n"
            f"📈 24h Volume: ${token_data['volume24h']}\n"
        )
    else:
        msg += "⚠️ ICEB token data not yet listed on DexScreener.\n"

    try:
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="HTML")
        print("[+] Update sent successfully.")
    except Exception as e:
        print(f"[!] Telegram API error: {e}")


async def main():
    bot = Bot(BOT_TOKEN)
    print("========================================")
    print(" ICEBOYS — Tracker Cycle Started")
    print("========================================")
    while True:
        await send_update(bot)
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
