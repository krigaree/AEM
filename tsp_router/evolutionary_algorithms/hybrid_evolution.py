import os
from copy import deepcopy
from typing import List, Tuple, Dict
import random

from tsp_router.tour import Tour

random.seed(0)
import numpy as np
np.random.seed(0)
from time import time

from tsp_router.local_search.steepest_on_edges import SteepestOnEdges
from tsp_router.utils.loader import Loader

Candidate = Tuple[int, int]


class HybridEvolution:

    def __init__(self, matrix: np.ndarray):
        self.local_search = SteepestOnEdges()
        self.matrix = matrix
        self.all_vertices = list(range(self.matrix.shape[0]))

    def solve(self, max_time: int) -> Tuple[List[int], int]:
        pop = self.generate_population(population_size=20)
        start_time = time()
        i = 0
        while max_time > (time() - start_time):
            parent1, parent2 = self.draw_parents(pop)
            child_solution = self.recombine(parent1, parent2)
            child_solution = self.local_search.improve(
                parent1, self.matrix, self.all_vertices)
            # if self.check_if_improves():
            #     self.replace_worst(pop, child_solution)
            self.replace_if_improves(pop, child_solution)
            i += 1
        return self.find_best_solution(pop), i

    def generate_population(self, population_size) -> List[List[int]]:
        population = []
        while len(population) < population_size:
            random_solution = random.sample(
                self.all_vertices, int(np.ceil(len(self.all_vertices) / 2)))
            if random_solution not in population:
                population.append(random_solution)
        return population

    def draw_parents(self, population) -> Tuple[List[int], List[int]]:
        rand_choices = random.sample(range(len(population)), 2)
        return population[rand_choices[0]], population[rand_choices[1]]

    def recombine(self, parent1, parent2):
        parent1 = Tour.convert_tour(parent1)
        parent2 = Tour.convert_tour(parent2)
        sub_tours = []
        while parent1 and parent2:
            print(len(parent1), len(parent2))
            sub_tour = []
            for k1, v1 in parent1.items():
                if not sub_tour:
                    for k2, v2 in parent2.items():
                        print(k1, k2)
                        if k1 == k2:
                            sub_tour.append(k1)
                            print(k1)
                            prev1, next1 = parent1[k1]
                            prev2, next2 = parent2[k1]
                            break
                else:
                    break
            if sub_tour:
                while True:
                    in_len = len(sub_tour)
                    print("TU:", sub_tour)
                    if prev1 == prev2:
                        if prev1 not in sub_tour:
                            sub_tour.insert(0, prev1)
                            prev1, prev2 = parent1[prev1][0], parent2[prev1][0]
                    if next1 == next2:
                        if next1 not in sub_tour:
                            sub_tour.append(next1)
                            next1, next2 = parent1[next1][1], parent2[next1][1]
                    if len(sub_tour) == in_len:
                        break
                print(sub_tour)
                for s in sub_tour:
                    del parent1[s]
                    del parent2[s]
                sub_tours.append(sub_tour)
                # break
            else:
                for k1 in parent1:
                    sub_tours.append([k1])
                for k2 in parent2:
                    sub_tours.append([k2])
                parent1, parent2 = {}, {}
                break

        print(parent1, parent2)
        print("SUB TOURS:", sub_tours)

    def replace_if_improves(self, population, solution):
        lengths = np.array([self.calc_length(sol) for sol in population])
        new_length = self.calc_length(solution)
        max_idx = np.argmax(lengths)
        if (new_length < lengths[max_idx]) and (solution not in population):
            population[max_idx] == solution

    def find_best_solution(self, population):
        lengths = np.array([self.calc_length(sol) for sol in population])
        min_idx = np.argmin(lengths)
        return population[min_idx]

    def calc_length(self, solution):
        length = 0
        for i in range(len(solution)):
            length += self.matrix[solution[i-1], solution[i]]
        return length


if __name__ == "__main__":
    loader = Loader("../../data/kroA200.tsp")
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)
    solver = HybridEvolution(matrix)
    sol = solver.solve(10)
    print("sol: ", sol)
    print("len: ", len)
