from copy import deepcopy
from typing import List, Tuple, Dict
import numpy as np

Tour = List[int]
Candidate = Tuple[int, int]


class SteepestOnEdges:
    """Local search tour improvement algorithm.
    It consider every possible 2-edges swap,
    swapping 2 edges when it results in an improved tour.
    """

    def __init(self) -> None:
        pass

    def swap_nodes(self, node_i: int, node_j: int) -> None:
        new_tour = deepcopy(self.tour)
        new_tour[node_j] = self.tour[node_i]
        new_tour[self.tour[node_i][0]][1] = node_j
        new_tour[self.tour[node_i][1]][0] = node_j
        del new_tour[node_i]
        self.tour = new_tour

    def swap_edges(self, edge_i: Tuple[int, int],
                   edge_j: Tuple[int, int]) -> None:
        new_tour = deepcopy(self.tour)
        node, node_after = edge_i[1], self.tour[edge_i[1]][1]  # next edge
        while True:
            new_tour[node][0] = self.tour[node][1]  # prev node is next node before
            new_tour[node][1] = self.tour[node][0]  # next node is prev node
            node, node_after = node_after, self.tour[node_after][1]  # next edge
            if node == edge_j[1]:
                break
        new_tour[edge_i[0]][1] = edge_j[0]
        new_tour[edge_i[1]][1] = edge_j[1]
        new_tour[edge_j[0]][0] = edge_i[0]
        new_tour[edge_j[1]][0] = edge_i[1]
        self.tour = new_tour

    def get_next_edge(self, edge: Tuple[int, int]) -> Tuple[int, int]:
        return edge[1], self.tour[edge[1]][1]

    def find_best_edges_swap(self) -> None:
        first_node = next(iter(self.tour))
        first_edge = (first_node, self.tour[first_node][1])
        second_edge = self.get_next_edge(first_edge)
        i = 0
        delta = 0
        candidate = None
        while i < len(self.tour) - 1:
            i += 1
            j = 0
            while first_edge != second_edge:
                j += 1
                sum_old_edges = self.matrix[first_edge] + \
                                self.matrix[second_edge]
                new_edge_i = (self.tour[first_edge[0]][1],
                              self.tour[second_edge[0]][1])
                new_edge_j = (self.tour[first_edge[1]][0],
                              self.tour[second_edge[1]][0])
                sum_new_edges = self.matrix[new_edge_i] + \
                                self.matrix[new_edge_j]
                new_delta = sum_new_edges - sum_old_edges
                if new_delta < 0 and new_delta < delta:
                    delta = new_delta
                    candidate = (first_edge, second_edge)
                second_edge = self.get_next_edge(second_edge)
            first_edge = self.get_next_edge(first_edge)
            second_edge = self.get_next_edge(first_edge)
        return delta, candidate

    def find_best_node_insert(self):
        unused_vertices = list(set(self.all_vertices) - set(self.tour))
        delta = 0
        candidate = None
        for node, (before, after) in self.tour.items():
            for new_node in unused_vertices:
                first_edge = (before, node)
                second_edge = (node, after)
                new_fist_edge = (before, new_node)
                new_second_edge = (new_node, after)
                old_edges = self.matrix[first_edge] + self.matrix[
                    second_edge]
                new_edges = self.matrix[new_fist_edge] + self.matrix[
                    new_second_edge]
                new_delta = new_edges - old_edges
                if new_delta < 0 and new_delta < delta:
                    delta = new_delta
                    candidate = (node, new_node)
        return delta, candidate

    @staticmethod
    def convert_tour(tour: Tour) -> Dict[int, List[int]]:
        new_tour = {}
        for i in range(len(tour)):
            # Edge = (node_before, node_after)
            new_tour[tour[i - 1]] = [tour[i - 2], tour[i]]
        return new_tour

    @staticmethod
    def invert_tour(tour: Dict[int, List[int]]) -> Tour:
        first = next(iter(tour))
        new_tour = [first]
        node = tour[first][1]
        while node != first:
            new_tour.append(node)
            node = tour[node][1]
        return new_tour

    def improve(self, tour: Tour, matrix: np.ndarray, all_vertices: Tour) -> Tour:
        """We want to iterate until there is no improvement."""
        break_flag = True  # If new candidate is found don't break loop
        self.tour = self.convert_tour(tour)
        self.matrix = matrix
        self.all_vertices = all_vertices
        i = 0
        while break_flag:
            i += 1
            break_flag = False
            delta_edge, candidate_edge = self.find_best_edges_swap()
            delta_node, candidate_node = self.find_best_node_insert()

            if (delta_edge <= delta_node) and delta_edge != 0:
                self.swap_edges(candidate_edge[0], candidate_edge[1])
                break_flag = True
            elif delta_edge > delta_node:
                self.swap_nodes(candidate_node[0], candidate_node[1])
                break_flag = True
        return self.invert_tour(self.tour)
