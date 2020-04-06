import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tsp_router.utils.evaluator import Evaluator
from tsp_router.utils.loader import Loader
from tsp_router.utils.visualizer import Visualizer
from tsp_router.constructive_heuristics.greedy_nn import GreedyNN
from tsp_router.constructive_heuristics.greedy_regret_cycle import GreedyRegretCycle
from tsp_router.constructive_heuristics.greedy_cycle import GreedyCycle

def run(path):
    print('-'*21)
    print(f"Executing for {path.split('/')[-1].split('.')[0]}")
    print('-'*21)

    loader = Loader(path)
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)

    cycle_solver = GreedyCycle(matrix)
    regret_solver = GreedyRegretCycle(matrix)
    nn_solver = GreedyNN(matrix)

    evaluator = Evaluator()
    visualizer = Visualizer()

    print('\nGreedy Cycle Solver')
    evaluator.evaluate(cycle_solver, 100)
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

    print('\nGreedy Cycle Regret Solver')
    evaluator.evaluate(regret_solver, 100)
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)

    print('\nGreedy NN Solver')
    evaluator.evaluate(nn_solver, 100)
    evaluator.print_metrics()
    visualizer.create_graph_euclidean(evaluator.min_solution, matrix, vertices)


def main():
    run('../data/kroA100.tsp')
    run('../data/kroB100.tsp')


if __name__ == '__main__':
    main()
