"""Module untuk struktur data Queue (FIFO)."""


class Queue:
    """Queue untuk menyimpan antrian paket.

    Digunakan karena queue memiliki sifat FIFO (First In First Out),
    sehingga item yang masuk pertama akan selalu berada di depan
    dan mudah diakses.
    """

    def __init__(self) -> None:
        """Inisialisasi queue kosong."""
        self.queue: list = []

    def enqueue(self, item) -> None:
        """Menambahkan item ke akhir queue."""
        self.queue.append(item)

    def dequeue(self):
        """Menghapus dan mengembalikan item dari depan queue."""
        if not self.is_empty():
            return self.queue.pop(0)
        raise IndexError("Queue is empty")

    def front(self):
        """Mengembalikan item terdepan tanpa menghapusnya."""
        if not self.is_empty():
            return self.queue[0]
        raise IndexError("Queue is empty")

    def is_empty(self) -> bool:
        """Memeriksa apakah queue kosong."""
        return len(self.queue) == 0

    def size(self) -> int:
        """Mengembalikan jumlah item dalam queue."""
        return len(self.queue)

    def show_queue(self):
        """Menampilkan seluruh isi queue ke console."""
        print("\n=== ANTRIAN PACKET ===")
        for item in self.queue:
            print(item)
