from solana.keypair import Keypair
import base58

# ⚠️ Replace this only with your own secret key string.
# Do NOT share it with anyone else.
secret_key_b58 = "HxmywH2gW9ezQ2nBXwurpaWsZS6YvdmLF23R9WgMAM7p"

# Your public wallet address to verify against
expected_public_key = "F2Lz21btaZax8jVxrtj75Jw5tewFgXhrA4CAi3HzZteS"

try:
    secret_bytes = base58.b58decode(secret_key_b58)
    keypair = Keypair.from_secret_key(secret_bytes)
    derived_pub = str(keypair.public_key)

    if derived_pub == expected_public_key:
        print("✅ Match confirmed: this private key belongs to your wallet.")
    else:
        print("❌ Not a match. This secret key does NOT generate that public wallet.")
        print("Derived Public Key:", derived_pub)

except Exception as e:
    print("⚠️ Error decoding key:", e)
