"""Module untuk struktur data Queue (FIFO).

@author: Alif Akbar
"""


class Queue:
    """Queue untuk menyimpan antrian paket.

    Digunakan karena queue memiliki sifat FIFO (First In First Out),
    sehingga item yang masuk pertama akan selalu berada di depan
    dan mudah diakses.

    Attributes:
        queue: List internal untuk menyimpan item dalam antrian.
    """

    def __init__(self) -> None:
        """Inisialisasi queue kosong."""
        self.queue: list = []

    def enqueue(self, item: object) -> None:
        """Menambahkan item ke akhir queue.

        Args:
            item: Item yang akan ditambahkan ke antrian.
        """
        self.queue.append(item)

    def dequeue(self) -> object:
        """Menghapus dan mengembalikan item dari depan queue.

        Returns:
            Item dari depan queue.

        Raises:
            IndexError: Jika queue kosong.
        """
        if not self.is_empty():
            return self.queue.pop(0)
        raise IndexError("Queue is empty")

    def front(self) -> object:
        """Mengembalikan item terdepan tanpa menghapusnya.

        Returns:
            Item terdepan dari queue.

        Raises:
            IndexError: Jika queue kosong.
        """
        if not self.is_empty():
            return self.queue[0]
        raise IndexError("Queue is empty")

    def is_empty(self) -> bool:
        """Memeriksa apakah queue kosong.

        Returns:
            True jika queue kosong, False jika tidak.
        """
        return len(self.queue) == 0

    def size(self) -> int:
        """Mengembalikan jumlah item dalam queue.

        Returns:
            Jumlah item dalam queue.
        """
        return len(self.queue)
<<<<<<< HEAD
=======

    # def show_queue(self) -> None:
    #     """Menampilkan seluruh isi queue ke console."""
    #     print("\n=== ANTRIAN PACKET ===")
    #     for item in self.queue:
    #         print(item)
>>>>>>> main
