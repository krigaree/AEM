from typing import List, Tuple

import numpy as np # type: ignore

from solvers.solver import Solver # type: ignore

Solution = List[int]

class Evaluator:

    def __init__(self):
        self.min_val = None
        self.min_solution = None
        self.max_val = None
        self.max_solution = None
        self.mean_val = None

    def evaluate(self, solver: Solver, iterations: int):
        results = []
        for i in range(iterations):
            results.append(solver.solve(start_idx = i))
        results = np.array(results)
        results = results[np.argsort(results[:, 1])]
        self.min_solution = results[0, 0]
        self.min_val = results[0, 1]
        self.max_solution = results[-1, 0]
        self.max_val = results[-1, 1]
        self.mean_val = results[:, 1].mean()

if __name__ == '__main__':
    evaluator = Evaluator()
