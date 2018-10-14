# encoding: utf-8
import queue
from search_algorithm import SearchAlgorithm
from utils import manhattan_distance

class AStar(SearchAlgorithm):
    """
    Clase para realizar la búsqueda óptima utilizando
    el método A*.
    """
    def __init__(self, grid, start, goal):
        super(AStar, self).__init__(grid, start, goal)
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.f_score = [[]]
    
    def execute_search(parameter_list):
        """
        Corre el algoritmo A* sobre la cuadrícula
        para encontrar el objetivo.
        """
        self.color[self.start[0]][self.start[1]] =\
            'GRAY'
        self.distance[self.start[0]][self.start[1]] = 0
        self.parent[self.start[0]][self.start[1]] = None
        self.open_list.append((0, self.start))
        while not self.open_list.empty():
            current_square = min(self.open_list)
            self.open_list.remove(current_square)
            current_square = current_square[1]
            up_square = self.move_up(current_square)
            down_square = self.move_down(current_square)
            right_square = self.move_to_the_right(current_square)
            left_square = self.move_to_the_left(current_square)
            successors = [up_square, down_square, right_square, left_square]

            for successor in successors:
                if successor:
                    if successor == self.goal:




