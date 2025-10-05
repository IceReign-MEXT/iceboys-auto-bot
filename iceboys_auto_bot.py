
import os
import asyncio
import httpx
from datetime import datetime, timezone
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def send_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
        print("[+] Message sent successfully.")
    except Exception as e:
        print(f"[!] Error sending message: {e}")

async def tracker():
    while True:
        try:
            print("\n========================================")
            print("ICEBOYS — Tracker Cycle Started")
            print("========================================")

            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            wallet = "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"

            # Try fetching balance (mock for now)
            sol_balance = "0.000000000"

            message = f"""🚀 ICEBOYS Tracker Update
🕒 {now}

💎 Wallet: {wallet}
💰 SOL Balance: {sol_balance} SOL

⚠️ ICEB token data not yet listed on DexScreener.
"""
            await send_message(message)
            await asyncio.sleep(300)  # wait 5 mins before next cycle
        except Exception as e:
            print(f"[!] Error: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(tracker())
