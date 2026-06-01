"""
@author: Irfan Kurniawan
"""
from pathlib import Path
from ipaddress import IPv4Address
    
# fungsi mencari server berdasarkan ip menggunakan binary search
def cari_server_binary(target:str):
    target = int(IPv4Address(target))
    data = []
    data_cari = []

    with open(Path('src/data/server.txt'), 'r') as f:
            for line in f:
                data.append(line.strip().split('|'))
    
    data_copy = data[:]
    
    for item in data_copy:
        bentuk_angka = int(IPv4Address(item[2]))
        item[2] = bentuk_angka
    
    data_copy.sort(key=lambda x: x[2])
    
    left = 0
    right = len(data_copy) - 1
    idx = 0
    ketemu = False
    
    while left <= right:
        mid = (left + right) // 2
        kembali_ip = str(IPv4Address(data_copy[mid][2]))
        
        if data_copy[mid][2] == target:
            ketemu = True
            data_cari.append(
                (
                    idx, 
                    kembali_ip, 
                    data_copy[mid][1], 
                    data_copy[mid][0], 
                    data_copy[mid][3], 
                    ketemu
                )
            )
            return data_cari
        
        if data_copy[mid][2] < target:
            left = mid + 1
        else:
            right = mid - 1
            
        data_cari.append(
            (
                idx, 
                kembali_ip, 
                data_copy[mid][1], 
                data_copy[mid][0], 
                data_copy[mid][3], 
                ketemu
            )
        )
        idx += 1
            
    return data_cari

# fungsi mencari server berdasarkan ip menggunakan linear search
def cari_server_linear(target:str):
    data = []
    data_cari = []
    ketemu = False
    
    with open(Path('src/data/server.txt'), 'r') as f:
            for line in f:
                data.append(line.strip().split('|'))
    
    for indeks, item in enumerate(data):
        if item[2] == target:
            ketemu = True
            data_cari.append(
                (indeks, item[2], item[1], item[0], item[3], ketemu)
            )
            break
        else:
            data_cari.append(
                (indeks, item[2], item[1], item[0], item[3], ketemu)
            )
    return data_cari
        

if __name__ == '__main__':
    # ss = SearchingServer()
    from pprint import pprint
    pprint(cari_server_binary('192.168.1.90'))
    pprint(cari_server_linear('192.168.1.40'))
