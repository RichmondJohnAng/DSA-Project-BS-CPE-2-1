from flask import Flask, render_template, request
from linkedlist import LinkedList
from stack import Stack
from infix_postfix import InfixPostfix

app = Flask(__name__)

linked_list = LinkedList()
stack = Stack()
infix_postfix = InfixPostfix()

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
