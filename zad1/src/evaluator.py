from typing import List, Optional
import numpy as np
from solvers.solver import Solver

Solution = List[int]

class Evaluator:

    def __init__(self):
        self.min_val: Optional[float] = None
        self.min_solution: Optional[List[int]] = None
        self.max_val: Optional[float] = None
        self.max_solution: Optional[List[int]] = None
        self.mean_val: Optional[float] = None

    def evaluate(self, solver: Solver, iterations: int) -> None:
        results = []
        for i in range(iterations):
            results.append(solver.solve(start_idx = i))
        solutions = np.array(results)
        solutions = solutions[np.argsort(solutions[:, 1])]
        self.min_solution = solutions[0, 0]
        self.min_val = solutions[0, 1]
        self.max_solution = solutions[-1, 0]
        self.max_val = solutions[-1, 1]
        self.mean_val = solutions[:, 1].mean()

    def print_metrics(self) -> None:
        print(f'Shortest path length: {self.min_val}')
        print(f'Longest path length: {self.max_val}')
        print(f'Mean path length: {self.mean_val}')
