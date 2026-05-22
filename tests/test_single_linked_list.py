from DSA import SingleLinkedList


def test_new_linked_list_should_be_empty():
    linked_list = SingleLinkedList()

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_add_front_to_empty_list():
    linked_list = SingleLinkedList()

    linked_list.add_front("Server A")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server A"
    assert linked_list.head == linked_list.tail
    assert linked_list.get_size() == 1
    assert linked_list.traverse_recursive() == ["Server A"]


def test_add_front_to_non_empty_list():
    linked_list = SingleLinkedList()

    linked_list.add_front("Server B")
    linked_list.add_front("Server A")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server B"
    assert linked_list.head.next == linked_list.tail
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Server A", "Server B"]


def test_add_back_to_empty_list():
    linked_list = SingleLinkedList()

    linked_list.add_back("Server A")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server A"
    assert linked_list.head == linked_list.tail
    assert linked_list.get_size() == 1
    assert linked_list.traverse_recursive() == ["Server A"]


def test_add_back_to_non_empty_list():
    linked_list = SingleLinkedList()

    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server C"
    assert linked_list.get_size() == 3
    assert linked_list.traverse_recursive() == [
        "Server A",
        "Server B",
        "Server C",
    ]


def test_add_front_and_add_back_combination():
    linked_list = SingleLinkedList()

    linked_list.add_back("Server B")
    linked_list.add_front("Server A")
    linked_list.add_back("Server C")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server C"
    assert linked_list.get_size() == 3
    assert linked_list.traverse_recursive() == [
        "Server A",
        "Server B",
        "Server C",
    ]


def test_remove_front_from_empty_list_should_return_none():
    linked_list = SingleLinkedList()

    removed_data = linked_list.remove_front()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_front_from_single_node_list():
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")

    removed_data = linked_list.remove_front()

    assert removed_data == "Server A"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_remove_front_from_multiple_nodes_list():
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    removed_data = linked_list.remove_front()

    assert removed_data == "Server A"
    assert linked_list.head.data == "Server B"
    assert linked_list.tail.data == "Server C"
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Server B", "Server C"]


def test_remove_back_from_empty_list_should_return_none():
    linked_list = SingleLinkedList()

    removed_data = linked_list.remove_back()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_back_from_single_node_list():
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")

    removed_data = linked_list.remove_back()

    assert removed_data == "Server A"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_remove_back_from_multiple_nodes_list():
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    removed_data = linked_list.remove_back()

    assert removed_data == "Server C"
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server B"
    assert linked_list.tail.next is None
    assert linked_list.get_size() == 2
    assert linked_list.traverse_recursive() == ["Server A", "Server B"]


def test_remove_until_empty():
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")

    assert linked_list.remove_front() == "Server A"
    assert linked_list.remove_back() == "Server B"

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_recursive() == []


def test_display_recursive_for_empty_list(capsys):
    linked_list = SingleLinkedList()

    linked_list.display_recursive()

    captured = capsys.readouterr()
    assert captured.out == "NULL\n"


def test_display_recursive_for_non_empty_list(capsys):
    linked_list = SingleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    linked_list.display_recursive()

    captured = capsys.readouterr()
    assert captured.out == "Server A -> Server B -> Server C -> NULL\n"
