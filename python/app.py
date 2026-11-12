from flask import Flask, render_template, request, jsonify

try:
    from linkedlist import LinkedList
    from stack import Stack
    from infix_postfix import InfixPostfix
    from queue_deque import Queue, Deque
    from binary_tree import BinaryTree, Node
    from letter_conversion import process_letter_conversion, to_uppercase
    from area_of_circle import process_circle_area, calculate_area_of_circle, area_of_circle
    from area_of_triangle import process_triangle_area, calculate_area_of_triangle, area_of_triangle
    from profile import get_profile_level_data, get_melo_library_data
except ImportError:
    from python.linkedlist import LinkedList
    from python.stack import Stack
    from python.infix_postfix import InfixPostfix
    from python.queue_deque import Queue, Deque
    from python.binary_tree import BinaryTree, Node
    from python.letter_conversion import process_letter_conversion, to_uppercase
    from python.area_of_circle import process_circle_area, calculate_area_of_circle, area_of_circle
    from python.area_of_triangle import process_triangle_area, calculate_area_of_triangle, area_of_triangle
    from python.profile import get_profile_level_data, get_melo_library_data

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

linked_list = LinkedList()
stack = Stack()
infix_postfix = InfixPostfix()
queue = Queue()
deque = Deque()
binary_tree = BinaryTree("R")
binary_tree.load_default()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/profile')
def profile():
    return render_template(
        'profile.html',
        profile=get_profile_level_data(),
        melo_song=get_melo_library_data()
    )

@app.route('/api/melo/ako-ang-bagyo')
def api_melo_ako_ang_bagyo():
    return jsonify(get_melo_library_data())

@app.route('/works', methods=['GET', 'POST'])
@app.route('/projects/capitalize', methods=['GET', 'POST'])
def works():
    result = None
    error = None
    input_string = ''
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result, error = process_letter_conversion(input_string)
    return render_template('touppercase.html', result=result, error=error, input_string=input_string)

