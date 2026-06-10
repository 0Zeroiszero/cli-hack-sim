<<<<<<< HEAD
"""Tests for DoubleLinkedList data structure."""

=======
>>>>>>> main
from DSA import DoubleLinkedList


def test_new_double_linked_list_should_be_empty():
<<<<<<< HEAD
    """Verify a newly created DoubleLinkedList is empty.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_forward_recursive() == []
    assert linked_list.traverse_backward_recursive() == []


def test_add_front_to_empty_list():
<<<<<<< HEAD
    """Verify add_front works correctly on an empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.add_front("Server A")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server A"
    assert linked_list.head == linked_list.tail
    assert linked_list.head.prev is None
    assert linked_list.head.next is None
    assert linked_list.get_size() == 1
    assert linked_list.traverse_forward_recursive() == ["Server A"]
    assert linked_list.traverse_backward_recursive() == ["Server A"]


def test_add_front_to_non_empty_list():
<<<<<<< HEAD
    """Verify add_front prepends a node to a non-empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.add_front("Server B")
    linked_list.add_front("Server A")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server B"

    assert linked_list.head.prev is None
    assert linked_list.head.next == linked_list.tail
    assert linked_list.tail.prev == linked_list.head
    assert linked_list.tail.next is None

    assert linked_list.get_size() == 2
    assert linked_list.traverse_forward_recursive() == ["Server A", "Server B"]
<<<<<<< HEAD
    assert linked_list.traverse_backward_recursive() == [
        "Server B",
        "Server A",
    ]


def test_add_back_to_empty_list():
    """Verify add_back works correctly on an empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
    assert linked_list.traverse_backward_recursive() == ["Server B", "Server A"]


def test_add_back_to_empty_list():
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.add_back("Server A")

    assert linked_list.is_empty() is False
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server A"
    assert linked_list.head == linked_list.tail
    assert linked_list.head.prev is None
    assert linked_list.head.next is None
    assert linked_list.get_size() == 1
    assert linked_list.traverse_forward_recursive() == ["Server A"]
    assert linked_list.traverse_backward_recursive() == ["Server A"]


def test_add_back_to_non_empty_list():
<<<<<<< HEAD
    """Verify add_back appends a node to a non-empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server C"

    assert linked_list.head.prev is None
    assert linked_list.head.next.data == "Server B"
    assert linked_list.tail.prev.data == "Server B"
    assert linked_list.tail.next is None

    assert linked_list.get_size() == 3
    assert linked_list.traverse_forward_recursive() == [
        "Server A",
        "Server B",
        "Server C",
    ]
    assert linked_list.traverse_backward_recursive() == [
        "Server C",
        "Server B",
        "Server A",
    ]


def test_add_front_and_add_back_combination():
<<<<<<< HEAD
    """Verify mixed add_front and add_back operations maintain correct order.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.add_back("Server B")
    linked_list.add_front("Server A")
    linked_list.add_back("Server C")

    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server C"

    assert linked_list.head.next.data == "Server B"
    assert linked_list.head.next.prev == linked_list.head
    assert linked_list.tail.prev.data == "Server B"
    assert linked_list.tail.prev.next == linked_list.tail

    assert linked_list.get_size() == 3
    assert linked_list.traverse_forward_recursive() == [
        "Server A",
        "Server B",
        "Server C",
    ]
    assert linked_list.traverse_backward_recursive() == [
        "Server C",
        "Server B",
        "Server A",
    ]


def test_remove_front_from_empty_list_should_return_none():
<<<<<<< HEAD
    """Verify remove_front returns None on an empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    removed_data = linked_list.remove_front()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_front_from_single_node_list():
<<<<<<< HEAD
    """Verify remove_front removes the only node and leaves the list empty.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")

    removed_data = linked_list.remove_front()

    assert removed_data == "Server A"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_forward_recursive() == []
    assert linked_list.traverse_backward_recursive() == []


