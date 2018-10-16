# encoding: utf-8
from queue import PriorityQueue
from math import inf
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
        self.f_score = [[inf] * self.grid_size for i\
            in range(self.grid_size)]
    
    def execute_search(self):
        """
        Corre el algoritmo A* sobre la cuadrícula
        para encontrar el objetivo.
        """
        path = []
        self.color[self.start[0]][self.start[1]] =\
            'GRAY'
        self.distance[self.start[0]][self.start[1]] = 0
        self.parent[self.start[0]][self.start[1]] = None
        self.open_list.append((0, self.start))
        self.f_score[self.start[0]][self.start[1]] =\
            manhattan_distance(self.start, self.goal)
    
        while self.open_list:
            current_square = min(self.open_list)
            current_square_coordinates =\
                current_square[1]
            if current_square_coordinates == self.goal:
                return path
            if self.parent[current_square_coordinates[0]][current_square_coordinates[1]]:
                current_path = self.get_path(current_square_coordinates)
                path += current_path
                path += self.get_reverse_path(current_path)
            self.open_list.remove(current_square)
            self.closed_list.append(current_square)
            print(current_square_coordinates)
            print(self.parent[current_square[1][0]][current_square[1][1]])
            up_square = self.move_up(current_square_coordinates)
            down_square = self.move_down(current_square_coordinates)
            right_square = self.move_to_the_right(current_square_coordinates)
            left_square = self.move_to_the_left(current_square_coordinates)

            successors = [up_square, down_square, right_square, left_square]
            
            for successor in successors:
                if not successor or successor in\
                    self.closed_list:
                    continue
                if successor not in self.open_list:
                    f = self.distance[successor[0]][successor[1]] +\
                        manhattan_distance(successor, self.goal)
                    self.open_list.append((f, successor))
                



