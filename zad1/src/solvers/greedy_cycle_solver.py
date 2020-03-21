from math import ceil
from typing import Dict, List, Tuple

import numpy as np
from tqdm.auto import tqdm

from solvers.solver import Solver

Solution = List[int]

class GreedyCycleSolver(Solver):

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)

    def insert_node(self, idx: int, vert_idx: int) -> None:
        self.solution.insert(idx, vert_idx)
        self.status[vert_idx] = False

    def nearest_vertex(self, idx: int) -> int:
        x = self._matrix[idx] # Vector of distances from first node
        st2idx = np.where(self.status)[0] # Indices of unused nodes
        n_idx = st2idx[np.argmin(x[st2idx])] # Take nearest node
        return n_idx

    def initialize(self, f_idx: int) -> None:
        # Array for storing ordered idices of used nodes
        self.solution: Solution = []
        # Array for storing information about unused nodes
        self.status = [True]*len(self._matrix)
        # append first node
        self.insert_node(0, f_idx)
        # Nearest vertex from first vertex
        s_idx = self.nearest_vertex(f_idx)
        # append second node
        self.insert_node(1, s_idx)
        self.dist_node = {(f_idx, s_idx):
                          np.sum(self._matrix[self.solution], axis=0)\
                          -self._matrix[f_idx, s_idx],
                          (s_idx, f_idx):
                          np.sum(self._matrix[self.solution], axis=0)\
                          -self._matrix[s_idx, f_idx]}

    def min_with_mask(self, i: int) -> Tuple[int, int, int]:
        dist_mat = np.array(list(self.dist_node.values()))
        subset_idx = np.argmin(dist_mat[:,self.status])
        indices = np.arange((i+2)*100).reshape(dist_mat.shape)
        best_edge = indices[:,self.status].flatten()[subset_idx]
        vert_idx = best_edge%100
        idx_min = (best_edge-vert_idx)//100
        idx_min_f, idx_min_l = list(self.dist_node.keys())[idx_min]
        return idx_min_f, idx_min_l, vert_idx

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        self.initialize(start_idx)

        for i in range(ceil((len(self.status))/2)-2): # 50% without 2 first nodes
            idx_min_f, idx_min_l, vert_idx = self.min_with_mask(i)
            idx_min = self.solution.index(idx_min_f)

            self.insert_node(idx_min+1, vert_idx)

            f = self.solution[idx_min%len(self.solution)]
            m = self.solution[(idx_min+1)%len(self.solution)]
            l = self.solution[(idx_min+2)%len(self.solution)]

            del self.dist_node[(f,l)]
            self.dist_node[(f,m)] = np.sum(self._matrix[[f,m]], axis=0)\
                -self._matrix[f,m]
            self.dist_node[(m,l)] = np.sum(self._matrix[[m,l]], axis=0)\
                -self._matrix[m,l]

        length = sum([self._matrix[indices] for indices in list(self.dist_node.keys())])

        return self.solution, length
