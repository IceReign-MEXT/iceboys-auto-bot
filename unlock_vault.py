#!/usr/bin/env python3
"""
unlock_vault.py
Decrypts icehub_vault.enc -> extracts to wallets_plain_unlocked, then securely cleans up.
"""
import os
import shlex
import subprocess
from pathlib import Path
import getpass
import sys

HOME = Path("/data/data/com.termux/files/home")
BASE = HOME / "icehub_system"
VAULT = BASE / "icehub_vault.enc"
PASSFILE = BASE / ".icehub_vault_pw"
TMP_TAR = BASE / "test_extract_unlocked.tar.gz"
EXTRACT_DIR = BASE / "wallets_plain_unlocked"

def run(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def get_password_arg():
    if PASSFILE.exists():
        return f"-pass file:{shlex.quote(str(PASSFILE))}", None
    pw = getpass.getpass("Enter vault passphrase (input hidden): ")
    tmp_pw = BASE / ".tmp_vault_pw"
    tmp_pw.write_text(pw)
    tmp_pw.chmod(0o600)
    return f"-pass file:{shlex.quote(str(tmp_pw))}", tmp_pw

def cleanup_temp_pw(tmp_pw_path):
    try:
        if tmp_pw_path and tmp_pw_path.exists():
            tmp_pw_path.unlink()
    except Exception:
        pass

def decrypt_vault(pass_arg):
    cmd = (
        f"openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in {shlex.quote(str(VAULT))} "
        f"-out {shlex.quote(str(TMP_TAR))} {pass_arg}"
    )
    print("Decrypting vault (may take a moment)...")
    rc, out, err = run(cmd)
    if rc != 0:
        print("✖ Decryption failed.")
        if err:
            print(err.strip())
        return False
    return True

def extract_tar():
    EXTRACT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    cmd = f"tar -xzf {shlex.quote(str(TMP_TAR))} -C {shlex.quote(str(EXTRACT_DIR))}"
    rc, out, err = run(cmd)
    if rc != 0:
        print("✖ Extraction failed.")
        if err:
            print(err.strip())
        return False
    return True

def secure_delete(path: Path):
    try:
        if path.exists():
            rc, out, err = run(f"shred -u {shlex.quote(str(path))}")
            if rc != 0:
                path.unlink(missing_ok=True)
    except Exception:
        path.unlink(missing_ok=True)

def cleanup_extracted():
    if EXTRACT_DIR.exists():
        print("Removing unlocked files...")
        for root, dirs, files in os.walk(EXTRACT_DIR, topdown=False):
            for name in files:
                secure_delete(Path(root) / name)
            for name in dirs:
                try:
                    (Path(root) / name).rmdir()
                except Exception:
                    pass
        try:
            EXTRACT_DIR.rmdir()
        except Exception:
            pass

def main():
    print("=== IceHub vault unlock helper ===")
    if not VAULT.exists():
        print("ERROR: Vault file not found:", VAULT)
        sys.exit(1)

    tmp_pw = None
    try:
        pa, tmp_pw = get_password_arg()
        ok = decrypt_vault(pa)
        if not ok:
            cleanup_temp_pw(tmp_pw)
            sys.exit(2)

        ok = extract_tar()
        if not ok:
            cleanup_temp_pw(tmp_pw)
            secure_delete(TMP_TAR)
            sys.exit(3)

        print("\nExtracted files to:", EXTRACT_DIR)
        for dirpath, _, filenames in os.walk(EXTRACT_DIR):
            for f in filenames:
                p = Path(dirpath) / f
                print(" -", str(p.relative_to(EXTRACT_DIR)))
        input("\nPress ENTER when you are done to securely remove the unlocked files.")
    finally:
        secure_delete(TMP_TAR)
        cleanup_temp_pw(tmp_pw)
        cleanup_extracted()
        print("Done. Vault locked again.")

if __name__ == "__main__":
    main()
