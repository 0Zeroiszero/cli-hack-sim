"""
@author: PLEASE INI SIAPA YANG BUAT <<<<<<<<
@modified: 02/06/2026 oleh Abdullah Affandi
- kontrak abstraksi untuk traversal pada binary search tree
- preorder, inorder, postorder
- kalau mau buat traversal lain, buat method baru dengan abstraksi yang sama
"""

from abc import abstractmethod


class BST:
    def __init__(self):
        pass

    @abstractmethod
    # root - left - right
    def preorder(self, node):
        """
        Gunakan rekursi untuk menampilkan node.left dan node.right
        """
        # if node is not None:
        # print(node.data, end=' ')

        # self.preorder(node.left)
        # self.preorder(node.right)
        pass

    @abstractmethod
    # left - root - right
    def inorder(self, node):
        """
        Gunakan rekursi untuk menampilkan node.left dan node.right
        """
        # if node is not None:
        # self.in_order(node.left)

        # print(node.data, end=' ')

        # self.in_order(node.right)
        pass

    @abstractmethod
    # left - right - root
    def postorder(self, node):
        """
        Gunakan rekursi untuk menampilkan node.left dan node.right
        """
        # if node is not None:
        # self.postorder(node.left)
        # self.postorder(node.right)

        # print(node.data, end=' ')
        pass
