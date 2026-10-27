class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None
        current_node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        current_node.next = None
        return current_node.data

    def peek(self):
        if self.head is None:
            return None
        return self.head.data

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        self.head = None
        self.tail = None


class DequeNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"DequeNode({self.data})"


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def add_head(self, item):
        new_node = DequeNode(item)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    add_front = add_head

    def add_tail(self, item):
        new_node = DequeNode(item)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    add_rear = add_tail

    def remove_head(self):
        if self.head is None:
            return None
        removed_data = self.head.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return removed_data

    remove_front = remove_head

    def remove_tail(self):
        if self.tail is None:
            return None
        removed_data = self.tail.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        return removed_data

    remove_rear = remove_tail

    def peek_head(self):
        if self.head is None:
            return None
        return self.head.data

    peek_front = peek_head

    def peek_tail(self):
        if self.tail is None:
            return None
        return self.tail.data

    peek_rear = peek_tail

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        self.head = None
        self.tail = None
