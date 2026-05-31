import json

class SortingServer:
    def __init__(self):
        self.urutan = []
        self.urutan_data = []
    
    # fungsi untuk mengurutkan server berdasarkan bandwidth tertinggi menggunakan bubble sort
    def urutkan_server(self):
        with open('data/dalam-json/akun_dan_status_server.json', 'r') as f:
            data = json.load(f)
        
        idx = 0
        for req in data['servers']:
            self.urutan.append([idx, req['server_id'], req['server_name'], req['bandwidth_mbps']])
            idx += 1
        
        n = len(self.urutan)
        
        for i in range(n-1):
            swap = False
            for j in range(n-i-1):
                if self.urutan[j][3] < self.urutan[j+1][3]:
                    self.urutan[j], self.urutan[j+1] = self.urutan[j+1], self.urutan[j]
                    self.urutan[j][0], self.urutan[j+1][0] = self.urutan[j+1][0], self.urutan[j][0]
                    swap = True
            if not swap:
                break
        
        for i in self.urutan:
            self.urutan_data.append(tuple(i))
        
        return self.urutan_data

if __name__ == '__main__':
    ss = SortingServer()
    ss.urutkan_server()