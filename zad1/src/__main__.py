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
    greedy_solver = GreedySolver(matrix)
    greedy_cycle_solver = GreedyCycleSolver(matrix)
    regret_solver = RegretSolver(matrix)
    evaluator = Evaluator()
    visualizer = Visualizer()

    evaluator.evaluate(greedy_solver, 100)
    print('Greedy Solver')
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)
    evaluator.evaluate(greedy_cycle_solver, 100)
    print('\nGreedy Cycle Solver')
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)
    evaluator.evaluate(regret_solver, 100)
    print('\nRegert Solver')
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

if __name__ == '__main__':
    main()
