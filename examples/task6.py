import sys
import os.path
from tqdm import tqdm
import numpy as np
from statistics import mean
from time import time
import random
from matplotlib import pyplot as plt

random.seed(0)

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.utils.loader import Loader
from tsp_router.utils.visualizer import Visualizer

from tsp_router.local_search.steepest_on_edges_multiple_start import \
    SteepestOnEdgesMultipleStart
from tsp_router.local_search.steepest_on_edges_small_perturbation import \
    SteepestOnEdgesSmallPerturbation
from tsp_router.local_search.steepest_on_edges_destroy_repair import \
    LocalSearchWithLargeScaleNeighbourhood
from tsp_router.evolutionary_algorithms.hybrid_evolution import HybridEvolution


def random_cluster(matrix):
    random_point = np.random.randint(matrix.shape[0])
    cluster_size = int(np.ceil(matrix.shape[0] / 2))
    random_solution = np.argsort(matrix[random_point])[:cluster_size]
    return random_solution


# def random_solution(matrix):
#     random_solution = random.sample(
#         list(range(matrix.shape[0])), int(np.ceil(len(matrix.shape[0]) / 2)))


def run(path):
    loader = Loader(path)
    vertices = loader.load_vertices()

    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    solver = LocalSearchWithLargeScaleNeighbourhood()

    all_vertices = np.arange(len(vertices))

    solutions = []
    lengths = []
    times = []

    for i in tqdm(range(60)):
        random_solution = random_cluster(matrix)
        improved_solution, n_iterations, lengths_history = solver.solve(
            random_solution, matrix, all_vertices, 360)
        # plt.plot(lengths_history[1000:])
        # plt.show()
        # visualizer.create_graph_euclidean(
        #     improved_solution, matrix, vertices, "wykres.png")
        print("lengths_history", lengths_history)
        print("llll", len(improved_solution))
        print("improved_solution", improved_solution)
        print("unique", len(np.unique(np.array(improved_solution))))
        print("n_iterations:", n_iterations)

        times.append(n_iterations)
        l = 0
        for i in range(-1, len(improved_solution) - 1):
            l += matrix[improved_solution[i], improved_solution[i + 1]]
        lengths.append(l)
        print("l:", l)
        solutions.append(improved_solution)

    print("file:", path)
    print('min:', min(lengths))
    print('max:', max(lengths))
    print('mean:', mean(lengths))
    print('min_time:', min(times))
    print('max_time:', max(times))
    print('mean_time:', mean(times))
    best_sol = solutions[lengths.index(min(lengths))]
    visualizer.create_graph_euclidean(best_sol, matrix, vertices, "wykres.png")
    print("algo:", solver.__class__)


def main():
    # run('../data/kroA200.tsp')
    run('../data/kroA200.tsp')
    # run_all_algorithms('../data/kroA200.tsp')


if __name__ == '__main__':
    main()
