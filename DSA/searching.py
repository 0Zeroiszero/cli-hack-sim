class SearchingServer:
    def __init__(self):
        pass
    
    # fungsi mencari server berdasarkan ip menggunakan binary search
    def cari_server(self, data, target):
        print('Searching IP...')
        left = 0
        right = len(data) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if data[mid] == target:
                print('FOUND:')
                print(f'Server : {data.nama}')
                print(f'IP : {data.ip}')
            
            if data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        print('IP Tidak Ditemukan!')