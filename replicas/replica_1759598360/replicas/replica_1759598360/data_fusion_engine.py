#!/usr/bin/env python3
import os
import json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/icehub_system")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FUSION_LOG = os.path.join(REPORTS_DIR, "data_fusion_summary.json")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def main():
    print("=====================================")
    print("   ICEHUB DATA FUSION ENGINE - S4")
    print("=====================================")

    log("Starting data fusion process...")

    ai_core = load_json(os.path.join(REPORTS_DIR, "ai_core_summary.json"))
    network_data = load_json(os.path.join(REPORTS_DIR, "network_intelligence_summary.json"))

    fused = {
        "timestamp": datetime.now().isoformat(),
        "ai_core_summary": ai_core,
        "network_summary": network_data,
        "fusion_status": "complete",
        "insight": "Data successfully combined across IceHub layers."
    }

    with open(FUSION_LOG, "w") as f:
        json.dump(fused, f, indent=4)

    log(f"Fusion summary saved to: {FUSION_LOG}")
    log("System intelligence matrix updated successfully.")
    print("=====================================")
    print(" ✅ SEASON 4 — DATA FUSION COMPLETE")
    print("=====================================")

if __name__ == "__main__":
    main()
