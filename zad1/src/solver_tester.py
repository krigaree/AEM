from typing import List, Tuple
from evaluator import Evaluator
from loader import Loader
from visualizer import Visualizer
from solvers.greedy_cycle_solver import GreedyCycleSolver # type: ignore
from solvers.regret_solver import RegretSolver # type: ignore

Solution = List[int]

def main():
    loader = Loader('../data/kroA100.tsp')
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)
    greedy_solver = GreedyCycleSolver(matrix)
    for i in range(1):
        s, l = greedy_solver.solve(99)
        print(s)
        visualizer = Visualizer()
        visualizer.create_graph_euclidean(s, matrix, vertices)

if __name__ == '__main__':
    main()