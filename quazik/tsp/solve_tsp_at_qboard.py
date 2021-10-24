from tsp.models import Marker, Distance
from quazik.settings import QBOARD_PARAMS

from typing import List
from copy import deepcopy
import numpy as np
from qboard import Solver


class SolveTSPAtQBoard:
    def __init__(self, markers: List[Marker], distances: List[Distance], fine1=10, fine2=10, solver_name='gurobi'):
        self.markers = deepcopy(markers)
        self.distances = deepcopy(distances)

        self.marker_to_number = {marker: number for number, marker in enumerate(self.markers)}
        self.number_to_marker = {value: key for key, value in self.marker_to_number.items()}
        self.fine1 = fine1
        self.fine2 = fine2
        self.solver_name = solver_name

        self.number_markers = len(self.markers)

        self.adjacency_matrix = np.zeros((self.number_markers, self.number_markers))
        for distance in distances:
            origin = distance.origin
            destination = distance.destination

            self.adjacency_matrix[self.marker_to_number[origin], self.marker_to_number[destination]] = distance.distance

        self.adjacency_matrix /= np.max(self.adjacency_matrix)

        self.Q = np.zeros((self.number_markers ** 2, self.number_markers ** 2))
        for j in range(self.number_markers):
            for i in range(self.number_markers):
                for k in range(self.number_markers):
                    self.Q[self.number_markers * i + j,
                           self.number_markers * k + ((j + 1) % self.number_markers)] += self.adjacency_matrix[i, k]

        for j in range(self.number_markers + 1):
            for i in range(self.number_markers):
                self.Q[self.number_markers * i + (j % self.number_markers),
                       self.number_markers * i + (j % self.number_markers)] -= self.fine1
                for k in range(i + 1, self.number_markers):
                    self.Q[self.number_markers * i + (j % self.number_markers),
                           self.number_markers * k + (j % self.number_markers)] += 2 * self.fine1

        for i in range(self.number_markers):
            for j in range(self.number_markers + 1):
                self.Q[self.number_markers * i + (j % self.number_markers),
                       self.number_markers * i + (j % self.number_markers)] -= self.fine2
                for k in range(j + 1, self.number_markers + 1):
                    self.Q[self.number_markers * i + (j % self.number_markers),
                           self.number_markers * i + (k % self.number_markers)] += 2 * self.fine2

    def get_best_path(self, solver_name=None) -> List[Marker]:
        solver_name = solver_name if solver_name is not None else self.solver_name
        solver = Solver(mode=f"remote:{solver_name}", params=QBOARD_PARAMS)

        x, energy = solver.solve_qubo(self.Q, timeout=30)
        x = np.array(x).reshape((self.number_markers, self.number_markers))

        path = []
        for j in range(self.number_markers + 1):
            for i in range(self.number_markers):
                if x[i, j % self.number_markers] == 1:
                    path.append(self.number_to_marker[i])

        return path
