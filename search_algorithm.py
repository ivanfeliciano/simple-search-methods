# encoding: utf-8
from math import inf

class SearchAlgorithm(object):
    """
    Clase base para los algoritmos de búsqueda sobre
    una cuadrícula.
    """
    def __init__(self, grid, start, goal):
        """
        Inicializa algoritmo entradas para el algoritmo 
        de búqueda.
        
        :param grid: la cuadrícula sobre la que se hace la búsqueda, con los obstáculos definidos en valores booleanos.
        :type grid: list
        :param start: las coordenadas (fila, columna) sobre la cuadrícula donde inicia la búsqueda.
        :type start: tuple
        :param goal: las coordenadas (fila, columna) sobre la cuadrícula donde termina la búsqueda.
        :type goal: tuple
        """
        self.grid_size = len(grid)
        self.grid = grid
        self.color = [['WHITE' for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.parent = [[None for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.distance = [[inf for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.start = start
        self.goal = goal

    def is_valid(self, coordinates):
        """
        Método para verificar si un cuadro está definido en 
        la cuadrícula y si no ha sido visitado.
        
        :param coordinates: coordenas del cuadrito.
        :type coordinates: tuple
        """
        return 0 <= coordinates[0] < self.grid_size and\
            0 <= coordinates[1] < self.grid_size and\
            not self.grid[coordinates[0]][coordinates[1]] and\
            self.color[coordinates[0]][coordinates[1]] == 'WHITE'
    
    def move_up(self, current_square):
        """
        Instrucción para intentar moverse hacia arriba sobre
        la cuadrícula. Si no es posible regresa False y si lo
        es, define como padre del cuadro de arriba al cuadro actual
        y además suma la distancia hasta este cuadrito para
        finalmente regresar True.
        
        :param current_square: las coordenadas del cuadro actual.
        :type current_square: tuple
        :return: un valor booleano, si realizó el movimiento o no
        """
        up_square = [current_square[0] - 1, current_square[1]]
        if self.is_valid(up_square):
            self.color[up_square[0]][up_square[1]] = 'GRAY'
            self.distance[up_square[0]][up_square[1]] =\
                self.distance[current_square[0]][current_square[1]] + 1
            self.parent[up_square[0]][up_square[1]] = ([current_square[0], current_square[1]], 'U')
            return up_square
        return False

    def move_down(self, current_square):
        """
        Instrucción para intentar moverse hacia abajo sobre
        la cuadrícula. Si no es posible regresa False y si lo
        es, define como padre del cuadro de abajo el cuadro actual
        y además suma la distancia hasta este cuadrito para
        finalmente regresar True.
        
        :param current_square: las coordenadas del cuadro actual.
        :type current_square: tuple
        :return: un valor booleano, si realizó el movimiento o no
        """
        down_square = [current_square[0] + 1, current_square[1]]
        if self.is_valid(down_square):
            self.color[down_square[0]][down_square[1]] = 'GRAY'
            self.distance[down_square[0]][down_square[1]] =\
                self.distance[current_square[0]][current_square[1]] + 1
            self.parent[down_square[0]][down_square[1]] = (
                [current_square[0], current_square[1]], 'D')
            return down_square
        return False

    def move_to_the_right(self, current_square):
        """
        Instrucción para intentar moverse hacia la derecha sobre
        la cuadrícula. Si no es posible regresa False y si lo
        es, define como padre del cuadro de la derecha al cuadro actual
        y además suma la distancia hasta este cuadrito para
        finalmente regresar True.

        :param current_square: las coordenadas del cuadro actual.
        :type current_square: tuple
        :return: un valor booleano, si realizó el movimiento o no
        """
        right_square = [current_square[0], current_square[1] + 1]
        if self.is_valid(right_square):
            self.color[right_square[0]][right_square[1]] = 'GRAY'
            self.distance[right_square[0]][right_square[1]] =\
                self.distance[current_square[0]][current_square[1]] + 1
            self.parent[right_square[0]][right_square[1]] = (
                [current_square[0], current_square[1]], 'R')
            return right_square
        return False

    def move_to_the_left(self, current_square):
        """
        Instrucción para intentar moverse hacia la izquierda sobre
        la cuadrícula. Si no es posible regresa False y si lo
        es, define como padre del cuadro de la izquieda al cuadro actual
        y además suma la distancia hasta este cuadrito para
        finalmente regresar True.

        :param current_square: las coordenadas del cuadro actual.
        :type current_square: tuple
        :return: un valor booleano, si realizó el movimiento o no
        """
        left_square = [current_square[0], current_square[1] - 1]
        if self.is_valid(left_square):
            self.color[left_square[0]][left_square[1]] = 'GRAY'
            self.distance[left_square[0]][left_square[1]] =\
                self.distance[current_square[0]][current_square[1]] + 1
            self.parent[left_square[0]][left_square[1]] = (
                [current_square[0], current_square[1]], 'L')
            return left_square
        return False



    def get_path(self, coordinates):
        """
        Obtiene el camino que se debe seguir desde el inicio
        hasta un cuadro.
        
        :param coordinates: coordenadas del que se quiere obtener un camino.
        :type coordinates: tuple
        """
        path_stack = []
        current_parent = self.parent[coordinates[0]][coordinates[1]]
        while current_parent:
            path_stack.append(current_parent[1])
            current_parent = self.parent[current_parent[0]
                                         [0]][current_parent[0][1]]
        return list(reversed(path_stack))
    
    def get_reverse_path(self, path):
        """
        Obtiene las instrucciones de regreso para
        una trayectoria dada.
        
        :param path: una lista que representa un camino de instrucciones.
        :type path: list
        """
        way_back = []
        for direction in reversed(path):
            if direction == 'U':
                way_back.append('D')
            if direction == 'D':
                way_back.append('U')
            if direction == 'R':
                way_back.append('L')
            if direction == 'L':
                way_back.append('R')
        return way_back
