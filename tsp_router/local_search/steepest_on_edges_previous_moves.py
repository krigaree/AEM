from collections import OrderedDict
from copy import deepcopy
from typing import List, Tuple, Dict, Union, Set

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
        self.tour[self.tour[node_i][0]][1] = node_j
        self.tour[self.tour[node_i][1]][0] = node_j
        self.tour[node_j] = self.tour[node_i].copy()
        del self.tour[node_i]

    def swap_edges(self, edge_i: Tuple[int, int],
                   edge_j: Tuple[int, int]) -> None:
        if not self.check_direction_in_tour(edge_i):
            edge_i = edge_i[::-1]
            edge_j = edge_j[::-1]
        node, node_after = edge_i[1], self.tour[edge_i[1]][1]
        while True:
            self.tour[node] = self.tour[node][::-1]
            node, node_after = node_after, self.tour[node_after][1]
            if node == edge_j[1]:
                break
        self.tour[edge_i[0]][1] = edge_j[0]
        self.tour[edge_i[1]][1] = edge_j[1]
        self.tour[edge_j[0]][0] = edge_i[0]
        self.tour[edge_j[1]][0] = edge_i[1]

    def get_next_edge(self, edge: Tuple[int, int]) -> Tuple[int, int]:
        return edge[1], self.tour[edge[1]][1]

    def find_best_edges_swap(self) -> None:
        first_node = next(iter(self.tour))
        first_edge = (first_node, self.tour[first_node][1])
        tmp_first = first_edge
        second_edge = self.get_next_edge(first_edge)
        i = 0
        while i < len(self.tour) - 1:
            i += 1
            j = 0
            while tmp_first != second_edge:
                j += 1
                if ((first_edge, second_edge) not in self.edge_used_moves and
                        (second_edge, first_edge) not in self.edge_used_moves):
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
                    self.edge_used_moves.add((first_edge, second_edge))
                second_edge = self.get_next_edge(second_edge)
            first_edge = self.get_next_edge(first_edge)
            second_edge = self.get_next_edge(first_edge)

    def find_best_node_insert(self) -> None:
        unused_vertices = list(set(self.all_vertices) - set(self.tour))
        for node, (before, after) in self.tour.items():
            for new_node in unused_vertices:
                first_edge = (before, node)
                second_edge = (node, after)
                new_fist_edge = (before, new_node)
                new_second_edge = (new_node, after)
                if (((before, after), (node, new_node)) not in self.node_used_moves and
                        ((before, after), (new_node, node)) not in self.node_used_moves and
                        ((after, before), (node, new_node)) not in self.node_used_moves and
                        ((after, before), (new_node, node)) not in self.node_used_moves):
                    old_edges = self.matrix[first_edge] + self.matrix[
                        second_edge]
                    new_edges = self.matrix[new_fist_edge] + self.matrix[
                        new_second_edge]
                    delta = new_edges - old_edges
                    if delta < 0:
                        self.candidates[(node, new_node)] = delta
                    self.node_used_moves.add(((before, after), (node, new_node)))

    @staticmethod
    def convert_tour(tour: Tour) -> Dict[int, List[int]]:
        new_tour = {}
        for i in range(len(tour)):
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

    def check_edge_in_tour(self, edge) -> bool:
        return (edge[0] in self.tour and self.tour[edge[0]][1] == edge[1]) \
            or (edge[1] in self.tour and self.tour[edge[1]][1] == edge[0])

    def check_direction_in_tour(self, edge) -> bool:
        return self.tour[edge[0]][1] == edge[1]

    def improve(self, tour: Tour, matrix: np.ndarray,
                all_vertices: Tour) -> Tour:
        self.tour = self.convert_tour(tour)
        self.matrix = matrix
        self.all_vertices = all_vertices
        break_flag = True
        i = 0
        self.candidates: Dict[Union[Tuple[Tuple[int, int], Tuple[int, int]], Tuple[int, int]], float] = {}
        self.edge_used_moves: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
        self.node_used_moves: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
        while break_flag:
            i += 1
            break_flag = False
            self.find_best_edges_swap()
            self.find_best_node_insert()
            ordered_candidates = OrderedDict(
                sorted(self.candidates.items(), key=lambda t: t[1]))
            for candidate in ordered_candidates:
                if type(candidate[0]) is tuple:
                    if self.check_edge_in_tour(candidate[0]) \
                            and self.check_edge_in_tour(candidate[1]):
                        if not (self.check_direction_in_tour(candidate[0]) \
                                ^ self.check_direction_in_tour(candidate[1])):
                                self.swap_edges(candidate[0], candidate[1])  # type: ignore
                                break_flag = True
                                self.candidates.pop(candidate)
                    else:
                        self.candidates.pop(candidate)
                else:
                    if candidate[0] in self.tour and candidate[1] not in self.tour:
                        self.swap_nodes(candidate[0], candidate[1])  # type: ignore
                        break_flag = True
                        self.candidates.pop(candidate)
                    else:
                        self.candidates.pop(candidate)
        return self.invert_tour(self.tour)
