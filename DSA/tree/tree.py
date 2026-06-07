# from importlib.resources import contents
# from pathlib import Path
# from platform import node
# from sys import prefix
#
#
# class TreeNode:
#     """Node untuk struktur data Tree (pohon).
#
#     Setiap node dapat memiliki banyak anak (children) yang membentuk
#     struktur hierarkis.
#
#     Attributes:
#         name: Nama dari node.
#         children: Daftar node anak.
#     """
#
#     def __init__(self, name: str) -> None:
#         """Inisialisasi node tree dengan nama.
#
#         Args:
#             name: Nama dari node.
#         """
#         self.name = name
#         self.children: list = []
#
#     def add_child(self, child_node: "TreeNode") -> None:
#         """Menambahkan node anak ke node saat ini.
#
#         Args:
#             child_node: Node TreeNode yang akan ditambahkan sebagai anak.
#         """
#         self.children.append(child_node)
#
#     def cetak_tree(self, node: "TreeNode", prefix: str = "") -> None:
#         """Mencetak struktur tree secara visual.
#
#         Args:
#             node: Node yang akan dicetak.
#             prefix: Prefix string untuk indentasi.
#         """
#         # Mencetak node saat ini
#         print(f"{prefix}|-- {node.name}")
#
#         # Rekursi untuk setiap anak
#         for i, child in enumerate(node.children):
#             is_last = i == len(node.children) - 1
#             extension = "    " if is_last else "\u2502   "
#             self.cetak_tree(child, prefix + extension)
#
#     def preorder_traversal(self, node: "TreeNode") -> None:
#         """Melakukan preorder traversal pada tree.
#
#         Urutan: root, left, right.
#
#         Args:
#             node: Node yang akan dikunjungi.
#         """
#         if node is not None:
#             print(node.name, end=" ")  # Proses node saat ini
#             for child in node.children:
#                 self.preorder_traversal(child)  # Rekursi untuk anak-anaknya
#
#     def postorder_traversal(self, node: "TreeNode") -> None:
#         """Melakukan postorder traversal pada tree.
#
#         Urutan: left, right, root.
#
#         Args:
#             node: Node yang akan dikunjungi.
#         """
#         if node is not None:
#             for child in node.children:
#                 self.postorder_traversal(child)  # Rekursi untuk anak-anaknya
#             print(node.name, end=" ")  # Proses node saat ini
#
#     def inorder_traversal(self, node: "TreeNode") -> None:
#         """Melakukan inorder traversal pada tree.
#
#         Urutan: left, root, right (khusus tree biner).
#
#         Args:
#             node: Node yang akan dikunjungi.
#         """
#         if node is not None:
#             if len(node.children) > 0:
#                 self.inorder_traversal(
#                     node.children[0]
#                 )  # Rekursi untuk anak pertama
#             print(node.name, end=" ")  # Proses node saat ini
#             for child in node.children[1:]:
#                 self.inorder_traversal(child)  # Rekursi untuk anak-anak berikutnya
