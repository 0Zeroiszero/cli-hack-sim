"""Module untuk struktur data Stack (LIFO)."""


class Stack:
    """Stack untuk menyimpan log histori.

    Digunakan karena stack memiliki sifat LIFO (Last In First Out),
    sehingga log terbaru akan selalu berada di atas dan mudah diakses.
    """

    def __init__(self) -> None:
        """Inisialisasi stack kosong."""
        self.stack: list = []

    def push(self, item) -> None:
        """Menambahkan item ke atas stack."""
        self.stack.append(item)

    def pop(self) -> object:
        """Menghapus dan mengembalikan item teratas dari stack."""
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("Stack is empty")

    def peek(self) -> object:
        """Mengembalikan item teratas tanpa menghapusnya."""
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("Stack is empty")

    def is_empty(self) -> bool:
        """Memeriksa apakah stack kosong."""
        return len(self.stack) == 0

    def size(self) -> int:
        """Mengembalikan jumlah item dalam stack."""
        return len(self.stack)

    def show_logs(self):
        """Menampilkan seluruh isi stack ke console."""
        print("\n=== HISTORI LOG (TERBARU -> LAMA) ===")
        for item in reversed(self.stack):
            print(item)
