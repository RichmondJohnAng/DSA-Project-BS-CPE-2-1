from flask import Flask, render_template, request

app = Flask(__name__)

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


linked_list = LinkedList()

def area_of_triangle(base, height):
    return 0.5 * float(base) * float(height)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    if request.method == 'POST':
        radius = request.form.get('radius', '')
        try:
            result = float(radius) * 3.14 * float(radius)
        except (ValueError, TypeError):
            result = "Invalid input"
    return render_template('circle.html', result=result)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        try:
            result = area_of_triangle(base, height)
        except (ValueError, TypeError):
            result = "Invalid input: Please enter valid numbers."
    return render_template('triangle.html', result=result)

@app.route('/works/linkedlist', methods=['GET', 'POST'])
def works_linkedlist():
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form.get('data')
        target = request.form.get('target')

        if action == 'insert_at_beginning':
            if data:
                linked_list.insert_at_beginning(data)
                message = f"Inserted '{data}' at beginning."
            else:
                message = "Please provide a value to insert."

        elif action == 'insert_at_end':
            if data:
                linked_list.insert_at_end(data)
                message = f"Inserted '{data}' at end."
            else:
                message = "Please provide a value to insert."

        elif action == 'insert_after':
            if target and data:
                if linked_list.insert_after(target, data):
                    message = f"Inserted '{data}' after '{target}'."
                else:
                    message = f"Target '{target}' not found in the list."
            else:
                message = "Please provide both target and new value."

        elif action == 'remove_at_beginning':
            removed = linked_list.remove_at_beginning()
            if removed is not None:
                message = f"Removed '{removed}' from beginning."
            else:
                message = "List is empty, nothing to remove."

        elif action == 'remove_at_end':
            removed = linked_list.remove_at_end()
            if removed is not None:
                message = f"Removed '{removed}' from end."
            else:
                message = "List is empty, nothing to remove."

        elif action == 'remove_target':
            if target:
                if linked_list.remove_target(target):
                    message = f"Removed target '{target}'."
                else:
                    message = f"Target '{target}' not found in the list."
            else:
                message = "Please provide target value to remove."

    return render_template('linkedlist.html', items=linked_list.to_list(), message=message)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
