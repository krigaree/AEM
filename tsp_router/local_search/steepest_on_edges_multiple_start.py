from copy import deepcopy
from typing import List, Tuple
import random
import numpy as np

Tour = List[int]
Candidate = Tuple[int, int]


class SteepestOnEdgesMultipleStart:
    """Local search tour improvement algorithm.
    It consider every possible 2-edges swap,
    swapping 2 edges when it results in an improved tour.
    """

    def __init(self) -> None:
        pass

    def swap_edges(self, tour: Tour, i: int, j: int) -> Tour:
        """It take tour like [1,2,3,4,5,6] and indices 2 and 4
        and reverse sub_tour [3,4,5] between those two indices.
        Returned tour is [1,2,5,4,3,6]"""
        new_tour = deepcopy(tour)
        if i < j:
            new_tour[i:j + 1] = list(reversed(new_tour[i:j + 1]))
        else:
            new_tour[j:i + 1] = list(reversed(new_tour[j:i + 1]))
        return new_tour

    def find_best_edges_swap(
            self,
            tour: Tour,
            matrix: np.ndarray
    ) -> (float, Candidate):
        delta = 0
        candidate = None
        for node_i in range(0, len(tour) - 1):
            for node_j in range(node_i+1, len(tour) - 1):
                first_edges = matrix[tour[node_i - 1], tour[node_i]] \
                              + matrix[tour[node_j], tour[node_j + 1]]
                second_edges = matrix[tour[node_i - 1], tour[node_j]] \
                            + matrix[tour[node_i], tour[node_j + 1]]
                new_delta = second_edges - first_edges
                if new_delta < 0:
                    if node_i < 1 or new_delta < delta:
                        delta: int = new_delta
                        candidate = (node_i, node_j)
        return delta, candidate

    def find_best_node_insert(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour) -> (float, Candidate):
        unused_vertices = list(set(all_vertices) - set(tour))
        delta = 0
        candidate = None
        for node_i in range(0, len(tour) - 1):
            for new_node in unused_vertices:
                old_edges = matrix[tour[node_i - 1], tour[node_i]] \
                            + matrix[tour[node_i], tour[node_i + 1]]
                new_edges = matrix[tour[node_i - 1], new_node] \
                            + matrix[new_node, tour[node_i + 1]]
                new_delta = new_edges - old_edges
                if new_delta < delta:
                    delta: int = new_delta
                    candidate = (node_i, new_node)
        return delta, candidate

    def calc_length(self, tour: Tour, matrix: np.ndarray):
        length = 0
        for i in range(-1, len(tour) - 1):
            length += matrix[tour[i], tour[i + 1]]
        return length

    def single_search(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour
                      ) -> List:
        """We want to iterate until there is no improvement."""
        break_flag = True  # If new candidate is found don't break loop

        i = 0
        while break_flag:
            i += 1
            break_flag = False
            delta_edge, candidate_edge = self.find_best_edges_swap(
                tour, matrix)
            delta_node, candidate_node = self.find_best_node_insert(
                tour, matrix, all_vertices)

            if (delta_edge <= delta_node) and delta_edge != 0:
                tour = self.swap_edges(
                    tour, candidate_edge[0], candidate_edge[1])
                break_flag = True
            elif delta_edge > delta_node:
                tour[candidate_node[0]] = candidate_node[1]
                break_flag = True
            # l = self.calc_length(tour, matrix)
            # print('l:', length)
            # print(i)
        return tour  # list(tour)

    def random_solution(self, all_vertices):
        return random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices) / 2)))

    def improve(self, empty_parameter, matrix: np.ndarray, all_vertices: Tour,
                empty_parameter2 : int
                ) -> List:
        """We want to iterate until there is no improvement."""
        break_flag = True  # If new candidate is found don't break loop

        best_tour = self.random_solution(all_vertices)
        best_length = self.calc_length(best_tour, matrix)

        for _ in range(100):
            random_tour = self.random_solution(all_vertices)
            new_tour = self.single_search(random_tour, matrix, all_vertices)
            new_length = self.calc_length(new_tour, matrix)
            if new_length < best_length:
                best_tour = new_tour
                best_length = new_length

        return best_tour
