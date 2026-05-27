import random, json

server_list = []
ip_unik = set()
koordinat_server = {}
network = {}

class Server:
    def __init__(self, id, nama, ip, status):
        self.id = id
        self.nama = nama
        self.ip = ip
        self.status = status

# fungsi menambahkan server
def tambah_server():
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
        
        if ip_server[i] in ip_unik:
            print('IP sudah digunakan')
            return
        
        ip_unik.add(ip_server[i])
        
        posisi = (
            (random.randint(1,100)), (random.randint(1,100)) 
        )
        
        koordinat_server[nama_server[i]] = posisi
        network[nama_server[i]] = []
        
        server = Server(nama, id, ip, status)
        server_list.append(server)
    
    print('Server Berhasil Dibuat!')

def tampilkan_server():
    print("+========================================+")
    print("|             SEVER MONITOR              |")
    print("+========================================+")
    for i in server_list:
        print(f" Server ID         : {i.nama}")
        print(f" Server Name       : {i.id}")
        print(f" IP Address        : {i.ip}")
        print(f" Status            : {i.status}\n")
    print("+========================================+")