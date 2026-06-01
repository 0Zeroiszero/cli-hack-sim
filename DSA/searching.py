"""
@author: Irfan Kurniawan
"""
from pathlib import Path
from ipaddress import IPv4Address

class SearchingServer:
    def __init__(self):
        self.data = []
        self.data_cari = []
        self.ketemu = False
        
        with open(Path('src/data/server.txt'), 'r') as f:
            for line in f:
                self.data.append(line.strip().split('|'))
    
    # fungsi mencari server berdasarkan ip menggunakan binary search
    def cari_server_binary(self, target):
        for item in self.data:
            bentuk_angka = int(IPv4Address(item[2]))
            item[2] = bentuk_angka
        
        self.data.sort(key=lambda x: x[2])
        
        left = 0
        right = len(self.data) - 1
        idx = 0
        
        while left <= right:
            mid = (left + right) // 2
            kembali_ip = str(IPv4Address(self.data[mid][2]))
            
            if self.data[mid][2] == target:
                self.ketemu = True
                self.data_cari.append(
                    (
                        idx, 
                        kembali_ip, 
                        self.data[mid][1], 
                        self.data[mid][0], 
                        self.data[mid][3], 
                        self.ketemu
                    )
                )
                return self.data_cari
            
            if self.data[mid][2] < target:
                left = mid + 1
            else:
                right = mid - 1
                
            self.data_cari.append(
                (
                    idx, 
                    kembali_ip, 
                    self.data[mid][1], 
                    self.data[mid][0], 
                    self.data[mid][3], 
                    self.ketemu
                )
            )
            idx += 1
                
        return self.data_cari
    
    # fungsi mencari server berdasarkan ip menggunakan linear search
    def cari_server_linear(self, target):
        for indeks, item in enumerate(self.data):
            if item[2] == target:
                self.ketemu = True
                self.data_cari.append(
                   (indeks, item[2], item[1], item[0], item[3], self.ketemu)
                )
                break
            else:
                self.data_cari.append(
                   (indeks, item[2], item[1], item[0], item[3], self.ketemu)
                )
        return self.data_cari
        

if __name__ == '__main__':
    ss = SearchingServer()
    bentuk_angka = int(IPv4Address("192.168.1.30"))
    b = ss.cari_server_binary(bentuk_angka)
    # l = ss.cari_server_linear("192.168.1.60")