"""Module untuk struktur data Stack (LIFO).

@author: Alif Akbar
"""


class Stack:
    """Stack untuk menyimpan log histori.

    Digunakan karena stack memiliki sifat LIFO (Last In First Out),
    sehingga log terbaru akan selalu berada di atas dan mudah diakses.

    Attributes:
        stack: List internal untuk menyimpan item dalam stack.
    """

    def __init__(self) -> None:
        """Inisialisasi stack kosong."""
        self.stack: list = []

    def push(self, item: object) -> None:
        """Menambahkan item ke atas stack.

        Args:
            item: Item yang akan ditambahkan ke stack.
        """
        self.stack.append(item)

    def pop(self) -> object:
        """Menghapus dan mengembalikan item teratas dari stack.

        Returns:
            Item teratas dari stack.

        Raises:
            IndexError: Jika stack kosong.
        """
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("Stack is empty")

    def peek(self) -> object:
        """Mengembalikan item teratas tanpa menghapusnya.

        Returns:
            Item teratas dari stack.

        Raises:
            IndexError: Jika stack kosong.
        """
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("Stack is empty")

    def is_empty(self) -> bool:
        """Memeriksa apakah stack kosong.

        Returns:
            True jika stack kosong, False jika tidak.
        """
        return len(self.stack) == 0

    def size(self) -> int:
        """Mengembalikan jumlah item dalam stack.

        Returns:
            Jumlah item dalam stack.
        """
        return len(self.stack)

    # def show_logs(self) -> None:
    #     """Menampilkan seluruh isi stack ke console."""
    #     print("\n=== HISTORI LOG (TERBARU -> LAMA) ===")
    #     for item in reversed(self.stack):
    #         print(item)
