import random
from copy import deepcopy
from typing import List, Optional, Tuple

import numpy as np

Candidate = Tuple[int, int]
Tour = List[int]

check_all = np.zeros((50,50))


class GreedyOnNodes:
    """Local search tour improvement algorithm.
    It consider every possible 2-edges swap,
    swapping 2 edges when it results in an improved tour.
    """

    def __init(self) -> None:
        pass

    def swap_nodes(self, tour: Tour,
                   candidate_i: int, candidate_j: int) -> Tour:
        tmp = tour[candidate_i]
        tour[candidate_i] = tour[candidate_j]
        tour[candidate_j] = tmp
        if candidate_i==0 and candidate_j==len(tour)-2:
            tour[-1] = tour[0]
        return tour

    def find_best_node_in_tour(
            self, tour: Tour, matrix: np.ndarray
    ) -> Tuple[int, Optional[Candidate]]:
        delta = 0
        candidate = None
        shuffled_indices = list(range(len(tour)-2))
        random.shuffle(shuffled_indices)
        check_all = np.zeros((50,50))
        for i, node_ii in enumerate(shuffled_indices):
            shuffled_indices_2 = shuffled_indices[i+1:].copy()
            shuffled_indices_2.append(len(tour)-2)
            for node_jj in shuffled_indices_2:
                node_i, node_j = node_ii, node_jj
                if node_j<node_i:
                    node_i, node_j = node_j, node_i
                check_all[node_i, node_j] += 1
                if node_i==0:
                    node_i_prev = len(tour)-2
                else:
                    node_i_prev = node_i - 1
                if node_j==len(tour)-2:
                    node_j_next = 0
                else:
                    node_j_next = node_j + 1
                if node_i==0 and node_j==len(tour)-2:
                    old_edges = matrix[tour[node_i], tour[node_i+1]] \
                                + matrix[tour[node_j], tour[node_j-1]]
                    new_edges = matrix[tour[node_i], tour[node_j-1]] \
                                + matrix[tour[node_j], tour[node_i+1]]
                elif node_i!=node_j-1:
                    old_edges = matrix[tour[node_i_prev], tour[node_i]] \
                                + matrix[tour[node_i], tour[node_i + 1]] \
                                + matrix[tour[node_j - 1], tour[node_j]] \
                                + matrix[tour[node_j], tour[node_j_next]]
                    new_edges = matrix[tour[node_j], tour[node_i_prev]] \
                                + matrix[tour[node_j], tour[node_i+1]] \
                                + matrix[tour[node_j-1], tour[node_i]] \
                                + matrix[tour[node_i], tour[node_j_next]]
                else:
                    old_edges = matrix[tour[node_i_prev], tour[node_i]] \
                                + matrix[tour[node_j], tour[node_j_next]]
                    new_edges = matrix[tour[node_j], tour[node_i_prev]] \
                                + matrix[tour[node_i], tour[node_j_next]]
                new_delta = new_edges - old_edges
                if new_delta < delta:
                    delta = new_delta
                    candidate = (node_i, node_j)
                    return delta, candidate
        return 0, None

    def find_best_node_insert(
            self, tour: Tour, matrix: np.ndarray, all_vertices: Tour
    ) -> Tuple[int, Optional[Candidate]]:
        shuffled_indices = list(range(0, len(tour) - 2))
        random.shuffle(shuffled_indices)
        unused_vertices = list(set(all_vertices) - set(tour))
        random.shuffle(unused_vertices)
        delta = 0
        candidate = None
        for node_i in shuffled_indices:
            if node_i==0:
                node_i_prev = len(tour)-2
            else:
                node_i_prev = node_i - 1
            for new_node in unused_vertices:
                old_edges = matrix[tour[node_i_prev], tour[node_i]] \
                            + matrix[tour[node_i], tour[node_i + 1]]
                new_edges = matrix[tour[node_i_prev], new_node] \
                            + matrix[new_node, tour[node_i + 1]]
                new_delta = new_edges - old_edges
                if new_delta < delta:
                    delta = new_delta
                    candidate = (node_i, new_node)
                    return delta, candidate
        return 0, None

    def calc_length(self, tour: Tour, matrix: np.ndarray) -> int:
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
                delta, candidate = self.find_best_node_in_tour(tour, matrix)
                if delta != 0:
                    tour = self.swap_nodes(tour, candidate[0], candidate[1])
                    length = self.calc_length(tour, matrix)
                    # print('l:', length)
                else:
                    delta, candidate = self.find_best_node_insert(
                        tour, matrix, all_vertices
                    )
                    if delta != 0:
                        tour[candidate[0]] = candidate[1]
                        length = self.calc_length(tour, matrix)
                        # print('l:', length)
                    else:
                        # print('t', check_all)
                        return tour
            else:
                delta, candidate = self.find_best_node_insert(
                    tour, matrix, all_vertices
                )
                if delta != 0:
                    tour[candidate[0]] = candidate[1]
                    length = self.calc_length(tour, matrix)
                    # print('l:', length)
                else:
                    delta, candidate = self.find_best_node_in_tour(tour, matrix)
                    if delta != 0:
                        tour = self.swap_nodes(tour, candidate[0], candidate[1])
                        length = self.calc_length(tour, matrix)
                        # print('l:', length)
                    else:
                        # print('s', check_all)
                        return tour

