from solders.keypair import Keypair
from mnemonic import Mnemonic
from datetime import datetime
import json, os

mnemo = Mnemonic("english")
seed_phrase = mnemo.generate(strength=128)

kp = Keypair.from_seed(mnemo.to_seed(seed_phrase)[:32])

os.makedirs("/data/data/com.termux/files/home/icehub_system/wallets", exist_ok=True)
with open("/data/data/com.termux/files/home/icehub_system/wallets/sol_seed_phrase.txt", "w") as f:
    f.write(seed_phrase + "\n")

summary = {
    "public_key_base58": str(kp.pubkey()),
    "created_at": datetime.utcnow().isoformat() + "Z"
}
with open("/data/data/com.termux/files/home/icehub_system/wallets/sol_seed_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== ✅ VALID SOLANA WALLET GENERATED ===")
print("Seed Phrase:", seed_phrase)
print("Public Key:", kp.pubkey())
print("Saved to: ~/icehub_system/wallets/sol_seed_phrase.txt")
