import random
import json

class ServerNode:
    def __init__(self, nama, id, ip, status):
        self.id = id
        self.nama = nama
        self.ip = ip
        self.status = status

# fungsi menambahkan server
class FungsiServer:
    def __init__(self):
        self.server_list = []
        self.ip_unik = set()
        self.koordinat_server = {}
        self.network = {}
    
    def tambah_server(self):
        with open('data/dalam-json/akun.json', 'r') as f:
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
        
        print('Server Berhasil Dibuat!')
    
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

if __name__ == '__main__':
    fs = FungsiServer()
    fs.tambah_server()
    fs.tampilkan_server(data=fs.server_list)