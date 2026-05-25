import random

server_list = []
ip_unik = set()
koordinat_server = {}
network = {}

class Server:
    def __init__(self, nama, ip, status='ACTIVE', traffic=0):
        self.nama = nama
        self.ip = ip
        self.status = status
        self.traffic = traffic

# fungsi menambahkan server
def tambah_server():
    nama = input('Nama Server: ')
    ip = input('IP Server: ')
    
    if ip in ip_unik:
        print('IP sudah digunakan')
        return
    
    ip_unik.add(ip)
    
    posisi = (
        (random.randint(1,100)), (random.randint(1,100)) 
    )
    
    koordinat_server[nama] = posisi
    network[nama] = []
    
    server = Server(nama, ip)
    server_list.append(server)
    
    print('Server Berhasil Dibuat!')