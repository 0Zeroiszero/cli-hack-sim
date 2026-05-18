class Sorting:
    def __init__(self, traf):
        self.trafic = traf
    
    # fungsi untuk mengurutkan server berdasarkan traffic tertinggi menggunakan selection sort
    def sorting_server(self, arr):
        n = len(arr)
        
        for i in range(n):
            min_index = i
            for j in range(i+1, n):
                if arr[j] > arr[min_index]:
                    min_index = j
                    
            # tukar urutan yang salah
            arr[i], arr[min_index] = arr[min_index], arr[i]