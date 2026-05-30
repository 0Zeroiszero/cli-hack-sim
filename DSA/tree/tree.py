from importlib.resources import contents
from pathlib import Path
from platform import node
from platform import node
from sys import prefix

class TreeNode:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def cetak_tree(node: TreeNode, prefix: str = ""):
        # Mencetak node saat ini
        print(f"{prefix}|-- {node.name}")

        # Rekursi untuk setiap anak
        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            extension = "    " if is_last else "│   "
            cetak_tree(child, prefix + extension)

        # Mengurutkan agar folder tampil lebih dulu
        contents.sort(key=lambda x: (not x.is_dir(), x.name))
    
        # Loop untuk menampilkan setiap item
        for i, path in enumerate(contents):
            is_last = i == len(contents) - 1
            connector = "└── " if is_last else "├── "
        
            print(f"{prefix}{connector}{path.name}")
        
        # Jika item adalah folder, lakukan rekursi
            if path.is_dir():
                extension = "    " if is_last else "│   "
                cetak_tree(path, prefix + extension)