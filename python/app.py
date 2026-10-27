from flask import Flask, render_template, request

try:
    from linkedlist import LinkedList
    from stack import Stack
    from infix_postfix import InfixPostfix
    from queue_deque import Queue, Deque
except ImportError:
    from python.linkedlist import LinkedList
    from python.stack import Stack
    from python.infix_postfix import InfixPostfix
    from python.queue_deque import Queue, Deque

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

linked_list = LinkedList()
stack = Stack()
infix_postfix = InfixPostfix()
queue = Queue()
deque = Deque()

def area_of_triangle(base, height):
    return 0.5 * float(base) * float(height)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works', methods=['GET', 'POST'])
@app.route('/projects/capitalize', methods=['GET', 'POST'])
def works():
    result = None
    error = None
    input_string = ''
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        if not input_string.strip():
            error = "Please enter some text."
        elif not all(c.isalpha() or c.isspace() for c in input_string):
            error = "Invalid input: Numbers and special characters are not accepted. Only letters (A-Z, a-z) are allowed."
        else:
            result = input_string.upper()
    return render_template('touppercase.html', result=result, error=error, input_string=input_string)

@app.route('/works/area/circle', methods=['GET', 'POST'])
@app.route('/projects/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    error = None
    radius = ''
    if request.method == 'POST':
        radius = request.form.get('radius', '').strip()
        if not radius:
            error = "Please enter a radius value."
        else:
            try:
                r = float(radius)
                if r <= 0:
                    error = "Invalid input: Radius must be a positive number greater than 0."
                else:
                    area = 3.141592653589793 * (r ** 2)
                    result = round(area, 4) if not area.is_integer() else int(area)
            except (ValueError, TypeError):
                error = "Invalid input: Letters and special characters are not accepted. Please enter a valid number."
    return render_template('circle.html', result=result, error=error, radius=radius)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
@app.route('/projects/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    error = None
    base = ''
    height = ''
    if request.method == 'POST':
        base = request.form.get('base', '').strip()
        height = request.form.get('height', '').strip()
        if not base or not height:
            error = "Please enter both base and height values."
        else:
            try:
                b = float(base)
                h = float(height)
                if b <= 0 or h <= 0:
                    error = "Invalid input: Base and height must be positive numbers greater than 0."
                else:
                    area = area_of_triangle(b, h)
                    result = round(area, 4) if not area.is_integer() else int(area)
            except (ValueError, TypeError):
                error = "Invalid input: Letters and special characters are not accepted. Please enter valid numbers."
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
