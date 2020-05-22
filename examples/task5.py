import sys
import os.path
from tqdm import tqdm
import numpy as np
from statistics import mean
from time import time
import random

random.seed(0)

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.utils.evaluator import Evaluator
from tsp_router.utils.loader import Loader
from tsp_router.utils.visualizer import Visualizer

from tsp_router.local_search.steepest_on_edges_multiple_start import \
    SteepestOnEdgesMultipleStart
from tsp_router.local_search.steepest_on_edges_small_perturbation import \
    SteepestOnEdgesSmallPerturbation
from tsp_router.local_search.steepest_on_edges_destroy_repair import \
    LocalSearchWithLargeScaleNeighbourhood
from tsp_router.evolutionary_algorithms.hybrid_evolution import HybridEvolution


def run(path):
    loader = Loader(path)
    vertices = loader.load_vertices()

    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    # ms = SteepestOnEdgesMultipleStart()
    # sp = SteepestOnEdgesSmallPerturbation()
    # ln = LocalSearchWithLargeScaleNeighbourhood()
    he = HybridEvolution()
    solver = he

    all_vertices = np.arange(len(vertices))
    solutions = []
    lengths = []
    times = []

    for i in tqdm(range(5)):
        random_solution = random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices) / 2)))
        start = time()
        improved_solution, n_iterations = solver.solve(
            random_solution, matrix, all_vertices, 120)
        print("llll", len(improved_solution))
        print("improved_solution", improved_solution)
        print("unique", len(np.unique(np.array(improved_solution))))
        print("n_iterations:", n_iterations)
        end = time()

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


def run_all_algorithms(path):
    print("RUN ALL")
    algos = [
        SteepestOnEdgesMultipleStart,
        SteepestOnEdgesSmallPerturbation,
        LocalSearchWithLargeScaleNeighbourhood,
        HybridEvolution
    ]
    algos = [algos[2]]
    for ls_algoritm in algos:
        loader = Loader(path)
        vertices = loader.load_vertices()

        matrix = loader.calculate_matrix(vertices)

        visualizer = Visualizer()

        alg = ls_algoritm()

        all_vertices = np.arange(len(vertices))
        solutions = []
        lengths = []
        times = []

        for i in tqdm(range(10)):
            random_solution = random.sample(
                list(all_vertices), int(np.ceil(len(all_vertices) / 2)))
            start = time()
            # improved_solution = two_opt.improve(random_solution, matrix, all_vertices)
            # improved_solution = two_opt.improve(matrix, all_vertices, 100)
            improved_solution, n_iterations = alg.solve(
                random_solution, matrix, all_vertices, 360)
            # print("llll", len(improved_solution))
            # print("improved_solution", improved_solution)
            print("unique", len(np.unique(np.array(improved_solution))))
            print("n_iterations:", n_iterations)
            end = time()

            times.append(n_iterations)
            l = 0
            for i in range(-1, len(improved_solution) - 1):
                l += matrix[improved_solution[i], improved_solution[i + 1]]
            print("l:", l)
            lengths.append(l)
            solutions.append(improved_solution)

        print("file:", path)
        print("algo:", alg.__class__)
        print('min:', min(lengths))
        print('max:', max(lengths))
        print('mean:', mean(lengths))
        print('min_time:', min(times))
        print('max_time:', max(times))
        print('mean_time:', mean(times))
        best_sol = solutions[lengths.index(min(lengths))]
        visualizer.create_graph_euclidean(
            best_sol, matrix, vertices, str(alg.__class__) + ".png")


def main():
    # run('../data/kroA200.tsp')
    run('../data/kroA200.tsp')
    # run_all_algorithms('../data/kroA200.tsp')


if __name__ == '__main__':
    main()
