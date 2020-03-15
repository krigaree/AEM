import numpy as np # type: ignore

Solution = List[int]

class Visualizer:

    def __init__(self):
        self.graph = None
        self.graph_image = None

    def create_graph(self, solution: Solution, matrix: np.ndarray) -> None:
        pass
    def save_graph(self, graph=None) -> None:
        pass
