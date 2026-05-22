from .node import DoubleNode


class DoubleLinkedList:
    """
    Double Linked List:
    - setiap node bisa bergerak maju dengan next
    - setiap node bisa bergerak mundur dengan prev
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

        new_node = DoubleNode(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def add_back(self, data):
        """
        Menambahkan node di bagian belakang.
        Cocok untuk membuat urutan navigasi server:
        Server A <-> Server B <-> Server C
        """

        new_node = DoubleNode(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

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
            self.head.prev = None

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
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        return removed_data

    def traverse_forward_recursive(self):
        """
        Traversal rekursif dari depan ke belakang.
        Arah: head -> tail
        """

        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.data)
            visit(node.next)

        visit(self.head)
        return result

    def traverse_backward_recursive(self):
        """
        Traversal rekursif dari belakang ke depan.
        Arah: tail -> head
        """

        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.data)
            visit(node.prev)

        visit(self.tail)
        return result

    def display_forward_recursive(self):
        """
        Menampilkan isi Double Linked List dari depan ke belakang.
        """

        def visit(node):
            if node is None:
                print("NULL")
                return

            print(node.data, end=" <-> ")
            visit(node.next)

        visit(self.head)

    def display_backward_recursive(self):
        """
        Menampilkan isi Double Linked List dari belakang ke depan.
        """

        def visit(node):
            if node is None:
                print("NULL")
                return

            print(node.data, end=" <-> ")
            visit(node.prev)

        visit(self.tail)

    def get_size(self):
        return self.size
