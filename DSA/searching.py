"""
@author: Irfan Kurniawan
"""
from pathlib import Path

class SearchingServer:
    def __init__(self):
        self.data = []
        self.data_cari = []
    
    # fungsi mencari server berdasarkan ip menggunakan binary search
    def cari_server(self, target):
        with open(Path('src/data/server.txt'), 'r') as f:
            for line in f:
                self.data.append(line.strip().split('|'))
        
        self.data.sort()
        left = 0
        right = len(self.data) - 1
        ketemu = False
        idx = 0
        
        while left <= right:
            mid = (left + right) // 2
            
            if self.data[mid][2] == target:
                ketemu = True
                self.data_cari.append((idx, self.data[mid][2], self.data[mid][1], self.data[mid][0], self.data[mid][3], ketemu))
                return self.data_cari
            
            if self.data[mid][2] < target:
                left = mid + 1
                self.data_cari.append((idx, self.data[mid][2], self.data[mid][1], self.data[mid][0], self.data[mid][3], ketemu))
                idx += 1
            else:
                right = mid - 1
                self.data_cari.append((idx, self.data[mid][2], self.data[mid][1], self.data[mid][0], self.data[mid][3], ketemu))
                idx += 1
                
        return self.data_cari
        

if __name__ == '__main__':
    ss = SearchingServer()