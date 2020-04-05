from loader import Loader
from two_opt import TwoOpt
from two_opt_nodes import TwoOptNodes
from two_opt_greedy import TwoOptGreedy

from visualizer import Visualizer
from tqdm import tqdm
import random
import numpy as np
from statistics import mean


def run(path):
    loader = Loader(path)
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    all_vertices = np.arange(len(vertices))
    solutions = []
    lengths = []
    for _ in tqdm(range(100)):
        random_solution = random.sample(
            list(all_vertices), int(np.ceil(len(all_vertices)/2)))

        # visualizer.create_graph_euclidean(random_solution, matrix, vertices)

        two_opt = TwoOptGreedy()
        improved_solution = two_opt.improve(random_solution, matrix, all_vertices)
        l = 0
        for i in range(-1, len(improved_solution)-1):
            l += matrix[improved_solution[i], improved_solution[i+1]]
        lengths.append(l)
        solutions.append(improved_solution)

    print('min:', min(lengths))
    print('max:', max(lengths))
    print('mean:', mean(lengths))
    # visualizer.create_graph_euclidean(improved_solution, matrix, vertices)


def main():
    run('../data/kroA100.tsp')
    # run('../data/kroB100.tsp')


if __name__ == '__main__':
    main()
