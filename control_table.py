#!/usr/bin/env python3
import os
import time
from datetime import datetime

BASE_PATH = os.path.expanduser("~/icehub_system")
REPORT_FILE = os.path.join(BASE_PATH, "control_log.txt")

def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REPORT_FILE, "a") as f:
        f.write(f"[{now}] {message}\n")
    print(f"[{now}] {message}")

def setup_directories():
    paths = [
        "engine/",
        "reports/",
        "ai_core/",
        "network/",
        "temp/",
    ]
    for p in paths:
        full = os.path.join(BASE_PATH, p)
        os.makedirs(full, exist_ok=True)
        log(f"Created directory: {full}")

def summary():
    files = sum(len(files) for _, _, files in os.walk(BASE_PATH))
    dirs = sum(len(dirs) for _, dirs, _ in os.walk(BASE_PATH))
    log(f"System summary — Directories: {dirs}, Files: {files}")

if __name__ == "__main__":
    log("==== ICEHUB CONTROL SYSTEM STARTED ====")
    setup_directories()
    summary()
    log("==== SYSTEM READY FOR NEXT MOVEMENT ====")
