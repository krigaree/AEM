from collections import OrderedDict
from copy import deepcopy
from typing import List, Tuple, Dict

import numpy as np

Tour = List[int]
Candidate = Tuple[int, int]


class SteepestOnEdgesPreviousMoves:
    """Local search tour improvement algorithm. It considers every
    possible 2-edges swap and caches them if it results in an improved tour.
    Then the best move is chosen if possible.
    """

    def __init(self) -> None:
        pass

    def swap_nodes(self, node_i: int, node_j: int) -> None:
        new_tour = deepcopy(self.tour)
        new_tour[node_j] = self.tour[node_i]
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
        while i < len(self.tour) - 1:
            i += 1
            j = 0
            while first_edge != second_edge:
                j += 1
                if (first_edge, second_edge) not in self.edge_used_moves:
                    sum_old_edges = self.matrix[first_edge] + \
                                    self.matrix[second_edge]
                    new_edge_i = (self.tour[first_edge[0]][1],
                                  self.tour[second_edge[0]][1])
                    new_edge_j = (self.tour[first_edge[1]][0],
                                  self.tour[second_edge[1]][0])
                    sum_new_edges = self.matrix[new_edge_i] + \
                                    self.matrix[new_edge_j]
                    delta = sum_new_edges - sum_old_edges
                    if delta < 0:
                        self.candidates[(first_edge, second_edge)] = delta
                second_edge = self.get_next_edge(second_edge)
            first_edge = self.get_next_edge(first_edge)
            second_edge = self.get_next_edge(first_edge)

    def find_best_node_insert(self):
        unused_vertices = list(set(self.all_vertices) - set(self.tour))
        for node, (before, after) in self.tour.items():
            for new_node in unused_vertices:
                first_edge = (before, node)
                second_edge = (node, after)
                new_fist_edge = (before, new_node)
                new_second_edge = (new_node, after)
                if (first_edge, second_edge) not in self.node_used_moves:
                    old_edges = self.matrix[first_edge] + self.matrix[
                        second_edge]
                    new_edges = self.matrix[new_fist_edge] + self.matrix[
                        new_second_edge]
                    delta = new_edges - old_edges
                    if delta < 0:
                        self.candidates[(node, new_node)] = delta

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
        new_tour = [next(iter(tour))]
        node = tour[first][1]
        while node != first:
            new_tour.append(node)
            node = tour[node][1]
        return new_tour

    def improve(self, tour: Tour, matrix: np.ndarray,
                all_vertices: Tour) -> Tour:
        """We want to iterate until there is no improvement."""
        self.tour = self.convert_tour(tour)
        self.matrix = matrix
        self.all_vertices = all_vertices
        break_flag = True  # If new candidate is found don't break loop
        i = 0
        self.candidates = {}
        self.edge_used_moves = set()
        self.node_used_moves = set()
        while break_flag:
            i += 1
            break_flag = False
            self.find_best_edges_swap()
            self.edge_used_moves = self.edge_used_moves | set(
                self.candidates.keys())
            ordered_candidates = OrderedDict(
                sorted(self.candidates.items(), key=lambda t: t[1]))
            for candidate in ordered_candidates:
                # Candidate is an edge
                if type(candidate[0]) is tuple:
                    if candidate[0][0] in self.tour \
                            and self.tour[candidate[0][0]][1] == candidate[0][1] \
                            and candidate[1][0] in self.tour \
                            and self.tour[candidate[1][0]][1] == candidate[1][
                        1]:
                        self.swap_edges(candidate[0], candidate[1])
                        break_flag = True
                        self.candidates.pop(candidate)
                        break
                else:
                    if candidate[0] in tour:
                        self.swap_nodes(candidate[0], candidate[1])
                        break_flag = True
                        self.candidates.pop(candidate)
                        break

        return self.invert_tour(self.tour)
