from typing import List, Tuple
import numpy as np
from math import ceil

from solvers.solver import Solver

Solution = List[int]

class GreedyCycleSolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def insert_node(self, position: int, vert_idx: int) -> None:
        self.solution.insert(position, vert_idx)
        self.status[vert_idx] = False

    def insert_first_nodes(self, first_idx: int) -> None:
        # Array for storing ordered idices of used nodes
        self.solution: Solution = []
        # Array for storing information about unused nodes
        self.status = [True]*len(self._matrix)
        self.insert_node(0, first_idx)
        second_idx = self.find_nearest_vertex(first_idx)
        self.insert_node(1, second_idx)
        self.length = 0

    def find_nearest_vertex(self, idx: int) -> int:
        # Vector of distances from first node
        x = self._matrix[idx] 
        # Indices of unused nodes
        st2idx = np.where(self.status)[0]
        vert_idx = st2idx[np.argmin(x[st2idx])]
        return vert_idx

    def find_next_vertex(self) -> None:
        st2idx = np.where(self.status)[0]
        edges_zipped = zip(
            self.solution, self.solution[1:] + [self.solution[0]])
        edges = np.array(list(map(np.array, edges_zipped)))
        added_lengths = np.sum(
            [
                self._matrix[np.ix_(st2idx, edges[:, 0])],
                self._matrix[np.ix_(st2idx, edges[:, 1])]
            ],
            axis=0
        )
        edges_lengths = np.tile(
            self._matrix[edges[:, 0], edges[:, 1]],
            (added_lengths.shape[0], 1)
        )
        len_changes = added_lengths - edges_lengths
        idx_min = np.unravel_index(
            np.argmin(len_changes, axis=None),
            len_changes.shape
        )
        self.length += len_changes[idx_min]
        return idx_min[1]+1, st2idx[idx_min[0]]

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        self.insert_first_nodes(start_idx)

        for _ in range(ceil((len(self.status))/2)-2):
            position, vertex_idx = self.find_next_vertex()
            self.insert_node(position, vertex_idx)

        return self.solution, self.length
