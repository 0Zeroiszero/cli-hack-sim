'''
Graph adalah struktur data yang digunakan untuk merepresentasikan hubungan antara objek-objek. Graph terdiri dari simpul (nodes) dan sisi (edges) yang menghubungkan simpul-simpul tersebut. Graph dapat digunakan untuk berbagai aplikasi seperti jaringan sosial, peta jalan, dan banyak lagi.
'''


from pathlib import Path
import json



class Graph:
    def __init__(self):
        # Menyimpan graf dalam bentuk adjacency list
        self.graph = {}

    def build_from_json(self, filepath:str) ->  None:
        topologi_path = Path("../../src/data/dalam-json/topologi.json")
        akunserver_path = Path("../../src/data/dalam-json/akun_dan_status_server.json")

        with open(akunserver_path, "r") as f:
            akunserver = f.read()
        with open(topologi_path, "r") as f:
            topologi = f.read()
        
        for topologi_key, topologi_value in topologi:
            list_hubungan = []
            list_hubungan.append(self.graph[topologi_value]["to"])
            self.graph[topologi_key] = list(list_hubungan)
        return self.graph

    def get_adjacency_list(self) -> dict:
        topologi_path = Path("../../src/data/dalam-json/topologi.json")
        akunserver_path = Path("../../src/data/dalam-json/akun_dan_status_server.json")

        with open(akunserver_path, "r") as f:
            akunserver = f.read()
        with open(topologi_path, "r") as f:
            topologi = f.read()
        
        for topologi_key, topologi_value in topologi:
            self.graph[topologi_key] = topologi_value
            to = self.graph[topologi_value]["to"]
            to_name = akunserver["servers"]["server_name"] if akunserver["servers"]["server_id"] == to else None
            self.graph[topologi_value]["to_name"] = to_name
        return self.graph

    def dijkstra(self, start:str, end:str) -> dict | None:
        # Inisialisasi jarak ke semua simpul sebagai tak hingga
        jarak = {simpul: float('inf') for simpul in self.graph}
        jarak[start] = 0
        queue = [(0, start)]

        while queue:
            current_distance, current_node = queue

            # Jika jarak yang diambil lebih besar dari jarak yang sudah diketahui, lewati
            if current_distance > jarak[current_node]:
                continue

            for neighbor in self.graph[current_node]:
                distance = current_distance + 1  # Asumsi setiap sisi memiliki bobot 1

                if distance < jarak[neighbor]:
                    jarak[neighbor] = distance
                    queue(distance, neighbor)

        return jarak