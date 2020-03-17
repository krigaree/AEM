from typing import List
import numpy as np # type: ignore
import matplotlib.pyplot as plt
import networkx as nx

Solution = List[int]

class Visualizer:

    def __init__(self):
        self.graph = None
        self.graph_image = None

    def create_graph(self, solution: Solution, matrix: np.ndarray) -> None:
        rows, cols = np.where(matrix > 0)

        pointsA = solution.copy()
        pointsB = solution.copy()
        del pointsA[0]
        del pointsB[-1]
        print(pointsA, pointsB)

        edges = zip(pointsA, pointsB)
        gr = nx.Graph()
        gr.add_edges_from(edges)
        nx.draw(gr, node_size=100)
        plt.show()

        # background = Image.new('RGB', (900, 900), (255, 255, 255))
        # draw = ImageDraw.Draw(background)
        # for point in 
        # draw.ellipse((20, 20, 80, 80), fill = 'blue', outline ='blue')
        # del draw
        # background.show()

    def save_graph(self, graph=None) -> None:
        pass
