# encoding: utf-8
import queue
from search_algorithm import SearchAlgorithm


class BFS(SearchAlgorithm):
    """
    Clase para realizar la búsqueda primero
    en anchura. Es una subclase de SearchAlgorithm.
    """
    def __init__(self, grid, start, goal):
        super(BFS, self).__init__(grid, start, goal)
        self.Q = queue.Queue()
        
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
        self.Q.put(self.start)

        while not self.Q.empty():
            current_square = self.Q.get()
            if current_square == self.goal:
                break
            if self.parent[current_square[0]][current_square[1]]:
                current_path = self.get_path(current_square)
                path += current_path
                path += self.get_reverse_path(current_path)
            
            up_square = self.move_up(current_square)
            if up_square:
                self.Q.put(up_square)
            down_square = self.move_down(current_square)
            if down_square:
                self.Q.put(down_square)
            right_square = self.move_to_the_right(current_square)
            if right_square:
                self.Q.put(right_square)
            left_square = self.move_to_the_left(current_square)
            if left_square:
                self.Q.put(left_square)
            
            self.color[current_square[0]][current_square[1]] = 'BLACK'
        return path

class DFS(SearchAlgorithm):
    """
    Clase para realizar la búsqueda primero en profundidad.
    """
    def __init__(self, grid, start, goal):
        super(DFS, self).__init__(grid, start, goal)
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
        if up_square:
            self.path.append('U')
            self.dfs_visit(up_square)
            self.path.append('D')
            if self.done:
                return
        down_square = self.move_down(current_square)
        if down_square:
            self.path.append('D')
            self.dfs_visit(down_square)
            # if not self.done:
            self.path.append('U')
            if self.done:
                return
        right_square = self.move_to_the_right(current_square)
        if right_square:
            self.path.append('R')
            self.dfs_visit(right_square)
            # if not self.done:
            self.path.append('L')
            if self.done:
                return
        left_square = self.move_to_the_left(current_square)
        if left_square:
            self.path.append('L')
            self.dfs_visit(left_square)
            # if not self.done:
            self.path.append('R')
            if self.done:
                return

        self.color[current_square[0]][current_square[1]] = 'BLACK'
