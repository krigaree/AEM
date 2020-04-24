from copy import deepcopy
from typing import List, Tuple
import numpy as np
import random

Tour = List[int]
Candidate = Tuple[int, int]


class GreedyOnEdges:
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
        new_tour[i:j + 1] = list(reversed(new_tour[i:j + 1]))
        return new_tour

    def find_best_edges_swap(self, tour: Tour, matrix: np.ndarray) -> (float, Candidate):
        shuffled_indices = list(range(0, len(tour) - 1))
        random.shuffle(shuffled_indices)

        for i in range(len(shuffled_indices)):
            for node_j in shuffled_indices[i + 1:]:
                if shuffled_indices[i] != 0 or node_j != len(tour) - 1:
                    pair = sorted([shuffled_indices[i], node_j])
                    first_edges = matrix[tour[pair[0] - 1], tour[pair[0]]] \
                                  + matrix[tour[pair[1]], tour[pair[1] + 1]]
                    second_edges = matrix[tour[pair[0] - 1], tour[pair[1]]] \
                                   + matrix[tour[pair[0]], tour[pair[1] + 1]]
                    new_delta = second_edges - first_edges
                    if new_delta < 0:
                        return new_delta, (pair[0], pair[1])
        return 0, None

    def find_best_node_insert(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour) -> (float, Candidate):
        shuffled_indices = list(range(0, len(tour) - 2))
        random.shuffle(shuffled_indices)
        unused_vertices = list(set(all_vertices) - set(tour))
        random.shuffle(unused_vertices)
        for node_i in shuffled_indices:  # range(0, len(tour) - 2):
            for new_node in unused_vertices:
                old_edges = matrix[tour[node_i - 1], tour[node_i]] \
                            + matrix[tour[node_i], tour[node_i + 1]]
                new_edges = matrix[tour[node_i - 1], new_node] \
                            + matrix[new_node, tour[node_i + 1]]
                new_delta = new_edges - old_edges
                if new_delta < 0:
                    return new_delta, (node_i, new_node)
        return 0, None

    def calc_length(self, tour: Tour, matrix: np.ndarray):
        length = 0
        for i in range(-1, len(tour) - 1):
            length += matrix[tour[i], tour[i + 1]]
        return length

    def improve(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour) -> Tour:
        """We want to iterate until there is no improvement."""
        i = 0
        while True:
            i += 1
            if random.choice((0, 1)) == 1:
                delta, candidate = self.find_best_edges_swap(tour, matrix)
                if delta != 0:
                    tour = self.swap_edges(tour, candidate[0], candidate[1])
                    length = self.calc_length(tour, matrix)
                    # print('l:', length)
                else:
                    delta, candidate = self.find_best_node_insert(tour, matrix, all_vertices)
                    if delta != 0:
                        tour[candidate[0]] = candidate[1]
                        length = self.calc_length(tour, matrix)
                        # print('l:', length)
                    else:
                        return tour
            else:
                delta, candidate = self.find_best_node_insert(tour, matrix, all_vertices)
                if delta != 0:
                    tour[candidate[0]] = candidate[1]
                    length = self.calc_length(tour, matrix)
                    # print('l:', length)
                else:
                    delta, candidate = self.find_best_edges_swap(tour, matrix)
                    if delta != 0:
                        tour = self.swap_edges(tour, candidate[0], candidate[1])
                        length = self.calc_length(tour, matrix)
                        # print('l:', length)
                    else:
                        return tour

        #     if (delta_edge <= delta_node) and delta_edge != 0:
        #         tour = self.swap_edges(tour, candidate_edge[0], candidate_edge[1])
        #         break_flag = True
        #     elif delta_edge > delta_node:
        #         tour[candidate_node[0]] = candidate_node[1]
        #         break_flag = True
        #     length = self.calc_length(tour, matrix)
        #     print('l:', length)
        # print(i)
        # return tour
