"""Modul struktur data Graph untuk representasi topologi jaringan.

Graph adalah struktur data untuk merepresentasikan hubungan antar-objek.
Graph terdiri dari simpul (nodes) dan sisi (edges) yang menghubungkan
simpul-simpul tersebut.

@author: Alif Akbar
@modified: Abdullah Affandi
"""

from pathlib import Path

from src.filehandler import FileHandler


class Graph:
    """Representasi graph menggunakan adjacency list.

    Graph menyimpan hubungan antar server dalam bentuk adjacency list,
    di mana setiap server (node) memiliki daftar edge (sisi) yang
    terhubung ke server lain.

    Attributes:
        graph: Adjacency list berupa dict {server_id: list[edge_dict]}.

    """

    def __init__(self) -> None:
        """Inisialisasi graph kosong."""
        self.graph: dict[str, list[dict]] = {}

    def build_from_json(self, filepath: str | Path) -> None:  # noqa: C901
        """Membangun adjacency list dari file topologi JSON.

        Membaca file JSON yang berisi topologi jaringan, lalu membangun
        adjacency list. Edge dengan two_way=True akan otomatis dibuatkan
        reverse edge.

        Args:
            filepath: Path ke file JSON topologi.

        """
        topologi = FileHandler().load_json(filepath)
        self.graph = {}

        for server_id, edges in topologi.items():
            if server_id not in self.graph:
                self.graph[server_id] = []

            for edge in edges:
                self.graph[server_id].append(dict(edge))

                if edge["two_way"]:
                    reverse = {
                        "to": server_id,
                        "latency_ms": edge["latency_ms"],
                        "bandwidth_mbps": edge["bandwidth_mbps"],
                        "two_way": True,
                    }
                    if edge["to"] not in self.graph:
                        self.graph[edge["to"]] = []
                    sudah_ada = False
                    for e in self.graph[edge["to"]]:
                        if e["to"] == server_id:
                            sudah_ada = True
                            break
                    if not sudah_ada:
                        self.graph[edge["to"]].append(reverse)

        for edges in topologi.values():
            for edge in edges:
                if edge["to"] not in self.graph:
                    self.graph[edge["to"]] = []

    def get_adjacency_list(self) -> dict[str, list[dict]]:
        """Mengembalikan adjacency list yang sudah diperkaya dengan nama server.

        Membaca data server dari file JSON untuk menambahkan informasi
        nama server pada setiap edge.

        Returns:
            dict: Adjacency list dengan format
            {server_id: [{"to", "to_name", "latency_ms", "bandwidth_mbps", "two_way"}, ...]}.

        """
        server_data = FileHandler().load_json(
            Path("data/dalam-json/akun_dan_status_server.json"),
        )
        server_names: dict[str, str] = {}
        for s in server_data.get("servers", []):
            server_names[s["server_id"]] = s["server_name"]

        result: dict[str, list[dict]] = {}
        for server_id, edges in self.graph.items():
            enriched: list[dict] = []
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

    def dijkstra(  # noqa: C901
        self,
        start: str,
        end: str,
    ) -> dict | None:
        """Mencari rute terpendek menggunakan algoritma Dijkstra.

        Weight yang digunakan adalah latency_ms. Fungsi ini mengembalikan
        rute terpendek beserta total latency dan bandwidth terkecil
        (bottleneck) di sepanjang path.

        Args:
            start: Server ID asal (contoh: "SRV001").
            end: Server ID tujuan (contoh: "SRV007").

        Returns:
            dict jika rute ditemukan dengan format:
            {
                "from": str,
                "from_name": str,
                "to": str,
                "to_name": str,
                "total_latency_ms": int,
                "min_bandwidth_mbps": float,
                "path": list[dict],
            }
            None jika tidak ada jalur yang tersedia.

        """
        if start not in self.graph or end not in self.graph:
            return None

        jarak: dict[str, float] = {}
        for s in self.graph:
            jarak[s] = float("inf")
        jarak[start] = 0

        previous: dict[str, dict | None] = {}
        for s in self.graph:
            previous[s] = None

        visited: set[str] = set()

        while len(visited) < len(self.graph):
            current = None
            min_jarak = float("inf")
            for s in self.graph:
                if s not in visited and jarak[s] < min_jarak:
                    min_jarak = jarak[s]
                    current = s

            if current is None or jarak[current] == float("inf"):
                break

            if current == end:
                break

            visited.add(current)

            for edge in self.graph[current]:
                tetangga = edge["to"]
                if tetangga in visited:
                    continue

                jarak_baru = jarak[current] + edge["latency_ms"]

                if jarak_baru < jarak[tetangga]:
                    jarak[tetangga] = jarak_baru
                    previous[tetangga] = {"from": current, "edge": edge}

        if jarak[end] == float("inf"):
            return None

        path_hops: list[dict] = []
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

        server_data = FileHandler().load_json(
            Path("data/dalam-json/akun_dan_status_server.json"),
        )
        server_names: dict[str, str] = {}
        for s in server_data.get("servers", []):
            server_names[s["server_id"]] = s["server_name"]

        for hop in path_hops:
            hop["from_name"] = server_names.get(hop["from"], "Unknown")
            hop["to_name"] = server_names.get(hop["to"], "Unknown")

        min_bandwidth = float("inf")
        for hop in path_hops:
            if hop["bandwidth_mbps"] < min_bandwidth:
                min_bandwidth = hop["bandwidth_mbps"]

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
    g.build_from_json(Path("data/dalam-json/topologi.json"))

    print("Dijkstra")
    pprint(g.dijkstra("SRV001", "SRV006"))
