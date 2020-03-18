from typing import List, Tuple

import numpy as np

from solvers.solver import Solver

Solution = List[int]

class Evaluator:

    def __init__(self):
        self._min_val = None
        self._min_solution = None
        self._max_val = None
        self._max_solution = None
        self._mean_val = None

    def evaluate(self, solver: Solver, iterations: int) -> None:
        results = []
        for i in range(iterations):
            results.append(solver.solve(start_idx = i))
        solutions = np.array(results)
        solutions = solutions[np.argsort(solutions[:, 1])]
        self._min_solution = solutions[0, 0]
        self._min_val = solutions[0, 1]
        self._max_solution = solutions[-1, 0]
        self._max_val = solutions[-1, 1]
        self._mean_val = solutions[:, 1].mean()

    def print_metrics(self) -> None:
        print(f'Shortest path length: {self._min_val}')
        print(f'Longest path length: {self._max_val}')
        print(f'Mean path length: {self._mean_val}')
