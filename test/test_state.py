import pytest
from core.state import ApplicationState


@pytest.fixture
def app_state():
    return ApplicationState()


def test_add_equation(app_state):
    title = "Equation 1"
    expression = "1 + 1"

    app_state.add_equation(title, expression)

    assert len(app_state.equations) == 1
    assert app_state.equations[0].title == title
    assert app_state.equations[0].expression == expression


def test_delete_equation(app_state):
    app_state.add_equation("Equation 1", "1 + 1")
    app_state.add_equation("Equation 2", "2 * 2")

    app_state.delete_equation(0)

    assert len(app_state.equations) == 1
    assert app_state.equations[0].title == "Equation 2"


def test_delete_equation_invalid_index(app_state):
    app_state.add_equation("Equation 1", "1 + 1")

    with pytest.raises(IndexError, match="Invalid equation index."):
        app_state.delete_equation(5)  # Invalid index


def test_solve_equation(app_state):
    app_state.add_equation("Equation 1", "1 + 1")

    eq = app_state.equations[0]
    eq.solve()

    app_state.solve_equation(0)

    assert app_state.last_result["title"] == eq.title
    assert app_state.last_result["equation"] == eq.expression
    assert app_state.last_result["result"] == eq.result
    assert app_state.last_result["error"] == eq.error


def test_solve_equation_invalid_index(app_state):
    app_state.add_equation("Equation 1", "1 + 1")

    with pytest.raises(IndexError, match="Invalid equation index."):
        app_state.solve_equation(5)
