class Queue:
    '''
    Queue ini digunakan untuk menyimpan antrian paket.
    Digunakan karena queue memiliki sifat FIFO (First In First Out),
    sehingga item yang masuk pertama akan selalu berada di depan dan mudah diakses.
    '''
    def __init__(self) -> None:
        self.queue: list = []

    def enqueue(self, item) -> None:
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Queue is empty")

    def front(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            raise IndexError("Queue is empty")

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def size(self) -> int:
        return len(self.queue)
    
    def show_queue(self):
        print("\n=== ANTRIAN PACKET ===")
        for item in self.queue:
            print(item)