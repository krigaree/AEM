from typing import List, Tuple

import numpy as np # type: ignore

from solvers.solver import Solver

Solution = List[int]

class RegretSolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        raise NotImplementedError
