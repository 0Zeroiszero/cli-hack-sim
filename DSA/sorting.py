class SortingServer:
    def __init__(self):
        pass
    
    # fungsi untuk mengurutkan server berdasarkan traffic tertinggi menggunakan selection sort
    def urutkan_server(self, server):
        n = len(server)
        
        for i in range(n):
            min_index = i
            for j in range(i+1, n):
                if server[j].traffic > server[min_index].traffic:
                    min_index = j
            
            # tukar urutan yang salah
            server[i], server[min_index] = server[min_index], server[i]
        
        print('=== SERVER RANKING ===')
        for i in range(n):
            print(f'{i+1}. {server[i].nama} - {server[i].traffic} MB/s')