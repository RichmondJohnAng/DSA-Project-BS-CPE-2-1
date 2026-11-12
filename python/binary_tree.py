class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"

class BinaryTree:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def set_root(self, value):
        self.root = Node(value)
        return self.root

    def insert_left(self, current_node, value):
        if current_node is None:
            return None
        if current_node.left is None:
            current_node.left = Node(value)
            return current_node.left
        else:
            new_node = Node(value)
            new_node.left = current_node.left
            current_node.left = new_node
            return new_node

    def insert_right(self, current_node, value):
        if current_node is None:
            return None
        if current_node.right is None:
            current_node.right = Node(value)
            return current_node.right
        else:
            new_node = Node(value)
            new_node.right = current_node.right
            current_node.right = new_node
            return new_node

    def preorder_traversal(self, start, traversal=""):
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal    

    def inorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal    

    def postorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += (str(start.value) + " ")
        return traversal

    def find(self, start, value):
        if start is None:
            return None
        if str(start.value) == str(value):
            return start
        left_found = self.find(start.left, value)
        if left_found is not None:
            return left_found
        return self.find(start.right, value)

    def get_nodes(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return []
        nodes = [str(start.value)]
        if start.left:
            nodes.extend(self.get_nodes(start.left, False))
        if start.right:
            nodes.extend(self.get_nodes(start.right, False))
        return nodes

    def to_dict(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return None
        return {
            'value': str(start.value),
            'left': self.to_dict(start.left, False) if start.left else None,
            'right': self.to_dict(start.right, False) if start.right else None
        }

    def count_nodes(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return 0
        return 1 + self.count_nodes(start.left, False) + self.count_nodes(start.right, False)

    def height(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return 0
        return 1 + max(self.height(start.left, False), self.height(start.right, False))

    def clear(self):
        self.root = None

    def load_default(self):
        self.root = Node("R")
        self.insert_left(self.root, "A")
        self.insert_right(self.root, "B")
        self.insert_left(self.root.left, "C")
        self.insert_right(self.root.left, "D")
        self.insert_left(self.root.right, "E")
        self.insert_right(self.root.right, "F")
        self.insert_left(self.root.right.right, "G")

if __name__ == "__main__":
    tree = BinaryTree("R")
    
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")
    
    print()
    print("Preorder traversal: " + tree.preorder_traversal(tree.root, ""))
    print("\n\nInorder traversal: " + tree.inorder_traversal(tree.root, ""))
    print("\n\nPostorder traversal: " + tree.postorder_traversal(tree.root, ""))
    print()
