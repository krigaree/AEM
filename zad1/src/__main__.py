from evaluator import Evaluator
from loader import Loader
from visualizer import Visualizer
from solvers.greedy_solver import GreedySolver
from solvers.regret_solver import RegretSolver
from solvers.greedy_cycle_solver import GreedyCycleSolver

def main():
    loader = Loader('../data/kroA100.tsp')
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)
    greedy_solver = RegretSolver(matrix)
    evaluator = Evaluator()
    evaluator.evaluate(greedy_solver, 100)
    print(f'Shortest path length: {evaluator.min_val}')
    print(f'Longest path length: {evaluator.max_val}')
    print(f'Mean path length: {evaluator.mean_val}')
    visualizer = Visualizer()
    # visualizer.create_graph(evaluator.min_solution, matrix)
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

if __name__ == '__main__':
    main()
