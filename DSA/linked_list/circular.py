from .node import Node as CircularNode


class CircularLinkedList:
    """
    Circular Linked List:
    - node terakhir menunjuk kembali ke head
    - tidak memiliki NULL di akhir list
    - cocok untuk monitoring jaringan berulang
    - traversal menggunakan rekursif
    - tidak berisi search, sorting, file handler, dan fitur rubrik lain
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add_front(self, data):
        """
        Menambahkan node di bagian depan.
        """

        new_node = CircularNode(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            new_node.next = self.head
            self.head = new_node
            self.tail.next = self.head

        self.size += 1

    def add_back(self, data):
        """
        Menambahkan node di bagian belakang.
        Cocok untuk membuat urutan monitoring:
        Monitor 1 -> Monitor 2 -> Monitor 3 -> kembali ke Monitor 1
        """

        new_node = CircularNode(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head

        self.size += 1

    def remove_front(self):
        """
        Menghapus node paling depan.
        """

        if self.is_empty():
            return None

        removed_data = self.head.data

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head

        self.size -= 1
        return removed_data

    def remove_back(self):
        """
        Menghapus node paling belakang.
        """

        if self.is_empty():
            return None

        removed_data = self.tail.data

        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.size -= 1
            return removed_data

        current = self.head

        while current.next != self.tail:
            current = current.next

        self.tail = current
        self.tail.next = self.head
        self.size -= 1

        return removed_data

    def traverse_recursive(self):
        """
        Traversal rekursif untuk Circular Linked List.

        Karena Circular Linked List tidak punya NULL,
        traversal harus berhenti ketika jumlah node yang dikunjungi
        sudah sama dengan size.
        """

        result = []

        def visit(node, count):
            if count == self.size:
                return

            result.append(node.data)
            visit(node.next, count + 1)

        if not self.is_empty():
            visit(self.head, 0)

        return result

    def display_recursive(self):
        """
        Menampilkan Circular Linked List menggunakan rekursif.
        """

        def visit(node, count):
            if count == self.size:
                print("kembali ke HEAD")
                return

            print(node.data, end=" -> ")
            visit(node.next, count + 1)

        if self.is_empty():
            print("Kosong")
        else:
            visit(self.head, 0)

    def get_size(self):
        return self.size
