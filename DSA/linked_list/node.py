# TODO: Harus dihapus


# class Node:
#     """Node dasar untuk Linked List.
#
#     Sengaja dibuat sederhana agar bisa dipakai ulang untuk:
#     - Single Linked List  : memakai next
#     - Double Linked List  : nanti bisa ditambah prev
#     - Circular Linked List: next node terakhir mengarah ke head
#
#     Attributes:
#         data: Data yang disimpan dalam node.
#         next: Pointer ke node berikutnya.
#     """
#
#     def __init__(self, data: object) -> None:
#         """Inisialisasi node dengan data.
#
#         Args:
#             data: Data yang akan disimpan dalam node.
#         """
#         self.data = data
#         self.next = None
#
#
# class DoubleNode:
#     """Node untuk Double Linked List.
#
#     Setiap node menyimpan:
#     1. data
#     2. prev
#     3. next
#
#     Attributes:
#         data: Data yang disimpan dalam node.
#         prev: Pointer ke node sebelumnya.
#         next: Pointer ke node berikutnya.
#     """
#
#     def __init__(self, data: object) -> None:
#         """Inisialisasi node dengan data.
#
#         Args:
#             data: Data yang akan disimpan dalam node.
#         """
#         self.data = data
#         self.prev = None
#         self.next = None
