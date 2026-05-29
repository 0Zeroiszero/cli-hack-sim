from server import *
from login import *

class FileHandler:
    def __init__(self):
        pass
    
    # fungsi untuk menyimpan data server ke dalam file txt
    def save_server(self):
        with open('data/server.txt', 'w') as f:
            for i in server_list:
                data = f'{i.nama}|{i.id}|{i.ip}|{i.status}\n'
                f.write(data)

    # fungsi untuk mengambil data dari file txt
    def load_server(self):
        try:
            server_list.clear()
            
            with open('data/server.txt', 'r') as f:
                for baris in f:
                    data = baris.strip().split('|') # ini untuk mengubah text menjadi sebuah data dalam list
                    nama = data[0]
                    id = data[1]
                    ip = data[2]
                    status = data[3]
                    
                    obj = Server(nama, id, ip, status) # data kembali menjadi objek 
                    server_list.append(obj)
        except:
            print('File Tidak Ditemukan')

    # fungsi untuk menyimpan data akun ke dalam file json
    def save_akun(self):
        with open('data/dalam-json/akun.json', 'w') as f:
            json.dump(servers, f, indent=4)

    # fungsi untuk mengambil data dari file json
    def load_akun(self):
        try:
            servers.clear()
            with open('data/dalam-json/akun.json', 'r') as f:
                data = json.load(f)
                servers.update(data)
        except:
            print('File Tidak Ditemukan')

    # fungsi untuk menyimpan log stack
    def save_log(self, log_stack):
        with open('data/log.txt', 'w') as f:
            for log in log_stack:
                f.write(log + '\n')

    # fungsi untuk mengambil data dari file log.txt
    def load_log(self, log_stack):
        try:
            log_stack.clear()
            
            with open('data/log.txt', 'r') as f:
                for baris in f:
                    log_stack.append(baris.strip())
        except:
            print('File Tidak Ditemukan')

    # fungsi untuk menyimpan data packet
    def save_packet(self, packet_queue):
        with open('data/packet.txt', 'w') as f:
            for packet in packet_queue:
                f.write(packet + '\n')

    # fungsi untuk mengambil data dari file packet.txt
    def load_packet(self, packet_queue):
        try:
            packet_queue.clear()
            
            with open('data/packet.txt', 'r') as f:
                for baris in f:
                    packet_queue.append(baris.strip())
        except:
            print('File Tidak Ditemukan')

    def save_all(self):
        self.save_server()
        self.save_akun()
        # self.save_log()
        # self.save_packet()
        
        print('[ALL DATA SAVED]')

    def load_all(self):
        self.load_server()
        self.load_akun()
        # self.load_log()
        # self.load_packet()
        
        print('[ALL DATA LOADED]')

if __name__ == '__main__':
    fh = FileHandler()
    fh.save_all()
    fh.load_all()