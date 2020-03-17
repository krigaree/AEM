from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

Solution = List[int]

class Solver(ABC):

    @abstractmethod
    def __init__(self, matrix: np.ndarray):
        self._matrix = matrix
        self._solutions: List[Solution] = []
        self._lengths: List[int] = []
        super().__init__()

    @abstractmethod
    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        pass
