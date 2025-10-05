#!/usr/bin/env python3
"""
vault_manager.py

Password-protected vault for private keys.
- Encrypts files into icehub_vault.bin
- Stores/reads public_addresses.json (safe to keep readable)
- Unlocks to show or export private keys (requires password)

Usage:
  # Create vault (encrypt current wallet private files):
  python vault_manager.py create

  # List public addresses:
  python vault_manager.py list

  # Unlock and print private keys to screen:
  python vault_manager.py unlock --show

  # Unlock and export decrypted files to /tmp/icehub_decrypted/ (then optionally delete)
  python vault_manager.py unlock --export

  # Remove exported temp files:
  python vault_manager.py clean-temp

Security notes:
- Choose a strong password. Do NOT share it.
- Keep icehub_vault.bin offline/backed up.
- Use this only on your own device.
"""
import os
import json
import getpass
import shutil
from pathlib import Path
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets
import argparse

HOME = Path.home()
BASE = HOME / "icehub_system"
WALLETS = BASE / "wallets"
VAULT_FILE = BASE / "icehub_vault.bin"
PUB_FILE = BASE / "public_addresses.json"
TEMP_DIR = Path("/data/data/com.termux/files/home/icehub_system/tmp_decrypted")

# Files we want to include in the vault (relative to WALLETS)
DEFAULT_FILES = [
    "eth_account.json",
    "eth_account_private_backup.txt",
    "sol_account.json",
    "sol_account_secret.raw",
    "sol_seed_phrase.txt"
]

def derive_key(password: bytes, salt: bytes) -> bytes:
    # 200,000 iterations - moderate; adjust higher if you want slower derivation.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    return kdf.derive(password)

def encrypt_bytes(key: bytes, data: bytes) -> bytes:
    # AES GCM
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce + ct

def decrypt_bytes(key: bytes, blob: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = blob[:12]
    ct = blob[12:]
    return aesgcm.decrypt(nonce, ct, None)

def create_vault(files=None):
    files = files or DEFAULT_FILES
    salt = secrets.token_bytes(16)
    password = getpass.getpass("Create vault password: ").encode()
    confirm = getpass.getpass("Confirm password: ").encode()
    if password != confirm:
        print("Passwords do not match. Aborting.")
        return
    key = derive_key(password, salt)
    # Build a small archive: JSON mapping filename -> base64(data)
    archive = {}
    for fn in files:
        p = WALLETS / fn
        if not p.exists():
            print(f"[warn] missing: {p} (skipping)")
            continue
        data = p.read_bytes()
        archive[fn] = urlsafe_b64encode(data).decode()
    payload = json.dumps(archive).encode()
    encrypted = encrypt_bytes(key, payload)
    # Store salt + encrypted
    with open(VAULT_FILE, "wb") as f:
        f.write(salt + encrypted)
    os.chmod(VAULT_FILE, 0o600)
    print("[+] Vault created:", VAULT_FILE)

def unlock_vault(password: bytes):
    if not VAULT_FILE.exists():
        print("Vault not found. Create it first.")
        return None
    raw = VAULT_FILE.read_bytes()
    salt = raw[:16]
    blob = raw[16:]
    key = derive_key(password, salt)
    try:
        data = decrypt_bytes(key, blob)
    except Exception as e:
        print("Decryption failed. Wrong password or corrupted vault.")
        return None
    archive = json.loads(data.decode())
    # decode base64 back to bytes
    decoded = {k: urlsafe_b64decode(v.encode()) for k,v in archive.items()}
    return decoded

def show_private(password):
    decoded = unlock_vault(password)
    if not decoded:
        return
    print("=== Decrypted private key files ===")
    for fn, raw in decoded.items():
        print(f"\n--- {fn} ---")
        # show only first & last 80 chars if very long
        text = raw.decode(errors="ignore")
        if len(text) > 800:
            print(text[:400])
            print("\n... (truncated) ...\n")
            print(text[-400:])
        else:
            print(text)

def export_decrypted(password, dest=None):
    decoded = unlock_vault(password)
    if not decoded:
        return
    dest = Path(dest or TEMP_DIR)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for fn, raw in decoded.items():
        out = dest / fn
        out.write_bytes(raw)
        os.chmod(out, 0o600)
    print("[+] Exported decrypted files to:", dest)
    print("[!] Remember to delete them after use: python vault_manager.py clean-temp")

def clean_temp():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print("[+] Temporary decrypted files removed.")
    else:
        print("[*] No temp directory to remove.")

def create_public_addresses_file(addrs: dict):
    PUB_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Only store public addresses, never private keys here
    with open(PUB_FILE, "w") as f:
        json.dump(addrs, f, indent=2)
    os.chmod(PUB_FILE, 0o644)
    print("[+] Public addresses saved to:", PUB_FILE)

def list_public():
    if not PUB_FILE.exists():
        print("[!] No public_addresses.json found.")
        return
    print(PUB_FILE.read_text())

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["create","list","unlock","clean-temp","init-public"])
    p.add_argument("--show", action="store_true", help="show decrypted content on screen (use with unlock)")
    p.add_argument("--export", action="store_true", help="export decrypted files to temp dir (use with unlock)")
    p.add_argument("--public-file", type=str, help="Path to JSON file with public addresses to initialize")
    return p.parse_args()

def main():
    args = parse_args()
    if args.action == "create":
        # include defaults - you can adapt by editing DEFAULT_FILES above
        create_vault()
    elif args.action == "list":
        list_public()
    elif args.action == "unlock":
        pw = getpass.getpass("Enter vault password: ").encode()
        if args.show:
            show_private(pw)
        elif args.export:
            export_decrypted(pw)
        else:
            print("Use --show to print or --export to export files")
    elif args.action == "clean-temp":
        clean_temp()
    elif args.action == "init-public":
        # read given JSON file or build from detected public keys
        if args.public_file:
            path = Path(args.public_file)
            if not path.exists():
                print("Provided public file not found:", path)
                return
            addrs = json.loads(path.read_text())
            create_public_addresses_file(addrs)
            return
        # auto detect public files in wallets/
        addrs = {}
        # ETH
        ethf = WALLETS / "eth_account.json"
        try:
            if ethf.exists():
                j = json.loads(ethf.read_text())
                addrs["ethereum"] = j.get("address")
        except Exception:
            pass
        # SOL
        solf = WALLETS / "sol_account.json"
        try:
            if solf.exists():
                j = json.loads(solf.read_text())
                addrs["solana"] = j.get("public_key_base58") or j.get("public_key_hex")
        except Exception:
            pass
        # other public addresses - if you want add them manually
        create_public_addresses_file(addrs)
    else:
        print("Unknown action")

if __name__ == "__main__":
    main()
