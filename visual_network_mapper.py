#!/usr/bin/env python3
import os, json, datetime

base_path = "/data/data/com.termux/files/home/icehub_system"
reports_path = os.path.join(base_path, "reports")
output_file = os.path.join(reports_path, "network_visual_map.json")

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

def collect_reports():
    reports = []
    for file in os.listdir(reports_path):
        if file.endswith(".json"):
            reports.append(file)
    return reports

def create_graph_structure(reports):
    nodes = []
    edges = []

    for r in reports:
        name = r.replace("_summary.json", "").replace(".json", "")
        nodes.append(name)

    # Define connections (logical order)
    for i in range(len(nodes) - 1):
        edges.append({"from": nodes[i], "to": nodes[i + 1]})

    graph = {
        "timestamp": str(datetime.datetime.now()),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "nodes": nodes,
        "edges": edges
    }
    return graph

def main():
    print("=====================================")
    print("   ICEHUB VISUAL NETWORK MAPPER - S12")
    print("=====================================")
    log("Starting network visualization mapping...")
    reports = collect_reports()
    log(f"Detected {len(reports)} report files.")

    graph = create_graph_structure(reports)
    with open(output_file, "w") as f:
        json.dump(graph, f, indent=4)

    log(f"Visualization map saved to: {output_file}")
    log("Mapping summary:")
    print(json.dumps(graph, indent=4))
    print("=====================================")
    print(" ✅ SEASON 12 — VISUAL MAPPING COMPLETE")
    print("=====================================")

if __name__ == "__main__":
    main()
