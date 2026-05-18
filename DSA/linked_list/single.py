from .node import Node


class SingleLinkedList:
    """
    Single Linked List murni:
    - hanya fokus ke node dan pointer next
    - traversal menggunakan rekursif
    - tidak mengambil fitur search, sorting, file handler, dll
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add_front(self, data):
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self.size += 1

    def add_back(self, data):
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def remove_front(self):
        if self.is_empty():
            return None

        removed_data = self.head.data
        self.head = self.head.next
        self.size -= 1

        if self.head is None:
            self.tail = None

        return removed_data

    def remove_back(self):
        if self.is_empty():
            return None

        if self.head == self.tail:
            removed_data = self.head.data
            self.head = None
            self.tail = None
            self.size -= 1
            return removed_data

        current = self.head

        while current.next != self.tail:
            current = current.next

        removed_data = self.tail.data
        current.next = None
        self.tail = current
        self.size -= 1

        return removed_data

    def traverse_recursive(self):
        """
        Traversal rekursif.
        Fungsi ini mengubah linked list menjadi list biasa
        agar mudah ditampilkan atau dites.
        """
        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.data)
            visit(node.next)

        visit(self.head)
        return result

    def display_recursive(self):
        """
        Menampilkan linked list menggunakan rekursif.
        """

        def visit(node):
            if node is None:
                print("NULL")
                return

            print(node.data, end=" -> ")
            visit(node.next)

        visit(self.head)

    def get_size(self):
        return self.size
