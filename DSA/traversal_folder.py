"""Modul traversal folder server menggunakan struktur data tree.

Menyediakan kelas TreeNode dan ServerTreeBuilder untuk membangun
pohon direktori server, serta fungsi traversal preorder, inorder,
dan postorder untuk menampilkan struktur folder dan file.

@author: Irfan Kurniawan
"""

import json
from pathlib import Path


class TreeNode:
    """Node pohon yang merepresentasikan folder atau file server.

    Attributes:
        name: Nama folder atau file.
        server_id: ID server (jika node adalah root server).
        node_type: Tipe node ("folder" atau "file").
        size: Ukuran file dalam bytes (None untuk folder).
        children: Daftar node anak.

    """

    def __init__(
        self, name: str, node_type: str = "folder", size: int | None = None
    ) -> None:
        """Inisialisasi node pohon.

        Args:
            name: Nama folder atau file.
            node_type: Tipe node, "folder" atau "file".
            size: Ukuran file dalam bytes (None untuk folder).

        """
        self.name: str = name
        self.server_id: str | None = None
        self.node_type: str = node_type
        self.size: int | None = size
        self.children: list[TreeNode] = []

    def add_child(self, child: TreeNode) -> None:
        """Menambahkan node anak ke dalam daftar children.

        Args:
            child: Node TreeNode yang akan ditambahkan sebagai anak.

        """
        self.children.append(child)

    def is_file(self) -> bool:
        """Memeriksa apakah node ini adalah file.

        Returns:
            True jika node_type adalah "file", False jika folder.

        """
        return self.node_type == "file"


class ServerTreeBuilder:
    """Membangun pohon direktori server dari file JSON.

    Membaca data folder dan file dari file JSON, lalu membangun
    struktur pohon TreeNode untuk setiap server.
    """

    @staticmethod
    def build_server_tree() -> list[TreeNode]:
        """Membangun daftar pohon server dari file JSON.

        Membaca file data/dalam-json/daftar_folder_file_server.json
        dan membangun struktur TreeNode untuk setiap server beserta
        folder dan file di dalamnya.

        Returns:
            list[TreeNode]: Daftar root node untuk setiap server.

        """
        file_path = Path("data/dalam-json/daftar_folder_file_server.json")

        with open(file_path) as file:
            data = json.load(file)

        servers = data.get("servers", [])
        servers_tree: list[TreeNode] = []

        for server in servers:
            root = TreeNode(f"{server['server_name']} ({server['server_id']})")

            folders = server.get("folders", {})

            for folder_name, folder_content in folders.items():
                folder_node = TreeNode(folder_name)

                for file_name, file_size in folder_content.items():
                    file_node = TreeNode(
                        file_name, node_type="file", size=file_size
                    )
                    folder_node.add_child(file_node)

                root.add_child(folder_node)

            servers_tree.append(root)

        return servers_tree


def preorder(node: TreeNode | None, depth: int = 0) -> str:
    """Traversal preorder: root -> children.

    Mengunjungi node terlebih dahulu, kemudian children secara rekursif.

    Args:
        node: Node TreeNode yang akan dikunjungi.
        depth: Kedalaman saat ini (untuk indentasi).

    Returns:
        str: Representasi tree dalam format preorder.

    """
    if node is None:
        return ""

    indent = "| " * depth

    if node.is_file():
        result = f"{indent}├── {node.name} ({node.size})\n"
    else:
        result = f"{indent}├── {node.name}\n"

    for child in node.children:
        result += preorder(child, depth + 1)

    return result


def inorder(node: TreeNode | None) -> str:
    """Traversal inorder: children kiri -> root -> children kanan.

    Membagi children menjadi dua bagian (kiri dan kanan),
    mengunjungi children kiri, root, lalu children kanan.

    Args:
        node: Node TreeNode yang akan dikunjungi.

    Returns:
        str: Representasi tree dalam format inorder.

    """
    if node is None:
        return ""

    result: list[str] = []

    mid = len(node.children) // 2

    for child in node.children[:mid]:
        child_result = inorder(child)
        if child_result:
            result.append(child_result)

    if node.is_file():
        result.append(f"{node.name} ({node.size})")
    else:
        result.append(node.name)

    for child in node.children[mid:]:
        child_result = inorder(child)
        if child_result:
            result.append(child_result)

    return " -> ".join(result)


def postorder(node: TreeNode | None) -> str:
    """Traversal postorder: children -> root.

    Mengunjungi children terlebih dahulu, kemudian root.

    Args:
        node: Node TreeNode yang akan dikunjungi.

    Returns:
        str: Representasi tree dalam format postorder.

    """
    if node is None:
        return ""

    result: list[str] = []

    for child in node.children:
        child_result = postorder(child)
        if child_result:
            result.append(child_result)

    if node.is_file():
        result.append(f"{node.name} ({node.size})")
    else:
        result.append(node.name)

    return " -> ".join(result)


if __name__ == "__main__":
    build = ServerTreeBuilder()
    servers = build.build_server_tree()

    for server in servers:
        print("preorder\n" + preorder(server) + "\n")
        print("inorder\n" + inorder(server) + "\n")
        print("postorder\n" + postorder(server) + "\n")
