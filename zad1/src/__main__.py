from evaluator import Evaluator
from loader import Loader
from visualizer import Visualizer
from solvers.greedy_solver import GreedySolver # type: ignore
from solvers.regret_solver import RegretSolver # type: ignore

def main():
    loader = Loader('../data/kroA100.tsp')
    vertices = loader.load_vertices()
    matrix = loader.calculate_matrix(vertices)
    print(matrix[:10,:10])
    greedy_solver = GreedySolver(matrix)
    evaluator = Evaluator()
    evaluator.evaluate(greedy_solver, 10)
    print(f'Shortest path length: {evaluator.min_val}')
    print(f'Longest path length: {evaluator.max_val}')
    print(f'Mean path length: {evaluator.mean_val}')
    visualizer = Visualizer()
    visualizer.create_graph(evaluator.min_solution, matrix)

if __name__ == '__main__':
    main()
