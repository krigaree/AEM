from copy import deepcopy
from typing import List
import numpy as np

Tour = List[int]


class TwoOpt:
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

    def improve(self, tour: Tour, matrix: np.ndarray,
                all_vertices: Tour) -> Tour:
        """We want to iterate until there is no improvement."""
        break_flag = True  # If new candidate is found dont break loop
        i = 0
        while break_flag:
            i += 1
            break_flag = False
            delta_edges = 0
            for node_i in range(0, len(tour) - 1):
                for node_j in range(node_i, len(tour) - 1):
                    if node_i != 0 or node_j != len(tour) - 1:
                        first_edges = matrix[tour[node_i - 1], tour[node_i]] \
                                      + matrix[tour[node_j], tour[node_j + 1]]
                        second_edges = matrix[tour[node_i - 1], tour[node_j]] \
                                       + matrix[tour[node_i], tour[node_j + 1]]
                        new_delta = second_edges - first_edges
                        if new_delta < 0:
                            if node_i < 1 or new_delta < delta_edges:
                                delta_edges: int = new_delta
                                candidate_edge = (node_i, node_j)
                                break_flag = True
            unused_vertices = list(set(all_vertices) - set(tour))
            delta_node = 0
            for node_i in range(0, len(tour) - 2):
                for new_node in unused_vertices:
                    old_edges = matrix[tour[node_i - 1], tour[node_i]] \
                               + matrix[tour[node_i], tour[node_i + 1]]
                    new_edges = matrix[tour[node_i - 1], new_node] \
                                + matrix[new_node, tour[node_i + 1]]
                    new_delta = new_edges - old_edges
                    if new_delta < delta_node:
                        delta_node: int = new_delta
                        candidate_node = (node_i, new_node)
                        break_flag = True
            if delta_edges < delta_node:
                tour = self.swap_edges(tour, candidate_edge[0], candidate_edge[1])
            elif delta_edges > delta_node:
                tour[candidate_node[0]] = candidate_node[1]
            l = 0
            for i in range(-1, len(tour) - 1):
                l += matrix[tour[i], tour[i + 1]]
            print('l:', l)
        print(i)
        return tour
