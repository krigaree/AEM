from math import ceil
from typing import List, Tuple

import numpy as np
from tqdm.auto import tqdm

from solvers.solver import Solver

Solution = List[int]

class GreedyCycleSolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        # Array for storing information about unused nodes
        status = [True]*len(self._matrix)
        # Array for storing ordered idices of used nodes
        solution = [start_idx]
        length = 0
        # append first node
        x = self._matrix[start_idx] # Vector of distances from first node
        status[start_idx] = False
        st2idx = np.where(status)[0] # Indices of unused nodes
        solution.append(st2idx[np.argmin(x[st2idx])]) # Take nearest node
        status[solution[1]] = False
        dist_node = {(solution[0], solution[1]):
                     np.sum(self._matrix[solution], axis=0)\
                     -self._matrix[solution[0], solution[1]],
                     (solution[1], solution[0]):
                     np.sum(self._matrix[solution], axis=0)\
                     -self._matrix[solution[1], solution[0]]}

        for j in range(ceil((len(status))/2)-2): # 50% without 2 first nodes
            mask = np.array(status).reshape(1,-1).repeat(j+2,axis=0).flatten()
            mask2idx = np.where(mask)[0].flatten()
            dist_mat = np.array(list(dist_node.values())).flatten()

            best_edge = mask2idx[np.argsort(dist_mat[mask2idx])][0]
            vert_idx = best_edge%100
            idx_min = (best_edge-vert_idx)//100
            idx_min_f, idx_min_l = list(dist_node.keys())[idx_min]
            idx_min = solution.index(idx_min_f)

            solution.insert(idx_min+1, vert_idx)
            status[solution[idx_min+1]] = False

            f = solution[idx_min%len(solution)]
            m = solution[(idx_min+1)%len(solution)]
            l = solution[(idx_min+2)%len(solution)]

            del dist_node[(f,l)]
            dist_node[(f,m)] = np.sum(self._matrix[[f,m]], axis=0)\
                -self._matrix[f,m]
            dist_node[(m,l)] = np.sum(self._matrix[[m,l]], axis=0)\
                -self._matrix[m,l]

        return solution, length
