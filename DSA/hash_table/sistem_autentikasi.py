'''
Referensi ke DSA\hash_table
'''

from pathlib import Path

from rich import json

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import heapq

from DSA import hash_table

class AuthenticationSystem(hash_table):
    def __init__(self, size=10):
        super().__init__(size)
        self.console = Console()

    def tampilkan_akun_dan_status_server(self):
        akun_dan_status_server_path = Path("src/data/dalam-json/akun_dan_status_server.json")
        if not akun_dan_status_server_path.exists():
            self.console.print(Text("File akun_dan_status_server.json tidak ditemukan.", style="bold red"))
            return
        
        with open(akun_dan_status_server_path, "r") as file:
            akun_dan_status_server = json.load(file)
        
        if not akun_dan_status_server.get("servers"):
            self.console.print(Text("Tidak ada data server yang tersedia.", style="bold red"))
            return
        
        table_text = Text(style="bold blue")
        table_panel = Panel(table_text, title="AKUN DAN STATUS SERVER", style="bold blue")

        for item in akun_dan_status_server.get("servers", []):
            server_id = item.get("server_id", "N/A")
            server_name = item.get("server_name", "N/A")
            username = item.get("username", "N/A")
            password = item.get("password", "N/A")
            status = item.get("status", "N/A")
            table_text.append(f"Server ID: {server_id}\n")
            table_text.append(f"Server Name: {server_name}\n")
            table_text.append(f"Username: {username}\n")
            table_text.append(f"Password: {password}\n")
            table_text.append(f"Status: {status}\n\n")
        
        self.console.print(table_panel)
    
    def brute_force_attack(self):
        akun_dan_status_server_path = Path("src/data/dalam-json/akun_dan_status_server.json")
        brute_force = Path("src/data/dalam-json/bruteforce.json")
        return_dict = []

        with open(akun_dan_status_server_path, "r") as file:
            akun_dan_status_server = json.load(file)
        
        for idx, item in enumerate(akun_dan_status_server.get("servers", [])):
            server_id = item.get("server_id")
            server_name = item.get("server_name")
            username = item.get("username")
            password = item.get("password")
            status = item.get("status")
            info = (idx, server_id, server_name, username, password, status, False)
            return_dict.append(info)
        
        for username, password in brute_force.read_text_file():
            username = username.strip()
            password = password.strip()

        for item in return_dict:
            if item[3] == username and item[4] == password:
                return_dict[return_dict.index(item)] = (*item[:-1], True)
                break
            

        return return_dict