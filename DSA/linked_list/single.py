"""
@author: Abdullah Affandi
Implementasi Single Linked List untuk Queue Traffic
"""


class TrafficNode:
    # TODO: Sesuaikan atribut lain yang diperlukan untuk menyimpan informasi traffic
    def __init__(self, traffic_id, monitor_id, server_id, metadata):
        self.traffic_id = traffic_id
        self.monitor_id = monitor_id
        self.server_id = server_id
        self.metadata = metadata
        self.next = None


class TrafficQueueLinkedList:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, traffic_id, monitor_id, server_id, metadata):
        new_node = TrafficNode(
            traffic_id=traffic_id,
            monitor_id=monitor_id,
            server_id=server_id,
            metadata=metadata,
        )

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None

        removed_node = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        self.size -= 1
        return removed_node

    def display(self):
        if self.is_empty():
            print("Queue traffic kosong.")
            return

        current = self.front
        nodes = []

        while current is not None:
            text = (
                f"[{current.traffic_id}]\n"
                f" monitor_id : {current.monitor_id}\n"
                f" server_id  : {current.server_id}\n"
                f" metadata   : {current.metadata}"
            )
            nodes.append(text)
            current = current.next

        print("\n -> \n".join(nodes))
