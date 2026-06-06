'''
Referensi ke DSA\graph
'''

from pathlib import Path

from rich import json

from .graph import Graph

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import heapq

class TopologiNode(Graph):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console()

    def tampilkan_topologi(self) -> None:
        if not self.graph:
            self.console.print(Text("Topologi node masih kosong.", style="bold red"))
            return
        
        topologi_text = Text(style="bold blue")
        topologi_panel = Panel(topologi_text, title="TOPOLOGI NODE", style="bold blue")

        for simpul, tetangga in self.graph.items():
            topologi_text.append(f"{simpul}: {', '.join(tetangga)}\n")
        
        self.console.print(topologi_panel)
    
    def dijkstra_topologi(self, start: str, end: str) -> dict | None:
        path = Path("src/data/dalam-json/topologi.json")
        dict_topologi = {
            "from": str,                # server_id asal, contoh: "SRV001"
            "from_name": str,           # nama server asal, contoh: "Alpha"
            "to": str,                  # server_id tujuan, contoh: "SRV007"
            "to_name": str,             # nama server tujuan, contoh: "Hydra"
            "total_latency_ms": int,    # total latency seluruh path (ms)
            "min_bandwidth_mbps": int,  # bottleneck — bandwidth terkecil di antara semua edge dalam path
            "path": []                  # daftar node dalam path
            }
        if not path.exists():
            self.console.print(Text("File topologi.json tidak ditemukan.", style="bold red"))
            return None
        with open(path, "r") as f:
            topologi_data = json.load(f)
        if start not in topologi_data or end not in topologi_data:
            self.console.print(Text("Simpul awal atau tujuan tidak ditemukan dalam topologi.", style="bold red"))
            return None
        # Implementasi Dijkstra untuk mencari path terpendek berdasarkan latency
        
        queue = [(0, start, float('inf'), [start])]  # (total_latency, current_node, min_bandwidth, path)
        visited = set()
        while queue:
            total_latency, current_node, min_bandwidth, path = heapq.heappop(queue)
            if current_node in visited:
                continue
            visited.add(current_node)
            if current_node == end:
                return {
                    "from": start,
                    "from_name": topologi_data[start]["name"],
                    "to": end,
                    "to_name": topologi_data[end]["name"],
                    "total_latency_ms": total_latency,
                    "min_bandwidth_mbps": min_bandwidth,
                    "path": path
                }
            for neighbor, edge in topologi_data[current_node]["edges"].items():
                if neighbor not in visited:
                    new_latency = total_latency + edge["latency_ms"]
                    new_min_bandwidth = min(min_bandwidth, edge["bandwidth_mbps"])
                    heapq.heappush(queue, (new_latency, neighbor, new_min_bandwidth, path + [neighbor]))
        self.console.print(Text("Tidak ada path yang ditemukan antara simpul awal dan tujuan.", style="bold red"))
        return None
    