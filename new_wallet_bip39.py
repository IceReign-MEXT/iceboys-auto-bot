from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from solana.keypair import Keypair
import base58

# === Generate a real BIP-39 12-word mnemonic ===
mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
print("=== BIP-39 Solana Wallet ===")
print("Seed Phrase:", mnemonic)
print("=================================")

# === Derive Solana keypair ===
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
account = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

private_key = account.PrivateKey().Raw().ToBytes()
public_key = account.PublicKey().RawCompressed().ToBytes()

# Solana uses Ed25519 keys, so we convert properly
kp = Keypair.from_secret_key(private_key)

print("Public Key:", kp.public_key)
print("Secret Key (base58):", base58.b58encode(kp.secret_key).decode())
print("\nSave this phrase safely — it can restore your wallet in Phantom or Solflare.")
