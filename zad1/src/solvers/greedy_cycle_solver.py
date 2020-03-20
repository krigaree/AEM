from typing import List, Tuple
import numpy as np
from math import ceil

from solvers.solver import Solver

Solution = List[int]

class GreedyCycleSolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        status = [True]*len(self._matrix)
        solution = [start_idx]
        length = 0
        # append first node
        x = self._matrix[start_idx]
        status[start_idx] = False
        st2idx = np.where(status)[0]
        solution.append(st2idx[np.argmin(x[st2idx])])
        status[solution[1]] = False
        st2idx = np.where(status)[0]

        # append next nodes
        np_matrix = np.array(self._matrix)

        for _ in range(ceil((len(status))/2)-2):
            len_changes = []
            vertices_idx = []
            for i in range(len(solution)):
                edge_length = np_matrix[solution[i-1], solution[i]]
                new_edges_lengths = np.sum(
                    np_matrix[np.ix_(st2idx, [solution[i-1], solution[i]])],
                    axis=1
                    )
                best_vertex_idx = np.argmin(new_edges_lengths)
                len_changes.append(
                    new_edges_lengths[best_vertex_idx] - edge_length)
                vertices_idx.append(st2idx[best_vertex_idx])
            idx_min = np.argmin(len_changes)
            solution.insert(idx_min, vertices_idx[idx_min])

            status[solution[idx_min]] = False
            st2idx = np.where(status)[0]

        return solution, length
