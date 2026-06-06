'''
Graph adalah struktur data yang digunakan untuk merepresentasikan hubungan antara objek-objek. Graph terdiri dari simpul (nodes) dan sisi (edges) yang menghubungkan simpul-simpul tersebut. Graph dapat digunakan untuk berbagai aplikasi seperti jaringan sosial, peta jalan, dan banyak lagi.
'''


from pathlib import Path
import json


class Graph:
    def __init__(self):
        # Menyimpan graf dalam bentuk adjacency list
        self.graph = {}

    def tambah_simpul(self, simpul):
        if simpul not in self.graph:
            self.graph[simpul] = []

    def tambah_sisi(self, simpul1, simpul2):
        self.tambah_simpul(simpul1)
        self.tambah_simpul(simpul2)
        self.graph[simpul1].append(simpul2)
        self.graph[simpul2].append(simpul1)
    
    def tampilkan_graf(self):
        for simpul, tetangga in self.graph.items():
            print(f"{simpul}: {', '.join(tetangga)}")

    def dijkstra(self, start):
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