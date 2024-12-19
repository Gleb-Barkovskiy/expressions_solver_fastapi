class InvalidExpressionException(Exception):
    pass


class EmptyExpressionException(InvalidExpressionException):
    pass


class DivisionByZeroException(InvalidExpressionException):
    pass


class InvalidOperatorException(InvalidExpressionException):
    def __init__(self, operator):
        super().__init__(f"Invalid operator: {operator}")
        self.operator = operator


class InvalidParenthesesException(InvalidExpressionException):
    pass


class IllogicalExpressionException(InvalidExpressionException):
    pass


class InvalidVariable(InvalidExpressionException):
    pass
