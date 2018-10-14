# encoding: utf-8
import queue
from search_algorithm import SearchAlgorithm
from utils import manhattan_distance


class BestFS(SearchAlgorithm):
    """
    Clase para realizar la búsqueda primero
    el mejor basado utilizando como 
    heurística la distancia Manhattan.
    Es una subclase de SearchAlgorithm.
    """

    def __init__(self, grid, start, goal):
        super(BestFS, self).__init__(grid, start, goal)
        self.my_bests = queue.PriorityQueue()

    def execute_search(self):
        """
        Realiza la búsqueda primero en anchura.

        :return: una lista con la trayectoria más corta del inicio al objetivo.
        :return type: list
        """
        path = []
        self.color[self.start[0]][self.start[1]] =\
            'GRAY'
        self.distance[self.start[0]][self.start[1]] = 0
        self.parent[self.start[0]][self.start[1]] = None
        self.my_bests.put((manhattan_distance(self.start, self.goal),\
            self.start))

        while not self.my_bests.empty():
            current_square = self.my_bests.get()
            current_square = current_square[1]
            if current_square == self.goal:
                print("He llegado")
                print(self.goal)
                break
            if self.parent[current_square[0]][current_square[1]]:
                current_path = self.get_path(current_square)
                path += current_path
                path += self.get_reverse_path(current_path)

            up_square = self.move_up(current_square)
            if up_square:
                self.my_bests.put((manhattan_distance(up_square, self.goal), up_square))
            right_square = self.move_to_the_right(current_square)
            if right_square:
                self.my_bests.put((manhattan_distance(right_square, self.goal), right_square))
            left_square = self.move_to_the_left(current_square)
            if left_square:
                self.my_bests.put((manhattan_distance(left_square, self.goal), left_square))
            down_square = self.move_down(current_square)
            if down_square:
                self.my_bests.put((manhattan_distance(down_square, self.goal), down_square))

            self.color[current_square[0]][current_square[1]] = 'BLACK'
        return path


class HillClimbing(SearchAlgorithm):
    """
    Clase para realizar la búsqueda heurística Hill-Climbing.
    Utiliza como medida a la meta la distancia Manhattan.
    """

    def __init__(self, grid, start, goal):
        super(HillClimbing, self).__init__(grid, start, goal)
        self.path = []
        self.time = 0
        self.done = False

    def execute_search(self):
        """
        Corre la búsqueda primero en profundidad.

        :return: una lista con la trayectoria recorrida hasta el objetivo.
        :return type: list
        """
        self.time = 0
        current_square = self.start
        self.color[current_square[0]][current_square[1]] = 'WHITE'
        self.dfs_visit(current_square)
        return self.path

    def dfs_visit(self, current_square):
        if current_square == self.goal or self.done:
            self.done = True
            return
        self.distance[current_square[0]][current_square[1]] = self.time
        self.time += 1
        self.color[current_square[0]][current_square[1]] = 'GRAY'
        up_square = self.move_up(current_square)
        down_square = self.move_down(current_square)
        right_square = self.move_to_the_right(current_square)
        left_square = self.move_to_the_left(current_square)
        candidates = [up_square, down_square, right_square, left_square]
        candidates = [(manhattan_distance(candidates[idx], self.goal), idx)\
            for idx in range(4) if candidates[idx]]
        
        for candidate in sorted(candidates):
            if self.done:
                break
            if candidate[1] == 0:
                self.path.append('U')
                self.dfs_visit(up_square)
                # if not self.done:
                self.path.append('D')
            if candidate[1] == 2:
                self.path.append('R')
                self.dfs_visit(right_square)
                # if not self.done:
                self.path.append('L')
            if candidate[1] == 3:
                self.path.append('L')
                self.dfs_visit(left_square)
                # if not self.done:
                self.path.append('R')
            if candidate[1] == 1:
                self.path.append('D')
                self.dfs_visit(down_square)
                # if not self.done:
                self.path.append('U')

        self.color[current_square[0]][current_square[1]] = 'BLACK'
