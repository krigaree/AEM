from typing import List, Tuple
import numpy as np
from .steepest_on_edges import SteepestOnEdges
from time import time
import random
import sys
import os
from math import ceil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.constructive_heuristics.solver import Solver
from tsp_router.constructive_heuristics.greedy_cycle import GreedyCycle


Tour = List[int]
Candidate = Tuple[int, int]
Solution = List[int]


def calc_length(tour: Tour, matrix: np.ndarray):
    length = 0
    for i in range(-1, len(tour) - 1):
        length += matrix[tour[i], tour[i + 1]]
    return length


class GreedyCycleRepairer(Solver):

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
        self.length = 2 * (self._matrix[first_idx, second_idx])

    def find_nearest_vertex(self, idx: int) -> int:
        # Vector of distances from first node
        x = self._matrix[idx]
        # Indices of unused nodes
        st2idx = np.where(self.status)[0]
        vert_idx = st2idx[np.argmin(x[st2idx])]
        return vert_idx

    def find_next_vertex(self):
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
        return idx_min[1]+1, st2idx[idx_min[0]], len_changes[idx_min]

    def repair(self, tour: Tour) -> Solution:
        self.solution = tour
        self.status = [True] * len(self._matrix)
        self.status = np.array(self.status)
        self.status[tour] = False
        self.length = calc_length(tour, self._matrix)

        while len(self.solution) < ceil((len(self.status))/2):
            position, vertex_idx, _ = self.find_next_vertex()
            self.insert_node(position, vertex_idx)
        # for _ in range(ceil((len(self.status))/2)-2):

        return self.solution

    def solve(self):
        pass


class LocalSearchWithLargeScaleNeighbourhood:
    """Local search tour improvement algorithm.
    It consider every possible 2-edges swap,
    swapping 2 edges when it results in an improved tour.
    """

    def __init(self) -> None:
        pass

    def random_solution(self, all_vertices):
        return random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices) / 2)))

    def destroy(self, tour, n_to_delete=30):
        sample_size = len(tour) - n_to_delete
        sorted_sample = [
            tour[i] for i in
            sorted(random.sample(range(len(tour)), sample_size))
        ]
        return sorted_sample

    def repair(self, tour):
        return self.repairer.repair(tour)

    def solve(
            self,
            tour,
            matrix: np.ndarray,
            all_vertices: Tour,
            max_time: float
    ) -> Tuple[List, int]:
        # tour = Tour(tour)
        """We want to iterate until there is no improvement."""
        ls = SteepestOnEdges()

        best_tour = tour  # self.random_solution(all_vertices)
        best_tour_length = calc_length(best_tour, matrix)

        self.repairer = GreedyCycleRepairer(matrix)

        iterations = 0
        start_time = time()
        end_time = time()
        while (end_time - start_time) < max_time:
            iterations += 1

            new_tour = self.destroy(best_tour)
            new_tour = self.repair(new_tour)
            # print("num of vert", len(new_tour))

            new_tour = ls.improve(new_tour, matrix, all_vertices)
            new_tour_length = calc_length(new_tour, matrix)
            # print("best_tour_length:", best_tour_length)
            # print("new_tour_length:", new_tour_length)

            if new_tour_length < best_tour_length:
                best_tour = new_tour
                best_tour_length = new_tour_length

            # print('l:', length)
            end_time = time()
        # print(i)
        return best_tour, iterations  # list(tour)
