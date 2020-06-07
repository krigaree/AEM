import os
import random
import sys
from math import ceil
from time import time
from typing import List, Tuple

import numpy as np

# from .steepest_on_edges import SteepestOnEdges
from .steepest_on_edges_previous_moves import \
    SteepestOnEdgesPreviousMoves as SteepestOnEdges

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.constructive_heuristics.solver import Solver

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
        self.status = [True] * len(self._matrix)
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
        return idx_min[1] + 1, st2idx[idx_min[0]], len_changes[idx_min]

    def repair(self, tour: Tour) -> Solution:
        self.solution = tour
        self.status = [True] * len(self._matrix)
        self.status = np.array(self.status)
        self.status[tour] = False
        self.length = calc_length(tour, self._matrix)

        while len(self.solution) < ceil((len(self.status)) / 2):
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

    def __init__(self, best_solutions) -> None:
        self.solutions = best_solutions

    def random_solution(self, all_vertices):
        return random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices) / 2)))

    def destroy(self, tour, destroy_rate=30):
        destroy_rate = int(destroy_rate)
        sample_size = len(tour) - destroy_rate
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
            max_time: int
    ):
        # tour = Tour(tour)
        """We want to iterate until there is no improvement."""
        ls = SteepestOnEdges()

        # best_tour = tour  # self.random_solution(all_vertices)
        j = 0
        best_tour = self.solutions[j, 0]
        best_tour_length = calc_length(best_tour, matrix)

        self.repairer = GreedyCycleRepairer(matrix)

        iterations = 0
        tours_history = []
        start_time = time()
        end_time = time()
        iterations_from_correction = 0
        best_tours = {}
        destroy_rate = 30
        destroy_decay = 2 - 0.9
        min_destroy_rate = 20
        max_destroy_rate = 70
        while (end_time - start_time) < max_time:
            iterations += 1
            if iterations_from_correction > 500:
                destroy_rate = 30
                print("-" * 20)
                print(f"Starting from new tour")
                best_tours[best_tour_length] = best_tour.copy()
                j += 1
                best_tour = self.solutions[j, 0]
                best_tour_length = calc_length(best_tour, matrix)
                print(f"Length of new tour: {best_tour_length}")
            tours_history.append(best_tour_length)
            new_tour = self.destroy(best_tour, destroy_rate)
            new_tour = self.repair(new_tour)
            # print("num of vert", len(new_tour))

            new_tour = ls.improve(new_tour, matrix, all_vertices)
            new_tour_length = calc_length(new_tour, matrix)
            # print("best_tour_length:", best_tour_length)

            if new_tour_length < best_tour_length:
                best_tour = new_tour
                best_tour_length = new_tour_length
                iterations_from_correction = 0
                destroy_rate += 2.5
                destroy_rate = min(destroy_rate, 70)
                # destroy_rate = min(max_destroy_rate,
                #                    destroy_decay * destroy_rate)
                print("new_tour_length:", new_tour_length)
                print(destroy_rate)
            else:
                iterations_from_correction += 1

            # print('l:', length)
            end_time = time()
        # print(i)
        best_tours[best_tour_length] = best_tour
        min_length = np.min(list(best_tours))
        best_tour = best_tours[min_length]

        return best_tour, iterations, tours_history  # list(tour)
