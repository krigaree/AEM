from evaluator import Evaluator
from loader import Loader
from visualizer import Visualizer
from solvers.greedy_solver import GreedySolver
from solvers.regret_solver import RegretSolver
from solvers.greedy_cycle_solver import GreedyCycleSolver

def run(path):
    print('-'*21)
    print(f"Executing for {path.split('/')[-1].split('.')[0]}")
    print('-'*21)

    loader = Loader(path)
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)

    greedy_cycle_solver = GreedyCycleSolver(matrix)
    regret_solver = RegretSolver(matrix)
    greedy_solver = GreedySolver(matrix)

    evaluator = Evaluator()
    visualizer = Visualizer()

    print('\nGreedy Cycle Solver')
    evaluator.evaluate(greedy_cycle_solver, 100)
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

    print('\nRegret Solver')
    evaluator.evaluate(regret_solver, 100)
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

    print('\nGreedy Solver')
    evaluator.evaluate(greedy_solver, 100)
    evaluator.print_metrics()
    # visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

def main():
    run('../data/kroA100.tsp')
    run('../data/kroB100.tsp')

if __name__ == '__main__':
    main()
