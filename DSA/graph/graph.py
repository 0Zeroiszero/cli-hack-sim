"""@author: Alif Akbar; @modified: Abdullah Affandi

Graph adalah struktur data untuk merepresentasikan hubungan antar-objek.
Graph terdiri dari simpul (nodes) dan sisi (edges) yang menghubungkan
simpul-simpul tersebut. Graph dapat digunakan untuk berbagai aplikasi
seperti jaringan sosial, peta jalan, dan banyak lagi.
"""

from pathlib import Path

from src.filehandler import FileHandler


class Graph:
    """Representasi graph menggunakan adjacency list.

    Setiap edge menyimpan informasi latency (weight untuk Dijkstra),
    bandwidth, dan arah koneksi (two_way).
    """

    def __init__(self):
        """Menyimpan graf dalam bentuk adjacency list."""
        self.graph = {}

    def _add_reverse_edge(self, edge, server_id):
        """Menambahkan reverse edge jika koneksi two_way."""
        if not edge["two_way"]:
            return
        reverse_edge = {
            "to": server_id,
            "latency_ms": edge["latency_ms"],
            "bandwidth_mbps": edge["bandwidth_mbps"],
            "two_way": True,
        }
        if edge["to"] not in self.graph:
            self.graph[edge["to"]] = []
        # Cegah duplikasi jika reverse edge sudah ada
        for e in self.graph[edge["to"]]:
            if e["to"] == server_id:
                return
        self.graph[edge["to"]].append(reverse_edge)

    def build_from_json(self, filepath):
        """Membangun adjacency list dari file topologi JSON.

        Args:
            filepath: Path ke file topologi.json.
        """
        topologi = FileHandler().load_json(filepath)
        self.graph = {}

        for server_id, edges in topologi.items():
            if server_id not in self.graph:
                self.graph[server_id] = []
            for edge in edges:
                self.graph[server_id].append(dict(edge))
                self._add_reverse_edge(edge, server_id)

        # Pastikan semua server tujuan memiliki entri (meski kosong)
        for edges in topologi.values():
            for edge in edges:
                if edge["to"] not in self.graph:
                    self.graph[edge["to"]] = []

    def get_adjacency_list(self):
        """Mengembalikan adjacency list yang diperkaya dengan nama server.

        Returns:
            dict — setiap edge dict memiliki field tambahan
            "to_name" yang berisi nama server tujuan.
        """
        server_data = FileHandler().load_json(
            Path("src/data/dalam-json/akun_dan_status_server.json"),
        )
        server_names = {}
        for s in server_data.get("servers", []):
            server_names[s["server_id"]] = s["server_name"]

        result = {}
        for server_id, edges in self.graph.items():
            enriched = []
            for edge in edges:
                enriched.append(
                    {
                        "to": edge["to"],
                        "to_name": server_names.get(edge["to"], "Unknown"),
                        "latency_ms": edge["latency_ms"],
                        "bandwidth_mbps": edge["bandwidth_mbps"],
                        "two_way": edge["two_way"],
                    },
                )
            result[server_id] = enriched
        return result

    def _find_closest_unvisited(self, jarak, visited):
        """Mencari simpul belum dikunjungi dengan jarak terkecil."""
        current = None
        min_jarak = float("inf")
        for simpul in self.graph:
            if simpul not in visited and jarak[simpul] < min_jarak:
                min_jarak = jarak[simpul]
                current = simpul
        return current

    def _reconstruct_path(self, previous, end):
        """Rekonstruksi path dari end ke start berdasarkan previous."""
        path_hops = []
        current = end
        while previous[current] is not None:
            info = previous[current]
            path_hops.insert(
                0,
                {
                    "from": info["from"],
                    "to": current,
                    "latency_ms": info["edge"]["latency_ms"],
                    "bandwidth_mbps": info["edge"]["bandwidth_mbps"],
                    "two_way": info["edge"]["two_way"],
                },
            )
            current = info["from"]
        return path_hops

    def _enrich_path_with_names(self, path_hops):
        """Menambahkan from_name dan to_name ke setiap hop.

        Returns:
            dict mapping server_id -> server_name.
        """
        server_data = FileHandler().load_json(
            Path("src/data/dalam-json/akun_dan_status_server.json"),
        )
        server_names = {}
        for s in server_data.get("servers", []):
            server_names[s["server_id"]] = s["server_name"]

        for hop in path_hops:
            hop["from_name"] = server_names.get(hop["from"], "Unknown")
            hop["to_name"] = server_names.get(hop["to"], "Unknown")
        return server_names

    def dijkstra(self, start, end):
        """Mencari rute terpendek berdasarkan total latency terkecil.

        Args:
            start: Server ID asal (contoh: "SRV001").
            end: Server ID tujuan (contoh: "SRV007").

        Returns:
            dict jika ditemukan, None jika tidak ada jalur.
        """
        if start not in self.graph or end not in self.graph:
            return None

        jarak = {s: float("inf") for s in self.graph}
        jarak[start] = 0
        previous = {s: None for s in self.graph}
        visited = set()

        while len(visited) < len(self.graph):
            current = self._find_closest_unvisited(jarak, visited)
            if current is None or jarak[current] == float("inf"):
                break
            if current == end:
                break
            visited.add(current)
            for edge in self.graph[current]:
                neighbor = edge["to"]
                if neighbor in visited:
                    continue
                distance = jarak[current] + edge["latency_ms"]
                if distance < jarak[neighbor]:
                    jarak[neighbor] = distance
                    previous[neighbor] = {"from": current, "edge": edge}

        if jarak[end] == float("inf"):
            return None

        path_hops = self._reconstruct_path(previous, end)
        server_names = self._enrich_path_with_names(path_hops)
        min_bandwidth = min(h["bandwidth_mbps"] for h in path_hops)

        return {
            "from": start,
            "from_name": server_names.get(start, "Unknown"),
            "to": end,
            "to_name": server_names.get(end, "Unknown"),
            "total_latency_ms": int(jarak[end]),
            "min_bandwidth_mbps": min_bandwidth,
            "path": path_hops,
        }
