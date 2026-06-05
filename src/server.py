"""
@author: Irfan Kurniawan
@modified: 02/06/2026 21.40 WIB oleh Abdullah Affandi
- Mengganti path lokasi akun_dan_status_server.json pada fungsi tambah_server
- Menghilangkan print pada fungsi tambah_server karena sudah tidak diperlukan
"""

from pathlib import Path
import random
import json

class ServerNode:
    # Di-return oleh FungsiServer.tambah_server() untuk setiap server yang dibuat
    def __init__(self, nama: str, id: str, ip: str, status: str) -> None:
        self.id: str = id
        self.nama: str = nama
        self.ip: str = ip
        self.status: str = status

# fungsi menambahkan server
class FungsiServer:
    def __init__(self):
        self.server_list = []
        self.ip_unik = set()
        self.koordinat_server = {}
        self.network = {}
    
    def tambah_server(self):
        with open("src/data/dalam-json/akun_dan_status_server.json", "r") as f:
            data = json.load(f)
        
        nama_server = [item['server_name'] for item in data['servers']]
        server_id = [item['server_id'] for item in data['servers']]
        ip_server = [item['ip'] for item in data['servers']]
        status_server = [item['status'] for item in data['servers']]
        
        for i in range(len(nama_server)):
            nama = nama_server[i]
            id = server_id[i]
            ip = ip_server[i]
            status = status_server[i]
            
            if ip_server[i] in self.ip_unik:
                print('IP sudah digunakan')
                return
            
            self.ip_unik.add(ip_server[i])
            
            posisi = (
                (random.randint(1,100)), (random.randint(1,100)) 
            )
            
            self.koordinat_server[nama_server[i]] = posisi
            self.network[nama_server[i]] = []
            
            server = ServerNode(nama, id, ip, status)
            self.server_list.append(server)
    
    def tampilkan_server(self, data):
        print("\n+========================================+")
        print("|             SERVER MONITOR             |")
        print("+========================================+")
        for i in data:
            print(f" Server ID         : {i.nama}")
            print(f" Server Name       : {i.id}")
            print(f" IP Address        : {i.ip}")
            print(f" Status            : {i.status}\n")
        print("+========================================+")

def cek_access_server():
    file_path = Path("src/data/dalam-json/akun_dan_status_server.json")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    hasil = {
        "rows": [],
        "summary": {
            "total_server": 0,
            "unlocked_access": 0,
            "locked_access": 0,
            "visible_credential": 0,
        }
    }
    
    for indeks, req in enumerate(data['servers']):
        access = req["access"]
        credential = req["credential"]
        
        if access == "UNLOCKED":
            username = credential["username"]
            password = credential["password"]
            is_unlocked = True
            
            hasil["summary"]["unlocked_access"] += 1
            hasil["summary"]["visible_credential"] += 1
        else:
            username = "********"
            password = "********"
            is_unlocked = False
            
            hasil["summary"]["locked_access"] += 1
            
        row = {
            "indeks": indeks,
            "server_id": req["server_id"],
            "server_name": req["server_name"],
            "access": access,
            "username": username,
            "password": password,
            "is_unlocked": is_unlocked,
        }
        
        hasil["rows"].append(row)
        hasil["summary"]["total_server"] = len(data["servers"])
        
    return hasil

def get_server_detail(server_id: str) -> dict:
    file_path = Path("src/data/dalam-json/akun_dan_status_server.json")
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    for req in data["servers"]:
        if server_id == req["server_id"]:
            if req["access"] == "UNLOCKED":
                hasil = {
                    "server_id": req["server_id"],
                    "server_name": req["server_name"],
                    "ip": req["ip"],
                    "bandwidth_mbps": req["bandwidth_mbps"],
                    "status": req["status"],
                    "access": req['access'],
                    "vulnerable": req["vulnerable"],
                    "credential": {
                        "username": req["credential"]['username'],
                        "password": req["credential"]['password'],
                        "is_visible": True
                    },
                    "security_note": (
                        "Credential dapat ditampilkan karena access server sudah UNLOCKED. "
                    )
                }
                return hasil
            else:
                hasil = {
                    "server_id": req["server_id"],
                    "server_name": req["server_name"],
                    "ip": req["ip"],
                    "bandwidth_mbps": req["bandwidth_mbps"],
                    "status": req["status"],
                    "access": req['access'],
                    "vulnerable": req["vulnerable"],
                    "credential": {
                        "username": "*******",
                        "password": "*******",
                        "is_visible": False
                    },
                    "security_note": (
                        "Credential disembunyikan karena access LOCKED. "
                        "Gunakan fitur login/unlock untuk membuka akses. "
                    )
                }
                return hasil
    return {
        "error": True,
        "message": f"Server dengan ID '{server_id}' tidak ditemukan. "
    }

if __name__ == '__main__':
    fs = FungsiServer()
    # fs.tambah_server()
    # fs.tampilkan_server(data=fs.server_list)
    from pprint import pprint
    pprint(get_server_detail("SRV002"))
