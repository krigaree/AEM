import numpy as np # type: ignore

from solvers.solver import Solver # type: ignore

class Evaluator:

    def __init__(self):
        self.min_val = None
        self.min_solution = None
        self.max_val = None
        self.max_solution = None
        self.mean_val = None

    def evaluate(self, solver: Solver, iterations: int):
        for i in range(iterations):
            s, l = solver.solve(start_idx = i)
            print(l)

if __name__ == '__main__':
    evaluator = Evaluator()
