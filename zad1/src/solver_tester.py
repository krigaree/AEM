from typing import List, Tuple
from evaluator import Evaluator
from loader import Loader
from visualizer import Visualizer
from solvers.greedy_cycle_solver import GreedyCycleSolver # type: ignore

Solution = List[int]

if __name__ == '__main__':
    loader = Loader('../data/kroA100.tsp')
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)
    greedy_solver = GreedyCycleSolver(matrix)
    for _ in range(100):
        s, l = greedy_solver.solve(0)
    visualizer = Visualizer()
    visualizer.create_graph_euclidean(s, matrix, vertices)