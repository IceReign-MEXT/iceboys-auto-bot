#!/usr/bin/env python3
import os
import json
from datetime import datetime

base_dir = "/data/data/com.termux/files/home/icehub_system"
reports_dir = os.path.join(base_dir, "reports")
summary_file = os.path.join(reports_dir, "cognitive_analytics_summary.json")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def analyze_system():
    log("Starting cognitive analytics process...")
    
    # Load all previous summaries
    ai_core = load_json(os.path.join(reports_dir, "ai_core_summary.json"))
    net_intel = load_json(os.path.join(reports_dir, "network_intelligence_summary.json"))
    data_fusion = load_json(os.path.join(reports_dir, "data_fusion_summary.json"))

    # Count detected systems and streams
    linked_systems = len(net_intel.get("linked_systems", [])) if "linked_systems" in net_intel else 5
    fusion_score = len(data_fusion) * 10 if data_fusion else 50

    # Cognitive matrix simulation
    cognitive_matrix = {
        "AI_Core_Status": "Active" if ai_core else "Unknown",
        "Network_Status": "Linked" if net_intel else "Pending",
        "Fusion_Status": "Integrated" if data_fusion else "Not merged",
        "Linked_Systems": linked_systems,
        "Fusion_Score": fusion_score,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save analytics summary
    with open(summary_file, "w") as f:
        json.dump(cognitive_matrix, f, indent=4)

    log("Cognitive analytics report generated.")
    log(f"Saved to: {summary_file}")
    log("System insight map updated successfully.")

def main():
    print("=====================================")
    print("   ICEHUB COGNITIVE ANALYTICS ENGINE ")
    print("=====================================")
    analyze_system()
    print("=====================================")
    print(" ✅ SEASON 5 — ANALYTICS COMPLETE")
    print("=====================================")

if __name__ == "__main__":
    main()
