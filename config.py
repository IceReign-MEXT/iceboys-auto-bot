import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.expanduser("~/icehub_system/.env"))

# Telegram Bot setup
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Wallets
ETH_WALLET = os.getenv("ETH_WALLET")
SOL_WALLET = os.getenv("SOL_WALLET")

# Update interval (seconds)
UPDATE_INTERVAL = 120
