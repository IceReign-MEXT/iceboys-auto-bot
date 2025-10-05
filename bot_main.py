import asyncio
import logging
from datetime import datetime, timezone
from telegram import Bot
from telegram.constants import ParseMode
import httpx
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
import os
import time

# === CONFIG ===
BOT_TOKEN = "8398239711:AAEOq44XzZ5m8O3KcHXQdPAUbISjbeLCtzE"
CHANNEL_ID = -1002384609234
ETH_ADDRESS = "0x5B0703825e5299b52b0d00193Ac22E20795defBa"
SOL_ADDRESS = "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"

# === LOGGER ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# === HELPERS ===
async def get_eth_balance(address: str):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            data = r.json()
            if data.get("status") == "1":
                balance = int(data["result"]) / 10**18
                return f"{balance:.6f} ETH"
    except Exception as e:
        logging.error(f"ETH balance error: {e}")
    return "⚠️ ETH error"

async def get_sol_balance(address: str):
    try:
        async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
            resp = await client.get_balance(PublicKey(address))
            if resp and resp.value:
                balance = resp.value / 10**9
                return f"{balance:.6f} SOL"
    except Exception as e:
        logging.error(f"SOL balance error: {e}")
    return "⚠️ SOL error"

async def post_update(bot: Bot):
    while True:
        try:
            eth_balance = await get_eth_balance(ETH_ADDRESS)
            sol_balance = await get_sol_balance(SOL_ADDRESS)
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

            message = (
                f"💠 <b>IceHub 24/7 Tracker</b>\n\n"
                f"🕓 Updated: {now}\n\n"
                f"💎 <b>ETH Wallet:</b> <code>{ETH_ADDRESS}</code>\n"
                f"💰 Balance: {eth_balance}\n\n"
                f"❄️ <b>SOL Wallet:</b> <code>{SOL_ADDRESS}</code>\n"
                f"💰 Balance: {sol_balance}\n\n"
                f"#IceHub #ICEB #ICEGODS"
            )

            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
            logging.info("✅ Update posted successfully.")
        except Exception as e:
            logging.error(f"Failed to send update: {e}")
            logging.info("Retrying in 60s...")
        await asyncio.sleep(60)  # update every 1 minute

async def main():
    bot = Bot(token=BOT_TOKEN, request_timeout=30)
    logging.info("🚀 IceHub 24/7 Wallet Tracker Bot started...")
    await post_update(bot)

if __name__ == "__main__":
    asyncio.run(main())
