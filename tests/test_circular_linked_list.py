from DSA import CircularLinkedList


def test_new_circular_linked_list_should_be_empty():
    linked_list = CircularLinkedList()

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_add_front_to_empty_list():
    linked_list = CircularLinkedList()

    linked_list.add_front("Monitor 1")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 1"
    assert linked_list.head == linked_list.tail
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 1
    assert linked_list.traverse_recursive() == ["Monitor 1"]


def test_add_front_to_non_empty_list():
    linked_list = CircularLinkedList()

    linked_list.add_front("Monitor 2")
    linked_list.add_front("Monitor 1")

    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 2"
    assert linked_list.head.next == linked_list.tail
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Monitor 1", "Monitor 2"]


def test_add_back_to_empty_list():
    linked_list = CircularLinkedList()

    linked_list.add_back("Monitor 1")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 1"
    assert linked_list.head == linked_list.tail
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 1
    assert linked_list.traverse_recursive() == ["Monitor 1"]


def test_add_back_to_non_empty_list():
    linked_list = CircularLinkedList()

    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")
    linked_list.add_back("Monitor 3")

    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 3"
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 3
    assert linked_list.traverse_recursive() == [
        "Monitor 1",
        "Monitor 2",
        "Monitor 3",
    ]


def test_add_front_and_add_back_combination():
    linked_list = CircularLinkedList()

    linked_list.add_back("Monitor 2")
    linked_list.add_front("Monitor 1")
    linked_list.add_back("Monitor 3")

    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 3"
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 3
    assert linked_list.traverse_recursive() == [
        "Monitor 1",
        "Monitor 2",
        "Monitor 3",
    ]


def test_remove_front_from_empty_list_should_return_none():
    linked_list = CircularLinkedList()

    removed_data = linked_list.remove_front()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_front_from_single_node_list():
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")

    removed_data = linked_list.remove_front()

    assert removed_data == "Monitor 1"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_remove_front_from_multiple_nodes_list():
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")
    linked_list.add_back("Monitor 3")

    removed_data = linked_list.remove_front()

    assert removed_data == "Monitor 1"
    assert linked_list.head.data == "Monitor 2"
    assert linked_list.tail.data == "Monitor 3"
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Monitor 2", "Monitor 3"]


def test_remove_back_from_empty_list_should_return_none():
    linked_list = CircularLinkedList()

    removed_data = linked_list.remove_back()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_back_from_single_node_list():
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")

    removed_data = linked_list.remove_back()

    assert removed_data == "Monitor 1"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_remove_back_from_multiple_nodes_list():
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")
    linked_list.add_back("Monitor 3")

    removed_data = linked_list.remove_back()

    assert removed_data == "Monitor 3"
    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 2"
    assert linked_list.tail.next == linked_list.head
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Monitor 1", "Monitor 2"]


def test_remove_until_empty():
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")

    assert linked_list.remove_front() == "Monitor 1"
    assert linked_list.remove_back() == "Monitor 2"

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_tail_next_should_always_point_to_head_after_multiple_operations():
    linked_list = CircularLinkedList()

    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")
    linked_list.add_front("Monitor 0")
    linked_list.remove_front()
    linked_list.add_back("Monitor 3")
    linked_list.remove_back()

    assert linked_list.head.data == "Monitor 1"
    assert linked_list.tail.data == "Monitor 2"
    assert linked_list.tail.next == linked_list.head
    assert linked_list.traverse_recursive() == ["Monitor 1", "Monitor 2"]


def test_display_recursive_for_empty_list(capsys):
    linked_list = CircularLinkedList()

    linked_list.display_recursive()

    captured = capsys.readouterr()
    assert captured.out == "Kosong\n"


def test_display_recursive_for_non_empty_list(capsys):
    linked_list = CircularLinkedList()
    linked_list.add_back("Monitor 1")
    linked_list.add_back("Monitor 2")
    linked_list.add_back("Monitor 3")

    linked_list.display_recursive()

    captured = capsys.readouterr()
    assert captured.out == ("Monitor 1 -> Monitor 2 -> Monitor 3 -> kembali ke HEAD\n")
