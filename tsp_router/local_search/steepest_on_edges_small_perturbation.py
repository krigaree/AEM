import random
import time
from copy import deepcopy
from typing import List, Tuple, Dict, Optional
import numpy as np

Tour = List[int]
Candidate = Tuple[int, int]


class SteepestOnEdgesSmallPerturbation:
    """Local search tour improvement algorithm.
    It consider every possible 2-edges swap,
    swapping 2 edges when it results in an improved tour.
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
        node, node_after = edge_i[1], self.tour[edge_i[1]][1]  # next edge
        while True:
            self.tour[node] = self.tour[node][::-1]
            node, node_after = node_after, self.tour[node_after][1]  # next edge
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
        delta = 0
        candidate = None
        while i < len(self.tour) - 1:
            i += 1
            j = 0
            while tmp_first != second_edge:
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

    def local_search(self) -> None:
        break_flag = True  # If new candidate is found don't break loop
        while break_flag:
            break_flag = False
            delta_edge, candidate_edge = self.find_best_edges_swap()
            delta_node, candidate_node = self.find_best_node_insert()

            if (delta_edge <= delta_node) and delta_edge != 0:
                self.swap_edges(candidate_edge[0], candidate_edge[1])
                break_flag = True
            elif delta_edge > delta_node:
                self.swap_nodes(candidate_node[0], candidate_node[1])
                break_flag = True

    def tour_length(self, tour: Optional[Dict[int, List[int]]] = None) -> float:
        if tour is None:
            tour = self.tour
        first = next(iter(tour))
        node = tour[first][1]
        l = self.matrix[tour[node][0], node]
        while node != first:
            l += self.matrix[node, tour[node][1]]
            node = tour[node][1]
        return l

    def perturbation(self, swaps) -> None:
        i = 0
        while i < swaps:
            nodes_to_swap = random.choices(list(self.tour.keys()), k=2)
            if nodes_to_swap[0] != nodes_to_swap[1]:
                i += 1
                first_edge = (nodes_to_swap[0], self.tour[nodes_to_swap[0]][1])
                second_edge = (nodes_to_swap[1], self.tour[nodes_to_swap[1]][1])
                self.swap_edges(first_edge, second_edge)
            node_in_tour_to_swap = random.choices(list(self.tour.keys()), k=1)[0]
            unused_vertices = list(set(self.all_vertices) - set(self.tour))
            node_outside_tour_to_swap = random.choices(unused_vertices, k=1)[0]
            self.swap_nodes(node_in_tour_to_swap, node_outside_tour_to_swap)

    def solve(self, tour: Tour, matrix: np.ndarray,
                all_vertices: Tour, max_time: int) -> Tuple[Tour, int]:
        """We want to iterate until there is no improvement."""
        self.tour = self.convert_tour(tour)
        self.matrix = matrix
        self.all_vertices = all_vertices
        self.local_search()
        l = self.tour_length()
        best_l = l
        swaps = int(0.05 * len(tour))
        best_tour = deepcopy(self.tour)
        input_len = self.tour_length()
        start_time = time.time()
        i = 0
        while True:
            i += 1
            in_tour = deepcopy(self.tour)
            self.perturbation(swaps=swaps)
            self.local_search()
            t = time.time()-start_time
            if t < max_time:
                if self.tour_length() < best_l:
                    best_tour = deepcopy(self.tour)
                    best_l = self.tour_length()
                    # print(best_l)
                else:
                    self.tour = in_tour
            else:
                break
        output_len = self.tour_length(best_tour)
        # print("Improvement:", input_len - output_len)
        return self.invert_tour(best_tour), i
