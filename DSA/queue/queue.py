class Queue:
    '''
    Queue ini digunakan untuk menyimpan antrian paket.
    Digunakan karena queue memiliki sifat FIFO (First In First Out),
    sehingga item yang masuk pertama akan selalu berada di depan dan mudah diakses.
    '''
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
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

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)