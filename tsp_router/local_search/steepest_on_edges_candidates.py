from copy import deepcopy
from typing import List, Tuple
import numpy as np
# from ..tour import Tour

Tour = List[int]
Candidate = Tuple[int, int]


class SteepestOnEdges:
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

    def get_closest_nodes(self, idx, mat, node_id, n_nodes=10):
        # idx = np.where(np.isin(mat[node_id], mat[node_id, tour[:-2]]))[0]
        return idx[np.argsort(mat[node_id, idx])][:n_nodes]


    def find_best_edges_swap(
            self,
            tour: Tour,
            matrix: np.ndarray,
            # closest_nodes: np.ndarray
    ) -> (float, Candidate):
        delta = 0
        candidate = None
        # cond = np.zeros(matrix.shape[1]) == 1
        # cond[tour[:-1]] = True
        # idx = np.where(cond)[0]
        for node_i in range(0, len(tour) - 1):
            # closest_nds = self.get_closest_nodes(idx, matrix, tour[node_i])
            for node_j in range(node_i+1, len(tour) - 1): # closest_nds:
                # node_j = tour.index(node_j)
                # if node_j <= node_i:
                #     continue
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

    def find_best_insert_candidates(
            self,
            tour: Tour,
            matrix: np.ndarray,
            closest_nodes: np.ndarray
    ) -> (float, Candidate):
        delta = 0
        candidate = None
        for node_i in range(0, len(tour) - 1):
            # print(node_i)
            for node_j in closest_nodes[node_i]:
                if node_j <= node_i:
                    continue
                # print(node_j)
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
        cond = np.zeros(matrix.shape[1]) == 0
        cond[tour] = False
        idx = np.where(cond)[0]
        for node_i in range(0, len(tour) - 1):
            closest_nds = self.get_closest_nodes(idx, matrix, tour[node_i])
            for new_node in closest_nds:  # unused_vertices:
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

    # def find_closest_nodes(
    #         self,
    #         matrix: np.ndarray,
    #         tour,
    #         number_of_nodes: int = 50
    # ) -> np.ndarray:
    #     sorted_matrix = matrix[:, tour[:-1]].argsort()[:, :number_of_nodes]
    #     return sorted_matrix

    def improve(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour) -> \
            List:
        # tour = Tour(tour)
        """We want to iterate until there is no improvement."""
        break_flag = True  # If new candidate is found don't break loop

        # closest_nodes = self.find_closest_nodes(matrix, tour)
        i = 0
        while break_flag:
            i += 1
            break_flag = False
            delta_edge, candidate_edge = self.find_best_edges_swap(
                tour, matrix)
            delta_node, candidate_node = self.find_best_node_insert(
                tour, matrix, all_vertices)

            if (delta_edge <= delta_node) and delta_edge != 0:
                # print(candidate_edge)
                tour = self.swap_edges(
                    tour, candidate_edge[0], candidate_edge[1])
                break_flag = True
            elif delta_edge > delta_node:
                tour[candidate_node[0]] = candidate_node[1]
                # closest_nodes = self.find_closest_nodes(matrix, tour)
                break_flag = True
            # length = self.calc_length(tour, matrix)
            # print('l:', length)
        # print(i)
        return tour  # list(tour)
