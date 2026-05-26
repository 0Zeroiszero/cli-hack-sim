# TODO: Harus dihapus


class Node:
    """
    Node dasar untuk Linked List.
    Sengaja dibuat sederhana agar bisa dipakai ulang untuk:
    - Single Linked List  : memakai next
    - Double Linked List  : nanti bisa ditambah prev
    - Circular Linked List: next node terakhir mengarah ke head
    """

    def __init__(self, data):
        self.data = data
        self.next = None


class DoubleNode:
    """
    Node untuk Double Linked List.
    Setiap node menyimpan:
    1. data
    2. prev
    3. next
    """

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
