from loader import Loader
from two_opt import TwoOpt
from two_opt_nodes import TwoOptNodes
from two_opt_greedy import TwoOptGreedy
from visualizer import Visualizer
from solvers.greedy_nn_solver import GreedyNNSolver
from solvers.greedy_cycle_solver import GreedyCycleSolver

import numpy as np


def run(path):
    print('-'*21)
    print(f"Executing for {path.split('/')[-1].split('.')[0]}")
    print('-'*21)

    loader = Loader(path)
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)

    visualizer = Visualizer()

    all_vertices = np.arange(len(vertices))
    random_solution = all_vertices[:int(np.ceil(len(all_vertices)/2))]
    l = 0
    for i in range(-1, len(random_solution)-1):
        l += matrix[random_solution[i], random_solution[i+1]]
    print('Before', l)
    visualizer.create_graph_euclidean(random_solution, matrix, vertices)

    s = GreedyNNSolver(matrix)
    sol, l = s.solve(0)
    print('solll:', l)
    visualizer.create_graph_euclidean(sol, matrix, vertices)

    two_opt = TwoOpt()
    improved_solution = two_opt.improve(sol, matrix, all_vertices)
    # improved_solution = two_opt.improve(random_solution, matrix, all_vertices)
    print(f'improved: {improved_solution}')
    l = 0
    for i in range(-1, len(improved_solution)-1):
        l += matrix[improved_solution[i], improved_solution[i+1]]
    print('After', l)
    visualizer.create_graph_euclidean(improved_solution, matrix, vertices)



def main():
    run('../data/kroA100.tsp')
    # run('../data/kroB100.tsp')


if __name__ == '__main__':
    main()
