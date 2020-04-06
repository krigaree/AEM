import sys
import os.path
from tqdm import tqdm
import random
import numpy as np
from statistics import mean
from time import time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.utils.evaluator import Evaluator
from tsp_router.utils.loader import Loader
from tsp_router.utils.visualizer import Visualizer

from tsp_router.local_search.two_opt import TwoOpt
from tsp_router.local_search.two_opt_nodes import TwoOptNodes
from tsp_router.local_search.two_opt_nodes_greedy import TwoOptNodesGreedy
from tsp_router.local_search.two_opt_greedy import TwoOptGreedy


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
    run('../data/kroA100.tsp')
    # run('../../data/kroB100.tsp')


if __name__ == '__main__':
    main()
