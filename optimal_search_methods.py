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
        self.open_list = PriorityQueue()
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
        self.open_list.put((0, self.start))
        self.f_score[self.start[0]][self.start[1]] =\
            manhattan_distance(self.start, self.goal)
    
        while not self.open_list.empty():
            current_square = self.open_list.get()
            current_square_coordinates =\
                current_square[1]
            if current_square_coordinates == self.goal:
                break
            if self.parent[current_square_coordinates[0]][current_square_coordinates[1]]:
                current_path = self.get_path(current_square_coordinates)
                path += current_path
                path += self.get_reverse_path(current_path)
            up_square = self.move_up(current_square_coordinates)
            left_square = self.move_to_the_left(current_square_coordinates)
            right_square = self.move_to_the_right(current_square_coordinates)
            down_square = self.move_down(current_square_coordinates)

            successors = [up_square, left_square, right_square, down_square]
            
            for successor in successors:
                if successor:
                    f = self.distance[successor[0]][successor[1]] +\
                        manhattan_distance(successor, self.goal)
                    if self.f_score[successor[0]][successor[1]] >= f:
                        self.f_score[successor[0]][successor[1]] = f
                        self.open_list.put((f, successor))
        return path



