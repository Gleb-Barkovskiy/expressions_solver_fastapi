import pytest
from core.exceptions import (
    EmptyExpressionException,
    DivisionByZeroException,
    InvalidOperatorException,
    InvalidParenthesesException,
    IllogicalExpressionException,
    InvalidVariable,
)
from core.models.equation import Equation

@pytest.mark.parametrize(
    "title, expression, expected_result",
    [
        ("Simple Addition", "3 + 5", 8.0),
        ("Mixed Operations", "3 + 5 * 2", 13.0),
        ("Parentheses", "(1 + 2) * 3", 9.0),
        ("Comments Removed", "10 + 5 // this is a comment", 15.0),
        ("Complex Expression", "(1 + 2) * (3 - 1) / 2 + 10", 13.0),
        ("Variables", "x = 5; y = 5; x + y", 10.0)
    ],
)
def test_valid_equations(title, expression, expected_result):
    eq = Equation(title, expression)
    eq.solve()
    assert eq.result == expected_result
    assert eq.error is None


@pytest.mark.parametrize(
    "title, expression, expected_exception, expected_message",
    [
        ("Empty Expression", "// comment only", EmptyExpressionException, "Expression is empty"),
        ("Division by Zero", "10 / (5 - 5)", DivisionByZeroException, "Division by zero"),
        ("Invalid Operator", "10 $ 5", InvalidOperatorException, "$"),
        ("Mismatched Parentheses", "3 + (5 * 2", InvalidParenthesesException, "Mismatched parentheses"),
        ("Illogical Expression", "3 + * 2", IllogicalExpressionException, "Illogical expression structure"),
        ("Undefined Variable", "x + 5 x", InvalidVariable, "Undefined variable"),
        ("Invalid Variable Name", "1x = 10", InvalidVariable, "Invalid variable name"),
        ("Illogical Expression", "x = 5; x + * 2", IllogicalExpressionException, "Illogical expression structure"),
        ("Division by Zero", "x = 10 / (5 - 5); x", DivisionByZeroException, "Division by zero is not allowed."),
    ],
)
def test_invalid_equations(title, expression, expected_exception, expected_message):
    eq = Equation(title, expression)
    eq.solve()
    assert eq.result is None
    assert isinstance(eq.error, str)
    assert expected_message in eq.error

