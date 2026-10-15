import re

class InfixPostfix:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}

    def is_operator(self, token):
        return token in self.precedence

    def is_operand(self, token):
        if not token:
            return False
        if re.fullmatch(r'\d+(?:\.\d+)?', token):
            return True
        if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', token):
            return True
        return False

    def validate_infix(self, expression):
        if not expression or not expression.strip():
            return False, "Please enter an infix expression.", []

        raw_tokens = re.findall(r'\d+(?:\.\d+)?|[a-zA-Z_][a-zA-Z0-9_]*|[+\-*/%^()]|[^\s]', expression.strip())

        for t in raw_tokens:
            if not (self.is_operand(t) or self.is_operator(t) or t in ('(', ')')):
                return False, f"Invalid character '{t}'. Only letters, numbers, and operators (+, -, *, /, %, ^, (, )) are allowed.", []

        tokens = raw_tokens
        if not tokens:
            return False, "Empty expression.", []

        paren_count = 0
        prev_token = None

        for i, token in enumerate(tokens):
            if token == '(':
                paren_count += 1
                if prev_token is not None and (self.is_operand(prev_token) or prev_token == ')'):
                    return False, f"Invalid infix expression: Missing operator between '{prev_token}' and '('.", []
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    return False, "Mismatched parentheses: Unexpected closing parenthesis ')'.", []
                if prev_token == '(':
                    return False, "Invalid infix expression: Empty parentheses '()' are not allowed.", []
                if prev_token is not None and self.is_operator(prev_token):
                    return False, f"Invalid infix expression: Operator '{prev_token}' cannot be followed by ')'.", []
            elif self.is_operator(token):
                if i == 0:
                    return False, f"Invalid infix expression: Cannot start with operator '{token}'.", []
                if prev_token == '(':
                    return False, f"Invalid infix expression: Operator '{token}' cannot follow '('.", []
                if prev_token is not None and self.is_operator(prev_token):
                    return False, f"Invalid infix expression: Consecutive operators '{prev_token}' and '{token}'.", []
            elif self.is_operand(token):
                if prev_token is not None and (self.is_operand(prev_token) or prev_token == ')'):
                    return False, f"Invalid infix expression: Consecutive operands or missing operator between '{prev_token}' and '{token}'.", []

            prev_token = token

        if paren_count != 0:
            return False, "Mismatched parentheses: Missing closing parenthesis ')'.", []

        if tokens and self.is_operator(tokens[-1]):
            return False, f"Invalid infix expression: Cannot end with operator '{tokens[-1]}'.", []

        return True, None, tokens

    def convert(self, expression):
        is_valid, error, tokens = self.validate_infix(expression)
        if not is_valid:
            return None, error

        stack = []
        output = []

        for token in tokens:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
            elif self.is_operator(token):
                curr_prec = self.precedence[token]
                is_right_assoc = token == '^'

                while stack and stack[-1] != '(' and self.is_operator(stack[-1]):
                    top_prec = self.precedence[stack[-1]]
                    if (is_right_assoc and curr_prec < top_prec) or (not is_right_assoc and curr_prec <= top_prec):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)

        while stack:
            output.append(stack.pop())

        return ' '.join(output), None

    def evaluate(self, postfix_str):
        if not postfix_str:
            return None
        tokens = postfix_str.split()
        stack = []

        for token in tokens:
            if re.fullmatch(r'-?\d+(?:\.\d+)?', token):
                val = float(token) if '.' in token else int(token)
                stack.append(val)
            elif self.is_operator(token):
                if len(stack) < 2:
                    return None
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    res = a + b
                elif token == '-':
                    res = a - b
                elif token == '*':
                    res = a * b
                elif token == '/':
                    if b == 0:
                        return None
                    res = a / b
                elif token == '%':
                    if b == 0:
                        return None
                    res = a % b
                elif token == '^':
                    res = a ** b
                else:
                    return None

                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                elif isinstance(res, float):
                    res = round(res, 4)
                stack.append(res)
            else:
                return None

        if len(stack) == 1:
            return stack[0]
        return None
