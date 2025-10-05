#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/icehub_system"
LOG="$BASE/bot_run.log"

mkdir -p "$BASE"
cd "$BASE"

echo "[+] Writing config.py ..."
cat > "$BASE/config.py" <<'PY'
# icehub config (auto-generated)
TELEGRAM_BOT_TOKEN = "8398239711:AAEOq44XzZ5m8O3KcHXQdPAUbISjbeLCtzE"
TELEGRAM_CHAT_ID = "-1002139845678"
OWNER_ID = 6453658778
OWNER_USERNAME = "@RobertSmithETH"
UPDATE_INTERVAL = 600  # seconds

# Public wallet addresses (do NOT store private keys here)
ETH_WALLET = "0x5B0703825e5299b52b0d00193Ac22E20795defBa"
SOLANA_ADDRESSES = [
    "HxmywH2gW9ezQ2nBXwurpaWsZS6YvdmLF23R9WgMAM7p",
    "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"
]
# RPC endpoints (change if you want)
ETH_RPC = "https://rpc.ankr.com/eth"
SOL_RPC = "https://api.mainnet-beta.solana.com"
PY

echo "[+] Writing robust bot_main.py ..."
cat > "$BASE/bot_main.py" <<'PY'
#!/usr/bin/env python3
"""
Robust wallet tracker bot for IceHub
Uses config.py for configuration.
"""
import asyncio
import logging
from datetime import datetime, timezone
import sys

# local config
try:
    from config import (
        TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, UPDATE_INTERVAL,
        ETH_WALLET, SOLANA_ADDRESSES, ETH_RPC, SOL_RPC
    )
except Exception as e:
    print("ERROR: could not import config.py -", e)
    sys.exit(1)

# third-party imports (may fail if not installed)
try:
    from telegram import Bot
    from telegram.constants import ParseMode
    from web3 import Web3
    from solders.pubkey import Pubkey
    from solana.rpc.async_api import AsyncClient as SolanaClient
except Exception as e:
    print("ERROR: missing Python packages:", e)
    print("Run the setup script to install requirements.")
    raise

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("icehub")

# init clients
bot = Bot(token=TELEGRAM_BOT_TOKEN)
w3 = Web3(Web3.HTTPProvider(ETH_RPC))
sol_client = SolanaClient(SOL_RPC)

async def get_eth_balance(address: str) -> float:
    try:
        if not w3.is_connected():
            log.warning("Web3 not connected to RPC")
            return 0.0
        addr = w3.to_checksum_address(address)
        bal_wei = w3.eth.get_balance(addr)
        return float(w3.from_wei(bal_wei, "ether"))
    except Exception as e:
        log.error("ETH balance error: %s: %s", type(e).__name__, e)
        return 0.0

async def get_solana_balance(address: str) -> float:
    try:
        pubkey = Pubkey.from_string(str(address))
        resp = await sol_client.get_balance(pubkey)
        if resp and hasattr(resp, "value"):
            return resp.value / 1_000_000_000.0
        return 0.0
    except Exception as e:
        log.error("SOL balance error: %s: %s", type(e).__name__, e)
        return 0.0

async def send_update():
    eth_bal = await get_eth_balance(ETH_WALLET)
    sol_parts = []
    for addr in SOLANA_ADDRESSES:
        s = await get_solana_balance(addr)
        sol_parts.append((addr, s))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    msg_lines = [
        "💎 <b>IceBoys Wallet Tracker</b>",
        f"🕓 {now}",
        "",
        "<b>Ethereum</b>",
        f"<code>{ETH_WALLET}</code>",
        f"Balance: <b>{eth_bal:.6f} ETH</b>",
        "",
        "<b>Solana</b>"
    ]
    for addr, b in sol_parts:
        msg_lines.append(f"<code>{addr}</code>")
        msg_lines.append(f"Balance: <b>{b:.6f} SOL</b>")
        msg_lines.append("")

    message = "\n".join(msg_lines)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
        log.info("Update posted to Telegram.")
    except Exception as e:
        log.error("Failed to send Telegram message: %s", e)

async def main_loop():
    log.info("🚀 IceHub Wallet Tracker started.")
    # warm up solana client
    try:
        await sol_client.is_connected()
    except Exception:
        pass
    while True:
        await send_update()
        await asyncio.sleep(int(UPDATE_INTERVAL))

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        log.info("Bot stopped by user.")
    finally:
        try:
            asyncio.run(sol_client.close())
        except Exception:
            pass
PY

echo "[+] Ensure permissions ..."
chmod +x "$BASE/bot_main.py"

echo "[+] Installing Python packages (may take a few minutes)..."
# Best-effort install. Termux may require extra system deps; we try pip first.
python -m pip install --upgrade pip setuptools wheel >/dev/null 2>&1 || true
python -m pip install python-telegram-bot==13.15 web3 urllib3 solana==0.36.9 solders aiohttp >/dev/null 2>&1 || true

echo "[+] Starting bot in background (logs -> $LOG) ..."
# kill existing run if any
pkill -f "bot_main.py" || true
nohup python "$BASE/bot_main.py" >> "$LOG" 2>&1 &

sleep 1
echo "[+] Started. Tail the log with:"
echo "    tail -n 200 -f $LOG"
echo "If you see continuous errors about packages, run the install commands manually."
