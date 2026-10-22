class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None

    def is_empty(self):
        return self.top is None

    def size(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):
        elements = []
        current = self.top
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        self.top = None

    def print_stack(self):
        if self.top is None:
            print("Stack is empty")
        else:
            current = self.top
            print("Stack elements (top → bottom):")
            while current:
                print(current.data)
                current = current.next


if __name__ == "__main__":
    stack = Stack()
    stack.print_stack()

    stack.push(10)
    stack.push(20)
    stack.push(30)
    stack.print_stack()

    print("Top element:", stack.peek())
    print("Popped:", stack.pop())
    print("Popped:", stack.pop())
    stack.print_stack()

    print("Popped:", stack.pop())
    print("Popped from empty stack:", stack.pop())
    print("Peek on empty stack:", stack.peek())
    stack.print_stack()
