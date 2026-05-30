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