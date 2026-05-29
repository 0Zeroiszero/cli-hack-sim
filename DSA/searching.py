from server import server_list

class SearchingServer:
    def __init__(self):
        pass
    
    # fungsi mencari server berdasarkan ip menggunakan binary search
    def cari_server(self, target):
        data = []
        for i in server_list:
            data.append([i.nama, i.id, i.ip, i.status])
        
        data.sort()
        left = 0
        right = len(data) - 1
        
        print('Searching IP...\n')
        
        while left <= right:
            mid = (left + right) // 2
            
            if data[mid][2] == target:
                print('FOUND:')
                print(f'Server_Name : {data[mid][0]}')
                print(f'Server_Id   : {data[mid][1]}')
                print(f'IP          : {data[mid][2]}')
                print(f'Status      : {data[mid][3]}')
                return
            
            if data[mid][2] < target:
                left = mid + 1
            else:
                right = mid - 1
        else:
            print('IP Tidak Ditemukan!')

if __name__ == '__main__':
    ss = SearchingServer()
    ss.cari_server()