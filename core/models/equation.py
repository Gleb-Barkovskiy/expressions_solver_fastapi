from core.exceptions import (
    EmptyExpressionException,
    DivisionByZeroException,
    InvalidOperatorException,
    InvalidParenthesesException,
    IllogicalExpressionException,
    InvalidExpressionException,
    InvalidVariable,
)


class Equation:
    def __init__(self, title: str, expression: str):
        self.title = title
        self.expression = expression
        self.result = None
        self.error = None
        self.variables = {}

    def solve(self):
        try:
            self.result = self._evaluate()
            self.error = None
        except (InvalidExpressionException, InvalidVariable) as e:
            self.result = None
            self.error = str(e)

    def _remove_comments(self, expression: str) -> str:
        expression = expression.split("//")[0].strip()
        if not expression:
            raise EmptyExpressionException("Expression is empty after removing comments.")
        return expression

    def _evaluate(self) -> float:
        expressions = [self._remove_comments(expr) for expr in self.expression.split(';') if expr.strip()]
        if not expressions:
            raise EmptyExpressionException("No valid expressions found.")

        for expr in expressions[:-1]:
            self._process_expression(expr, store_result=True)

        return self._process_expression(expressions[-1], store_result=False)

    def _process_expression(self, expression: str, store_result: bool) -> float:
        if "=" in expression:
            var_name, expr = map(str.strip, expression.split("=", 1))
            if not var_name.isidentifier():
                raise InvalidVariable(f"Invalid variable name: {var_name}")
            value = self._evaluate_expression(expr)
            self.variables[var_name] = value
            if store_result:
                return value
        else:
            return self._evaluate_expression(expression)

    def _evaluate_expression(self, expression: str) -> float:
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        actions, nums = [], []

        def perform_actions():
            if len(nums) < 2:
                raise IllogicalExpressionException("Illogical expression structure.")
            b = nums.pop()
            a = nums.pop()
            op = actions.pop()

            if op == '+':
                nums.append(a + b)
            elif op == '-':
                nums.append(a - b)
            elif op == '*':
                nums.append(a * b)
            elif op == '/':
                if b == 0:
                    raise DivisionByZeroException("Division by zero is not allowed.")
                nums.append(a / b)
            else:
                raise InvalidOperatorException(op)

        def precedence_check(op1, op2):
            return precedence[op1] >= precedence[op2]

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_start = i
                while i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                    i += 1
                nums.append(float(expression[num_start:i + 1]))

            elif char.isidentifier():
                var_start = i
                while i + 1 < len(expression) and expression[i + 1].isidentifier():
                    i += 1
                var_name = expression[var_start:i + 1]
                if var_name not in self.variables:
                    raise InvalidVariable(f"Undefined variable: {var_name}")
                nums.append(self.variables[var_name])

            elif char == '(':
                actions.append(char)

            elif char == ')':
                while actions and actions[-1] != '(':
                    perform_actions()
                if not actions:
                    raise InvalidParenthesesException("Mismatched parentheses.")
                actions.pop()

            elif char in precedence:
                while actions and actions[-1] != '(' and precedence_check(actions[-1], char):
                    perform_actions()
                actions.append(char)

            else:
                raise InvalidOperatorException(char)

            i += 1

        while actions:
            if actions[-1] == '(':
                raise InvalidParenthesesException("Mismatched parentheses.")
            perform_actions()

        if len(nums) != 1:
            raise IllogicalExpressionException("Illogical expression structure.")
        return nums.pop()