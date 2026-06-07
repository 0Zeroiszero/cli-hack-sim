"""
@author: Irfan Kurniawan
@modified: 02/06/2026 oleh Abdullah Affandi
- kontrak abstraksi untuk traversal pada binary search tree
- preorder, inorder, postorder
- kalau mau buat traversal lain, buat method baru dengan abstraksi yang sama
@modified: 02/06/2026 oleh Abdullah Affandi
- Menghilangkan kontrak abstraksi
"""

from pathlib import Path
import json

class TreeNode():
    def  __init__(self, name, node_type="folder", size: int = None):
        self.name = name
        self.server_id = None
        self.node_type = node_type
        self.size = size
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def is_file(self):
        return self.node_type == "file"

class ServerTreeBuilder:

    # ServerTreeBuilder.build_server_tree()
    @staticmethod
    def build_server_tree() -> list[TreeNode]:
        file_path = Path("data/dalam-json/daftar_folder_file_server.json")
        
        with open(file_path, "r") as file:
            data = json.load(file)
        
        servers = data.get("servers", [])
        servers_tree = []
        
        for server in servers:
            root = TreeNode(
                f"{server["server_name"]} ({server["server_id"]})"
            )
            
            folders = server.get("folders", {})
            
            for folder_name, folder_content in folders.items():
                folder_node = TreeNode(folder_name)
                
                # isi file di folder
                for file_name, file_size in folder_content.items():
                    file_node = TreeNode(
                        file_name,
                        node_type="file",
                        size=file_size
                    )
                    
                    folder_node.add_child(file_node)
                    
                root.add_child(folder_node)
            
            servers_tree.append(root)
        
        return servers_tree

# PREORDER
# root -> children
def preorder(node, depth=0) -> str:
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

# INORDER
# children kiri -> root -> kanan
def inorder(node) -> str:
    if node is None:
        return ""
    
    result = []
    
    mid = len(node.children) // 2
    
    # kiri
    for child in node.children[:mid]:
        child_result = inorder(child)
        
        if child_result:
            result.append(child_result)
    
    # root
    if node.is_file():
        result.append(f"{node.name} ({node.size})")
    else:
        result.append(node.name)
    
    # kanan
    for child in node.children[mid:]:
        child_result = inorder(child)
        
        if child_result:
            result.append(child_result)
    
    return " -> ".join(result)

# POSTORDER
# children -> root
def postorder(node) -> str:
    if node is None:
        return ""
    
    result = []
    
    for child in node.children:
        child_result = postorder(child)
        
        if child_result:
            result.append(child_result)
    
    # root
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