def test_remove_front_from_multiple_nodes_list():
<<<<<<< HEAD
    """Verify remove_front removes the head node from a multi-node list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    removed_data = linked_list.remove_front()

    assert removed_data == "Server A"
    assert linked_list.head.data == "Server B"
    assert linked_list.tail.data == "Server C"
    assert linked_list.head.prev is None
    assert linked_list.head.next == linked_list.tail
    assert linked_list.tail.prev == linked_list.head
    assert linked_list.tail.next is None
    assert linked_list.get_size() == 2
    assert linked_list.traverse_forward_recursive() == ["Server B", "Server C"]
<<<<<<< HEAD
    assert linked_list.traverse_backward_recursive() == [
        "Server C",
        "Server B",
    ]


def test_remove_back_from_empty_list_should_return_none():
    """Verify remove_back returns None on an empty list.

    Args:
        None.

    Returns:
        None.
    """
=======
    assert linked_list.traverse_backward_recursive() == ["Server C", "Server B"]


def test_remove_back_from_empty_list_should_return_none():
>>>>>>> main
    linked_list = DoubleLinkedList()

    removed_data = linked_list.remove_back()

    assert removed_data is None
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0


def test_remove_back_from_single_node_list():
<<<<<<< HEAD
    """Verify remove_back removes the only node and leaves the list empty.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")

    removed_data = linked_list.remove_back()

    assert removed_data == "Server A"
    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_forward_recursive() == []
    assert linked_list.traverse_backward_recursive() == []


def test_remove_back_from_multiple_nodes_list():
<<<<<<< HEAD
    """Verify remove_back removes the tail node from a multi-node list.

    Args:
        None.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    removed_data = linked_list.remove_back()

    assert removed_data == "Server C"
    assert linked_list.head.data == "Server A"
    assert linked_list.tail.data == "Server B"
    assert linked_list.head.prev is None
    assert linked_list.tail.next is None
    assert linked_list.head.next == linked_list.tail
    assert linked_list.tail.prev == linked_list.head
    assert linked_list.get_size() == 2
    assert linked_list.traverse_forward_recursive() == ["Server A", "Server B"]
<<<<<<< HEAD
    assert linked_list.traverse_backward_recursive() == [
        "Server B",
        "Server A",
    ]


def test_remove_until_empty():
    """Verify repeated remove operations eventually empty the list.

    Args:
        None.

    Returns:
        None.
    """
=======
    assert linked_list.traverse_backward_recursive() == ["Server B", "Server A"]


def test_remove_until_empty():
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")

    assert linked_list.remove_front() == "Server A"
    assert linked_list.remove_back() == "Server B"

    assert linked_list.is_empty() is True
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.get_size() == 0
    assert linked_list.traverse_forward_recursive() == []
    assert linked_list.traverse_backward_recursive() == []


def test_display_forward_recursive_for_empty_list(capsys):
<<<<<<< HEAD
    """Verify display_forward_recursive prints 'NULL' for an empty list.

    Args:
        capsys: Pytest fixture to capture stdout/stderr.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.display_forward_recursive()

    captured = capsys.readouterr()
    assert captured.out == "NULL\n"


def test_display_forward_recursive_for_non_empty_list(capsys):
<<<<<<< HEAD
    """Verify display_forward_recursive prints the correct forward traversal.

    Args:
        capsys: Pytest fixture to capture stdout/stderr.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    linked_list.display_forward_recursive()

    captured = capsys.readouterr()
    assert captured.out == "Server A <-> Server B <-> Server C <-> NULL\n"


def test_display_backward_recursive_for_empty_list(capsys):
<<<<<<< HEAD
    """Verify display_backward_recursive prints 'NULL' for an empty list.

    Args:
        capsys: Pytest fixture to capture stdout/stderr.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()

    linked_list.display_backward_recursive()

    captured = capsys.readouterr()
    assert captured.out == "NULL\n"


def test_display_backward_recursive_for_non_empty_list(capsys):
<<<<<<< HEAD
    """Verify display_backward_recursive prints the correct backward traversal.

    Args:
        capsys: Pytest fixture to capture stdout/stderr.

    Returns:
        None.
    """
=======
>>>>>>> main
    linked_list = DoubleLinkedList()
    linked_list.add_back("Server A")
    linked_list.add_back("Server B")
    linked_list.add_back("Server C")

    linked_list.display_backward_recursive()

    captured = capsys.readouterr()
    assert captured.out == "Server C <-> Server B <-> Server A <-> NULL\n"
