"""@author: Alif Akbar; @modified: Abdullah Affandi

Graph adalah struktur data untuk merepresentasikan hubungan antar-objek.
Graph terdiri dari simpul (nodes) dan sisi (edges) yang menghubungkan
simpul-simpul tersebut.
"""

from pathlib import Path

from src.filehandler import FileHandler


class Graph:
    """Representasi graph menggunakan adjacency list."""

    def __init__(self):
        self.graph = {}

    def build_from_json(self, filepath):  # noqa: C901
        """Membangun adjacency list dari file topologi JSON."""
        topologi = FileHandler().load_json(filepath)
        self.graph = {}

        for server_id, edges in topologi.items():
            if server_id not in self.graph:
                self.graph[server_id] = []

            for edge in edges:
                # Simpan edge asli
                self.graph[server_id].append(dict(edge))

                # Kalo two_way True, tambahin reverse edge
                if edge["two_way"]:
                    reverse = {
                        "to": server_id,
                        "latency_ms": edge["latency_ms"],
                        "bandwidth_mbps": edge["bandwidth_mbps"],
                        "two_way": True,
                    }
                    if edge["to"] not in self.graph:
                        self.graph[edge["to"]] = []
                    # Cegah duplikasi
                    sudah_ada = False
                    for e in self.graph[edge["to"]]:
                        if e["to"] == server_id:
                            sudah_ada = True
                            break
                    if not sudah_ada:
                        self.graph[edge["to"]].append(reverse)

        # Pastikan server tujuan punya entri walau kosong
        for edges in topologi.values():
            for edge in edges:
                if edge["to"] not in self.graph:
                    self.graph[edge["to"]] = []

    def get_adjacency_list(self):
        """Ngembaliin adjacency list yang udah ditambahin nama server."""
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

    def dijkstra(self, start, end):  # noqa: C901
        """Cari rute terpendek pake algoritma Dijkstra (weight = latency).

        Args:
            start: server_id asal (contoh: "SRV001")
            end: server_id tujuan (contoh: "SRV007")

        Returns:
            dict kalo ketemu, None kalo gak ada jalur.
        """
        # ── 1. Kalo start/end gak ada di graph, langsung None ──
        if start not in self.graph or end not in self.graph:
            return None

        # ── 2. Set jarak awal ──
        # jarak ke semua server = tak terhingga
        jarak = {}
        for s in self.graph:
            jarak[s] = float("inf")
        jarak[start] = 0  # jarak dari start ke dirinya sendiri = 0

        # nyimpen server sebelumnya buat rekonstruksi path nanti
        previous = {}
        for s in self.graph:
            previous[s] = None

        # server yang udah diproses
        visited = set()

        # ── 3. Loop utama Dijkstra ──
        while len(visited) < len(self.graph):
            # Cari server dengan jarak terkecil yang belum dikunjungi
            current = None
            min_jarak = float("inf")
            for s in self.graph:
                if s not in visited and jarak[s] < min_jarak:
                    min_jarak = jarak[s]
                    current = s

            # Kalo gak ada yang bisa dikunjungi lagi, berhenti
            if current is None or jarak[current] == float("inf"):
                break

            # Kalo udah sampe tujuan, berhenti
            if current == end:
                break

            visited.add(current)

            # Cek semua tetangga dari server yang sekarang
            for edge in self.graph[current]:
                tetangga = edge["to"]
                if tetangga in visited:
                    continue

                # Hitung jarak baru = jarak current + latency ke tetangga
                jarak_baru = jarak[current] + edge["latency_ms"]

                # Kalo lebih pendek dari jarak yang udah tercatat, update
                if jarak_baru < jarak[tetangga]:
                    jarak[tetangga] = jarak_baru
                    previous[tetangga] = {"from": current, "edge": edge}

        # ── 4. Kalo tujuan gak terjangkau, return None ──
        if jarak[end] == float("inf"):
            return None

        # ── 5. Rekonstruksi path dari tujuan balik ke start ──
        path_hops = []
        current = end
        while previous[current] is not None:
            info = previous[current]
            # masukin ke depan (biar urut dari start ke end)
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

        # ── 6. Ambil nama server dari file JSON ──
        server_data = FileHandler().load_json(
            Path("src/data/dalam-json/akun_dan_status_server.json"),
        )
        server_names = {}
        for s in server_data.get("servers", []):
            server_names[s["server_id"]] = s["server_name"]

        # Tambahin nama ke setiap hop
        for hop in path_hops:
            hop["from_name"] = server_names.get(hop["from"], "Unknown")
            hop["to_name"] = server_names.get(hop["to"], "Unknown")

        # Cari bandwidth terkecil di sepanjang path (bottleneck)
        min_bandwidth = float("inf")
        for hop in path_hops:
            if hop["bandwidth_mbps"] < min_bandwidth:
                min_bandwidth = hop["bandwidth_mbps"]

        # ── 7. Return hasil ──
        return {
            "from": start,
            "from_name": server_names.get(start, "Unknown"),
            "to": end,
            "to_name": server_names.get(end, "Unknown"),
            "total_latency_ms": int(jarak[end]),
            "min_bandwidth_mbps": min_bandwidth,
            "path": path_hops,
        }


if __name__ == "__main__":
    from pprint import pprint

    g = Graph()
    g.build_from_json(Path("src/data/dalam-json/topologi.json"))

    print("Dijkstra")
    pprint(g.dijkstra("SRV001", "SRV006"))
