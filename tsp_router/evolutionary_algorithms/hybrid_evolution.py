from typing import List, Tuple
import random
import numpy as np
from time import time

from ..local_search.steepest_on_edges import SteepestOnEdges

Tour = List[int]
Candidate = Tuple[int, int]


class HybridEvolution:

    def __init__(self, matrix: np.ndarray):
        self.local_search = SteepestOnEdges()
        self.matrix = matrix
        self.all_vertices = list(range(self.matrix.shape[0]))

    def solve(self, max_time: int) -> Tuple[int, Tour]:
        pop = self.generate_population(population_size=20)
        start_time = time()
        while max_time > (time() - start_time):
            parent1, parent2 = self.draw_parents(pop)
            child_solution = self.recombine(parent1, parent2)
            child_solution = self.local_search.improve(
                child_solution, self.matrix, self.all_vertices)
            if self.check_if_improves():
                self.replace_worst(pop, child_solution)

        return self.find_best_solution()

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

    def recombine(self):
        pass

    def check_if_improves(self):
        pass

    def replace_worst(self):
        pass

    def find_best_solution(self):
        pass
