#!/usr/bin/env python3
import os
import json
import datetime

# Base paths
BASE_DIR = os.path.expanduser("~/icehub_system")
AI_CORE_DIR = os.path.join(BASE_DIR, "ai_core")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def create_core_files():
    # AI identity file
    identity = {
        "AI_NAME": "ICEBRAIN",
        "VERSION": "2.0-ALPHA",
        "CREATOR": "IceReign-MEXT",
        "CREATED_ON": str(datetime.datetime.now()),
        "STATE": "INITIALIZED",
        "MODE": "LEARNING"
    }
    with open(os.path.join(AI_CORE_DIR, "identity.json"), "w") as f:
        json.dump(identity, f, indent=4)
    log("AI identity file created.")

    # AI memory seed
    memory_seed = {
        "last_update": str(datetime.datetime.now()),
        "logs": [],
        "insights": [],
        "connections": []
    }
    with open(os.path.join(AI_CORE_DIR, "memory.json"), "w") as f:
        json.dump(memory_seed, f, indent=4)
    log("AI memory initialized.")

    # AI configuration
    config = {
        "learning_rate": 0.02,
        "scan_frequency": "daily",
        "auto_log": True,
        "debug_mode": True
    }
    with open(os.path.join(AI_CORE_DIR, "config.json"), "w") as f:
        json.dump(config, f, indent=4)
    log("AI configuration file created.")

def create_report():
    summary = {
        "timestamp": str(datetime.datetime.now()),
        "status": "AI CORE ACTIVATED",
        "ai_files": os.listdir(AI_CORE_DIR),
        "location": AI_CORE_DIR
    }
    path = os.path.join(REPORTS_DIR, "ai_core_summary.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=4)
    log(f"AI core summary saved to {path}")

def main():
    print("=" * 37)
    print("  ICEHUB AI CORE ACTIVATION - SEASON 2  ")
    print("=" * 37)

    if not os.path.exists(AI_CORE_DIR):
        os.makedirs(AI_CORE_DIR)
        log(f"Created AI core directory: {AI_CORE_DIR}")

    create_core_files()
    create_report()

    log("AI Core setup complete. System ready for data linking.")
    print("=" * 37)
    print("   ✅ SEASON 2 SUCCESSFULLY DEPLOYED")
    print("=" * 37)

if __name__ == "__main__":
    main()
