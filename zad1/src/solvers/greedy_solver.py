from typing import List, Tuple

import numpy as np

from math import ceil

from solvers.solver import Solver

Solution = List[int]

class GreedySolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        status = [True]*len(self._matrix)
        solution = [start_idx]
        length = 0
        for i in range(ceil((len(status)-1)/2)):
            x = self._matrix[solution[-1]]
            status[solution[-1]] = False
            st2idx = np.where(status)[0]
            solution.append(st2idx[np.argsort(x[st2idx])][0])
            length += x[solution[-1]]
        length += self._matrix[solution[0],solution[-1]]
        return solution, length
