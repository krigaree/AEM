from typing import List, Tuple
import numpy as np
from math import ceil

from solvers.solver import Solver

Solution = List[int]

class RegretSolver(Solver):

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
        return idx_min[1]+1, st2idx[idx_min[0]], len_changes[idx_min]

    def find_alternative_vertex(self, replaced_idx) -> None:
        # print('-'*70)
        tmp_status = []
        tmp_status = self.status.copy()
        # print(tmp_status)
        if replaced_idx >= len(self.solution):
            tmp_status[self.solution[-1]] = True
            tmp_status[self.solution[0]] = True
        else:
            tmp_status[self.solution[replaced_idx-1]] = True
            tmp_status[self.solution[replaced_idx]] = True
        st2idx = np.where(np.logical_not(tmp_status))[0]
        # print(f'st2idx: {st2idx}')
        edges_zipped = zip(
            self.solution,
            [self.solution[-1]] + self.solution,
            self.solution[1:] + [self.solution[0]]
        )
        edges = np.array(list(map(np.array, edges_zipped)))
        # print(f'Edges before deletion: {edges}')
        edges = np.delete(edges, [replaced_idx-1], axis=0)
        if replaced_idx >= len(self.solution):
            edges = edges[1:-1]
        edges = np.delete(edges, [replaced_idx-1, replaced_idx], axis=0)
        # print(f'Edges after deletion: {edges}')
        # tmp_mat = np.array(
        #     [
        #         self._matrix[edges[:, 0], edges[:, 1]],
        #         self._matrix[edges[:, 0], edges[:, 2]]
        #     ]
        # )
        # print(f'tmp_mat_print: \n{tmp_mat}')
        added_lengths = np.sum(
            [
                self._matrix[edges[:, 0], edges[:, 1]],
                self._matrix[edges[:, 0], edges[:, 2]]
            ],
            axis=0
        )
        # print(f'added_lengths: {added_lengths}')
        edges_lengths = np.array(
            self._matrix[edges[:, 1], edges[:, 2]]
        )
        # print(f'edges_lengths: {edges_lengths}')
        len_changes = added_lengths - edges_lengths
        # print(f'len_changes: {len_changes}')
        # idx_min = np.unravel_index(
        #     np.argmin(len_changes, axis=None),
        #     len_changes.shape
        # )
        idx_min = np.argmin(len_changes)
        vertex = edges[idx_min, 0]
        # self.length += len_changes[idx_min]
        return idx_min, vertex, len_changes[idx_min]

    def solve(self, start_idx: int = 0) -> Tuple[Solution, int]:
        self.insert_first_nodes(start_idx)

        position, vertex_idx, len_change = self.find_next_vertex()
        self.insert_node(position, vertex_idx)
        position, vertex_idx, len_change = self.find_next_vertex()
        self.insert_node(position, vertex_idx)

        for _ in range(ceil((len(self.status))/2)-2):
            position, vertex_idx, len_change = self.find_next_vertex()
            # print(f'self.solution{self.solution}')
            # print(f'position: {position}')
            pos2, v_idx2, len_change_del = self.find_alternative_vertex(position)

            self.insert_node(position, vertex_idx)

        return self.solution, self.length
