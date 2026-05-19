from server import *
from login import *

# fungsi untuk menyimpan data server ke dalam file txt
def save_server():
    with open('data/server.txt', 'w') as f:
        for i in server_list:
            data = f'{i.nama},{i.ip},{i.status},{i.traffic}\n'
            f.write(data)

# fungsi untuk mengambil data dari file txt
def load_server():
    try:
        server_list.clear()
        
        with open('data/server.txt', 'r') as f:
            for baris in f:
                data = baris.strip().split(',') # ini untuk mengubah text menjadi sebuah data dalam list
                nama = data[0]
                ip = data[1]
                status =[2]
                traffic = data[3]
                
                obj = Server(nama, ip, status, traffic) # data kembali menjadi objek 
                server_list.append(obj)
    except:
        print('File Tidak Ditemukan')

# fungsi untuk menyimpan data akun ke dalam file txt
def save_akun():
    with open('data/akun.txt', 'w') as f:
        for username in akun:
            password = akun[username]
            f.write(f'{username},{password}\n')

# fungsi untuk mengambil data dari file txt
def load_akun():
    try:
        with open('data/akun.txt', 'r') as f:
            for baris in f:
                data = baris.strip().split(',')
                username = data[0]
                password = data[1]
                akun[username] = password
    except:
        print('File Tidak Ditemukan')

def save_log():
    pass

def load_log():
    pass

def save_packet():
    pass

def load_packet():
    pass

def save_all():
    save_server()
    save_akun()
    save_log()
    save_packet()
    
    print('[ALL DATA SAVED]')

def load_all():
    load_server()
    load_akun()
    load_log()
    load_packet()
    
    print('[ALL DATA LOADED]')