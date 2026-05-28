import json

class SortingServer:
    def __init__(self):
        pass
    
    # fungsi untuk mengurutkan server berdasarkan traffic tertinggi menggunakan selection sort
    def urutkan_server(self):
        traffic = []
        
        with open('data/dalam-json/traffic.json', 'r') as f:
            data = json.load(f)
        
        for server in data:
            for monitor in data[server]:
                for req in data[server][monitor]:
                    latency = int(req['latency'].replace(' ms', ''))
                    traffic.append([req['destination'], latency])
        
        n = len(traffic)
        
        for i in range(n):
            min_index = i
            for j in range(i+1, n):
                if traffic[j][1] > traffic[min_index][1]:
                    min_index = j
            
            # tukar urutan yang salah
            traffic[i], traffic[min_index] = traffic[min_index], traffic[i]
        
        print('\n======= SERVER RANKING =======\n')
        for i in range(n):
            print(f'{i+1}. {traffic[i][0]} - {traffic[i][1]} MB/s')

if __name__ == '__main__':
    ss = SortingServer()
    ss.urutkan_server()