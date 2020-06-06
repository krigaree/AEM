import os.path
import random
import sys
from statistics import mean

import numpy as np
from tqdm import tqdm

random.seed(0)

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.utils.loader import Loader
from tsp_router.utils.visualizer import Visualizer

from tsp_router.local_search.steepest_on_edges_destroy_repair_with_restarting import \
    LocalSearchWithLargeScaleNeighbourhood

# from tsp_router.constructive_heuristics.greedy_regret_cycle import \
#     GreedyRegretCycle
from tsp_router.constructive_heuristics.greedy_regret_cycle_with_local_search import \
    GreedyRegretCycle
from tsp_router.utils.evaluator import Evaluator


def random_cluster(matrix):
    random_point = np.random.randint(matrix.shape[0])
    cluster_size = int(np.ceil(matrix.shape[0] / 2))
    random_solution = np.argsort(matrix[random_point])[:cluster_size]
    return random_solution


def best_cycle(matrix, n=20):
    regret_solver = GreedyRegretCycle(matrix)
    evaluator = Evaluator()
    evaluator.evaluate(regret_solver, 200)
    # evaluator.print_metrics()
    return evaluator.solutions[:n]
    # visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)


# def random_solution(matrix):
#     random_solution = random.sample(
#         list(range(matrix.shape[0])), int(np.ceil(len(matrix.shape[0]) / 2)))


def run(path):
    loader = Loader(path)
    vertices = loader.load_vertices()

    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    # solver = LocalSearchWithLargeScaleNeighbourhood()

    all_vertices = np.arange(len(vertices))

    solutions = []
    lengths = []
    times = []

    for i in tqdm(range(10)):
        # random_solution = random_cluster(matrix)
        # best_solutions = best_cycle(matrix)
        best_solutions = best_cycle(matrix, 10)
        solver = LocalSearchWithLargeScaleNeighbourhood(best_solutions)
        improved_solution, n_iterations, lengths_history = solver.solve(
            [], matrix, all_vertices, 360)
        # plt.plot(lengths_history[1000:])
        # plt.show()
        # visualizer.create_graph_euclidean(
        #     improved_solution, matrix, vertices, "wykres.png")
        # print("lengths_history", lengths_history)
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
