class SearchingServer:
    def __init__(self):
        pass
    
    # fungsi mencari server berdasarkan ip menggunakan binary search
    def cari_server(self, data, target):
        data.sort()
        left = 0
        right = len(data) - 1
        
        print('Searching IP...')
        
        while left <= right:
            mid = (left + right) // 2
            
            if data[mid].nama == target:
                print('FOUND:')
                print(f'Server : {data.nama}')
                print(f'IP : {data.ip}')
                return
            
            if data[mid].nama < target:
                left = mid + 1
            else:
                right = mid - 1
        
        print('IP Tidak Ditemukan!')