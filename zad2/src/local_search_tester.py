from loader import Loader
from two_opt import TwoOpt
from two_opt_nodes import TwoOptNodes
from two_opt_nodes_greedy import TwoOptNodesGreedy
from two_opt_greedy import TwoOptGreedy

from solvers.greedy_cycle_solver import GreedyCycleSolver
from solvers.greedy_regret_cycle_solver import GreedyRegretCycleSolver

from visualizer import Visualizer
from tqdm import tqdm
import random
import numpy as np
from statistics import mean
from time import time


def run(path):
    loader = Loader(path)
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    two_opt = TwoOptNodesGreedy()
    all_vertices = np.arange(len(vertices))
    solutions = []
    lengths = []
    times = []
    for i in tqdm(range(100)):
        random_solution = random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices)/2)))
        start = time()
        improved_solution = two_opt.improve(random_solution, matrix, all_vertices)
        end = time()
        times.append(end - start)
        l = 0
        for i in range(-1, len(improved_solution)-1):
            l += matrix[improved_solution[i], improved_solution[i+1]]
        lengths.append(l)
        solutions.append(improved_solution)

    print('min:', min(lengths))
    print('max:', max(lengths))
    print('mean:', mean(lengths))
    print('min_time:', min(times))
    print('max_time:', max(times))
    print('mean_time:', mean(times))
    best_sol = solutions[lengths.index(min(lengths))]
    visualizer.create_graph_euclidean(best_sol, matrix, vertices)


def main():
    # run('../data/kroA100.tsp')
    run('../data/kroB100.tsp')


if __name__ == '__main__':
    main()
