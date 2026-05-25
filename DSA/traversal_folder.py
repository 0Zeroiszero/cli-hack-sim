class BST:
    def __init__(self):
        pass

    # root - left - right
    def preorder(self, node):
        if node is not None:
            print(node.data, end=' ')
            self.preorder(node.left)
            self.preorder(node.right)

    # left - root - right 
    def inorder(self, node):
        if node is not None:
            self.in_order(node.left)
            print(node.data, end=' ')
            self.in_order(node.right)

    # left - right - root
    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data, end=' ')
