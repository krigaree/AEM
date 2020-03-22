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
        length = 0

        # insert first node
        solution = [start_idx]
        status[start_idx] = False

        # insert second node
        x = self._matrix[start_idx]
        st2idx = np.where(status)[0]
        solution.append(st2idx[np.argmin(x[st2idx])])
        status[solution[1]] = False
        st2idx = np.where(status)[0]

        # insert next nodes
        np_matrix = np.array(self._matrix)

        for _ in range(ceil((len(status))/2)-2):
            edges = np.array(
                list(
                    map(
                        np.array,
                        zip(solution[:], solution[1:] + [solution[0]])
                    )
                )
            )
            added_lengths = np.sum(
                [
                    np_matrix[np.ix_(st2idx, edges[:, 0])],
                    np_matrix[np.ix_(st2idx, edges[:, 1])]
                ],
                axis=0
            )

            len_changes = added_lengths \
                - np.tile(np_matrix[edges[:, 0], edges[:, 1]], (added_lengths.shape[0], 1))
            idx_min = np.unravel_index(
                np.argmin(len_changes, axis=None),
                len_changes.shape
            )
            solution.insert(idx_min[1]+1, st2idx[idx_min[0]])
            status[solution[idx_min[1]+1]] = False
            st2idx = np.where(status)[0]

        return solution, length
