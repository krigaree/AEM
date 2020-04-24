from typing import List, Union
import numpy as np
import matplotlib.pyplot as plt
# import networkx as nx

Solution = List[int]
Vertex = List[int]


class Visualizer:

    def __init__(self):
        self.graph = None
        self.graph_image = None

    def create_graph(self, solution: Solution, matrix: np.ndarray) -> None:
        rows, cols = np.where(matrix > 0)
        points_a = solution.copy()[:-1]
        points_b = solution.copy()[1:]
        edges = zip(points_a, points_b)
        gr = nx.Graph()
        gr.add_edges_from(edges)
        nx.draw(gr, node_size=100)
        plt.show()

    def create_graph_euclidean(
            self, solution: Solution, matrix: np.ndarray,
            vertices: Union[np.ndarray, List[Vertex]]
    ) -> None:

        vertices = np.array(vertices)
        plt.plot(vertices[:, 0], vertices[:, 1], "o")
        points_a = solution.copy()
        points_b = np.concatenate([solution.copy()[1:], solution[:1]])
        points_a = vertices[points_a]
        points_b = vertices[points_b]
        for a, b in zip(points_a, points_b):
            plt.plot([a[0], b[0]], [a[1], b[1]], '-')
        for n in range(len(vertices)):
            plt.annotate(str(n), (vertices[n, 0], vertices[n, 1]))
        plt.savefig("wykres.png")
        plt.show()

    def save_graph(self, graph=None) -> None:
        raise NotImplementedError
