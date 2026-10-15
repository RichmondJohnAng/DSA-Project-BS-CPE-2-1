class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def insert_after(self, target, data):
        target_val = target.data if isinstance(target, Node) else target
        curr = self.head
        while curr:
            if curr == target or curr.data == target_val or str(curr.data) == str(target_val):
                new_node = Node(data)
                new_node.next = curr.next
                curr.next = new_node
                return True
            curr = curr.next
        return False

    def remove_at_beginning(self):
        if not self.head:
            return None
        removed_data = self.head.data
        self.head = self.head.next
        return removed_data

    def remove_at_end(self):
        if not self.head:
            return None
        if not self.head.next:
            removed_data = self.head.data
            self.head = None
            return removed_data
        curr = self.head
        while curr.next.next:
            curr = curr.next
        removed_data = curr.next.data
        curr.next = None
        return removed_data

    def remove_target(self, target):
        if not self.head:
            return False

        target_val = target.data if isinstance(target, Node) else target

        if self.head == target or self.head.data == target_val or str(self.head.data) == str(target_val):
            self.head = self.head.next
            return True

        curr = self.head
        while curr.next:
            if curr.next == target or curr.next.data == target_val or str(curr.next.data) == str(target_val):
                curr.next = curr.next.next
                return True
            curr = curr.next
        return False

    def to_list(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(curr.data)
            curr = curr.next
        return elements

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    def __repr__(self):
        nodes = self.to_list()
        return " -> ".join(map(str, nodes)) if nodes else "Empty List"
