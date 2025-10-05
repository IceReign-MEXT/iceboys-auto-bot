import secrets

# Simple 12-word mnemonic generator (not BIP39 full)
words = [
    "apple", "banana", "cat", "dog", "eagle", "fish", "gold", "house", "ice", "jungle",
    "kite", "lion", "moon", "night", "orange", "purple", "queen", "river", "sun", "tree",
    "umbrella", "village", "wolf", "xray", "yarn", "zebra"
]

mnemonic = " ".join(secrets.choice(words) for _ in range(12))
print("=== Solana Wallet Mnemonic (Seed Phrase) ===")
print(mnemonic)
print("\nIMPORTANT: Save this phrase somewhere safe — it restores your Solana wallet.")
