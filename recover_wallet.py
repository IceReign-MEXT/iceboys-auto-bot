from solana.keypair import Keypair
from solana.publickey import PublicKey
import base58
import hashlib

def mnemonic_to_keypair(mnemonic: str):
    # Deterministic 32-byte seed from your mnemonic
    seed = hashlib.sha256(mnemonic.encode("utf-8")).digest()
    kp = Keypair.from_seed(seed)
    return kp

mnemonic = input("tray dirt celery ranch display collect sphere defy child delay swift anxiety ").strip()
kp = mnemonic_to_keypair(mnemonic)

print("\n✅ Wallet derived successfully!")
print("Public Key:", kp.public_key)
print("Secret Key (base58):", base58.b58encode(kp.secret_key).decode())
