#!/usr/bin/env python3
"""
tg_status_bot.py
Simple Telegram bot that posts token status to a CHANNEL (not a chat).
Requires a Bot token and the target channel chat_id (neg int or @channelusername).
Uses python-telegram-bot library.
"""

import os, time, json
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # e.g., "@YourChannel" or "-1001234567890"
INTERVAL = int(os.getenv("POST_INTERVAL_SECONDS", "300"))  # default every 5 minutes

if not BOT_TOKEN or not CHANNEL_ID:
    raise SystemExit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in ~/.env or env vars")

BASE = Path.home() / "icehub_system" / "reports"
TOKEN_FILE = BASE / "iceboys_token_update_summary.json"
FALLBACK = BASE / "iceboys_token_summary.json"
bot = Bot(BOT_TOKEN)

def load_token():
    if TOKEN_FILE.exists():
        return json.load(open(TOKEN_FILE))
    if FALLBACK.exists():
        return json.load(open(FALLBACK))
    return None

def format_message(data):
    lines = []
    lines.append(f"📢 *IceBoys (ICEB) Status Update*")
    lines.append(f"Supply: `{int(data.get('Supply')):,}`")
    lines.append(f"Price (USD): `{data.get('Initial Price (USD)')}`")
    lines.append(f"Total Genesis Value (USD): `{data.get('Total Genesis Value (USD)')}`")
    if "Total Genesis Value (NGN)" in data:
        lines.append(f"Total (NGN): `₦{data.get('Total Genesis Value (NGN)')}`")
    if "Total Genesis Value (ETH)" in data:
        lines.append(f"Total (ETH): `{data.get('Total Genesis Value (ETH)')}`")
    lines.append(f"Updated: `{data.get('updated_at', data.get('Launch Timestamp', 'N/A'))}`")
    return "\n".join(lines)

def main():
    print("[*] Telegram status bot started. Posting to:", CHANNEL_ID)
    while True:
        data = load_token()
        if data:
            text = format_message(data)
            try:
                bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="Markdown")
                print("[+] Posted update to channel")
            except Exception as e:
                print("Telegram send error:", e)
        else:
            print("[!] No token data file found.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
