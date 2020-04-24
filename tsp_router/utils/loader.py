from typing import List, Tuple, Dict, Any, Optional
import numpy as np

Vertex = List[float]


class Loader:

    def __init__(self, fname: str):
        self.config: Dict[str, Any] = {}
        self.fname = fname
        self.matrix: Optional[np.ndarray] = None
        self.vertices: List[Vertex] = []

    def load_vertices(self, fname: str = '') -> List[Vertex]:
        if not fname:
            fname = self.fname
        read_config = True
        with open(fname) as f:
            for i, line in enumerate(f):
                if read_config:
                    data = [x.strip() for x in line.split(':')]
                    if len(data) > 1:
                        key, value = data
                    else:
                        read_config = False
                    try:
                        self.config[key] = int(value)
                    except:
                        self.config[key] = value
                else:
                    if i < self.config['DIMENSION']+len(self.config.keys())+1:
                        vertex = [float(v) for v in line.split()[1:]]
                        self.vertices.append(vertex)
        return self.vertices

    def load_matrix(self, fname: str) -> Optional[np.ndarray]:
        with open(fname, 'rb') as f:
            self.matrix = np.load(f)
        return self.matrix

    def save_matrix(self, path: str, matrix: np.ndarray) -> None:
        with open(path, 'wb') as f:
            np.save(f, matrix)

    def calculate_matrix(self, vertices: List[Vertex]) -> np.ndarray:
        vert = np.array(vertices)
        matrix = np.zeros(shape=(len(vert), len(vert)))
        for i in range(1, len(vert)):
            for j in range(i):
                dist = np.round(np.linalg.norm(vert[i]-vert[j]))
                matrix[i, j] = dist
                matrix[j, i] = dist
        self.matrix = matrix
        return self.matrix