@app.route('/works/area/circle', methods=['GET', 'POST'])
@app.route('/projects/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    error = None
    radius = ''
    if request.method == 'POST':
        radius = request.form.get('radius', '')
        result, error = process_circle_area(radius)
    return render_template('circle.html', result=result, error=error, radius=radius)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
@app.route('/projects/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    error = None
    base = ''
    height = ''
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        result, error = process_triangle_area(base, height)
    return render_template('triangle.html', result=result, error=error, base=base, height=height)

@app.route('/works/linkedlist', methods=['GET', 'POST'])
@app.route('/projects/linkedlist', methods=['GET', 'POST'])
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

@app.route('/works/stack', methods=['GET', 'POST'])
@app.route('/projects/stack', methods=['GET', 'POST'])
def works_stack():
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form.get('data')

        if action == 'push':
            if data:
                stack.push(data)
                message = f"Pushed '{data}' onto the stack."
            else:
                message = "Please provide a value to push."

        elif action == 'pop':
            popped = stack.pop()
            if popped is not None:
                message = f"Popped '{popped}' from the top of the stack."
            else:
                message = "Stack Underflow: Stack is empty, nothing to pop."

        elif action == 'peek':
            top_val = stack.peek()
            if top_val is not None:
                message = f"Top element is '{top_val}'."
            else:
                message = "Stack is empty, no top element to peek."

        elif action == 'clear':
            stack.clear()
            message = "Stack has been cleared."

    return render_template('stack.html', items=stack.to_list(), message=message, stack_size=stack.size())

@app.route('/works/infix-postfix', methods=['GET', 'POST'])
@app.route('/projects/infix-postfix', methods=['GET', 'POST'])
def works_infix_postfix():
    expression = ''
    postfix = None
    eval_result = None
    error = None

    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()
        if expression:
            postfix, error = infix_postfix.convert(expression)
            if postfix:
                eval_result = infix_postfix.evaluate(postfix)
        else:
            error = 'Please enter an infix expression.'

    return render_template(
        'infix_postfix.html',
        expression=expression,
        postfix=postfix,
        eval_result=eval_result,
        error=error
    )

@app.route('/works/queue', methods=['GET', 'POST'])
@app.route('/projects/queue', methods=['GET', 'POST'])
@app.route('/works/queue-deque', methods=['GET', 'POST'])
@app.route('/projects/queue-deque', methods=['GET', 'POST'])
def works_queue():
    message = None
    structure = request.args.get('tab', 'queue')

    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form.get('data')
        target_struct = request.form.get('structure', 'queue')
        structure = target_struct

        if action == 'enqueue':
            if data:
                queue.enqueue(data)
                message = f"Enqueued '{data}' to tail of Queue."
            else:
                message = "Please provide a value to enqueue."

        elif action == 'dequeue':
            dequeued = queue.dequeue()
            if dequeued is not None:
                message = f"Dequeued '{dequeued}' from head of Queue."
            else:
                message = "Queue Underflow: Queue is empty, nothing to dequeue."

        elif action == 'queue_peek':
            head_val = queue.peek()
            if head_val is not None:
                message = f"Head element is '{head_val}'."
            else:
                message = "Queue is empty, no head element to peek."

        elif action == 'queue_clear':
            queue.clear()
            message = "Queue has been cleared."

        elif action in ('add_head', 'add_front'):
            if data:
                deque.add_head(data)
                message = f"Added '{data}' to head of Deque."
            else:
                message = "Please provide a value to add."

        elif action in ('add_tail', 'add_rear'):
            if data:
                deque.add_tail(data)
                message = f"Added '{data}' to tail of Deque."
            else:
                message = "Please provide a value to add."

        elif action in ('remove_head', 'remove_front'):
            removed = deque.remove_head()
            if removed is not None:
                message = f"Removed '{removed}' from head of Deque."
            else:
                message = "Deque Underflow: Deque is empty, nothing to remove."

        elif action in ('remove_tail', 'remove_rear'):
            removed = deque.remove_tail()
            if removed is not None:
                message = f"Removed '{removed}' from tail of Deque."
            else:
                message = "Deque Underflow: Deque is empty, nothing to remove."

        elif action in ('deque_peek_head', 'deque_peek_front'):
            val = deque.peek_head()
            if val is not None:
                message = f"Head element is '{val}'."
            else:
                message = "Deque is empty, no head element."

        elif action in ('deque_peek_tail', 'deque_peek_rear'):
            val = deque.peek_tail()
            if val is not None:
                message = f"Tail element is '{val}'."
            else:
                message = "Deque is empty, no tail element."

        elif action == 'deque_clear':
            deque.clear()
            message = "Deque has been cleared."

    return render_template(
        'queue.html',
        queue_items=queue.to_list(),
        queue_size=queue.size(),
        queue_head=queue.peek(),
        queue_tail=queue.tail.data if queue.tail else None,
        queue_front=queue.peek(),
        queue_rear=queue.tail.data if queue.tail else None,
        deque_items=deque.to_list(),
        deque_size=deque.size(),
        deque_head=deque.peek_head(),
        deque_tail=deque.peek_tail(),
        deque_front=deque.peek_head(),
        deque_rear=deque.peek_tail(),
        active_tab=structure,
        message=message
    )

@app.route('/works/binary-tree', methods=['GET', 'POST'])
@app.route('/projects/binary-tree', methods=['GET', 'POST'])
def works_binary_tree():
    message = None
    search_result = None

    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form.get('data', '').strip()
        parent_val = request.form.get('parent', '').strip()
        target = request.form.get('target', '').strip()

        if action == 'set_root':
            if data:
                binary_tree.set_root(data)
                message = f"Set root node to '{data}'."
            else:
                message = "Please provide a value for the root node."

        elif action == 'insert_left':
            if not data:
                message = "Please provide a value to insert."
            elif binary_tree.root is None:
                binary_tree.set_root(data)
                message = f"Tree was empty. Created root node '{data}'."
            else:
                target_node = binary_tree.root if not parent_val else binary_tree.find(binary_tree.root, parent_val)
                if target_node is None:
                    message = f"Parent node '{parent_val}' not found in the tree."
                else:
                    binary_tree.insert_left(target_node, data)
                    message = f"Inserted '{data}' as left child of '{target_node.value}'."

        elif action == 'insert_right':
            if not data:
                message = "Please provide a value to insert."
            elif binary_tree.root is None:
                binary_tree.set_root(data)
                message = f"Tree was empty. Created root node '{data}'."
            else:
                target_node = binary_tree.root if not parent_val else binary_tree.find(binary_tree.root, parent_val)
                if target_node is None:
                    message = f"Parent node '{parent_val}' not found in the tree."
                else:
                    binary_tree.insert_right(target_node, data)
                    message = f"Inserted '{data}' as right child of '{target_node.value}'."

        elif action == 'search':
            if target:
                found = binary_tree.find(binary_tree.root, target) if binary_tree.root else None
                if found:
                    message = f"Node '{target}' was found in the binary tree!"
                    search_result = target
                else:
                    message = f"Node '{target}' was not found in the binary tree."
            else:
                message = "Please enter a value to search."

        elif action == 'load_default':
            binary_tree.load_default()
            message = "Loaded example binary tree (R with subtrees A and B)."

        elif action == 'clear':
            binary_tree.clear()
            message = "Binary tree has been cleared."

    preorder = binary_tree.preorder_traversal(binary_tree.root, "").strip() if binary_tree.root else ""
    inorder = binary_tree.inorder_traversal(binary_tree.root, "").strip() if binary_tree.root else ""
    postorder = binary_tree.postorder_traversal(binary_tree.root, "").strip() if binary_tree.root else ""

    return render_template(
        'binary_tree.html',
        tree=binary_tree.to_dict(),
        tree_root=binary_tree.root.value if binary_tree.root else None,
        node_count=binary_tree.count_nodes(),
        tree_height=binary_tree.height(),
        all_nodes=binary_tree.get_nodes(),
        preorder=preorder,
        inorder=inorder,
        postorder=postorder,
        search_result=search_result,
        message=message
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    error = None
    success = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        if not name:
            error = "Please enter your full name."
        elif not email or '@' not in email or '.' not in email.split('@')[-1]:
            error = "Please enter a valid email address."
        elif not subject:
            error = "Please enter a subject."
        elif not message or len(message) < 5:
            error = "Please enter a message (at least 5 characters)."
        else:
            success = "Message received successfully! We will get back to you shortly."
    return render_template('contact.html', error=error, success=success)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
