from typing import List
from .models import Equation

class ApplicationState:
    def __init__(self):
        self.equations: List[Equation] = []
        self.last_result = {"title": None, "equation": None, "result": None, "error": None}

    def add_equation(self, title: str, equation: str):
        self.equations.append(Equation(title, equation))

    def delete_equation(self, index: int):
        if 0 <= index < len(self.equations):
            self.equations.pop(index)
        else:
            raise IndexError("Invalid equation index.")

    def solve_equation(self, index: int):
        if 0 <= index < len(self.equations):
            equation_obj = self.equations[index]
            equation_obj.solve()
            self.last_result = {
                "title": equation_obj.title,
                "equation": equation_obj.expression,
                "result": equation_obj.result,
                "error": equation_obj.error,
            }
        else:
            raise IndexError("Invalid equation index.")
