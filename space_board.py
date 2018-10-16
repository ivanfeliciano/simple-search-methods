# encoding: utf-8
from random import randrange, seed
import time
import pygame
from pygame.locals import *

from blind_methods import BFS, DFS
from heuristic_methods import BestFS, HillClimbing
from optimal_search_methods import AStar


SCREEN_SIZE = (600, 700)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]

class SpaceShip(object):
    def __init__(self, parameter_list):
        pass

class Space(object):
    neon_cyan = (178, 255, 255)
    line_width = 3
    def __init__(self, grid_size, width=30, height=30):
        self.grid_size = grid_size
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.grid_square_width = SCREEN_WIDTH // self.grid_size
        self.grid_square_height = SCREEN_WIDTH // self.grid_size

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.done = False

        # Load sprites
        self.background_sprite = pygame.image.load('./sprites/blue.png')
        self.meteors = [pygame.image.load('./sprites/Meteors/meteor'
                                    + str(i) + '.png') for i in range(1, 9)]
        self.ship_sprite = pygame.image.load('./sprites/blue_ship.png')
        self.goal_sprite = pygame.image.load('./sprites/blue_planet.png')

        # Scale sprites
        self.ship = pygame.transform.scale(self.ship_sprite, (self.grid_square_width, self.grid_square_height))
        self.goal_sprite = pygame.transform.scale(self.goal_sprite, (self.grid_square_width, self.grid_square_height))
        self.background_sprite = pygame.transform.scale(self.background_sprite, (self.grid_square_width, self.grid_square_height))
        self.meteors = [pygame.transform.scale(meteor, (self.grid_square_width, self.grid_square_height)) for meteor in self.meteors]
        self.ship_coordinates = None
        self.goal_coordinates = None

        #Init data structures
        self.direction_path = [[[False for i in range(4)] for j in range(grid_size + 1)] for k in range(grid_size + 1)]
        self.grid = [[False for i in range(grid_size)]\
                    for j in range(grid_size)]
        self.visited = [[False for i in range(grid_size)]
                        for j in range(grid_size)]

    def generate_configuration(self):
        """
        Define la posición de los obstáculos.
        """
        seed()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if randrange(100) >= 80:
                    self.grid[i][j] = randrange(8)
                else:
                    self.grid[i][j] = False
    def is_valid(self, idx_row, idx_col):
        """
        Verifica si hay un obstáculo en esta posición.
        """
        return 0 <= idx_row < self.grid_size and 0 <= idx_col < self.grid_size and not self.grid[idx_row][idx_col]
    
    def draw_path(path):
        pass
    
    def draw(parameter_list):
        pass
    
    def event_loop(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif self.ship_coordinates and event.type == pygame.KEYDOWN:
                    self.visited[self.ship_coordinates[1] //
                                 self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width] = True
                    current_col = self.ship_coordinates[0] // self.grid_square_width
                    current_row = self.ship_coordinates[1] // self.grid_square_height
                    if event.key == K_LEFT:
                        if self.ship_coordinates[0] - self.grid_square_width >= 0\
                                and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] - self.grid_square_width) // self.grid_square_width]:
                            self.direction_path[current_row][current_col][3] = True
                            self.direction_path[current_row][current_col - 1][1] = True
                            self.ship_coordinates[0] -= self.grid_square_width
                    elif event.key == K_UP:
                        if self.ship_coordinates[1] - self.grid_square_height >= 0\
                                and not self.grid[(self.ship_coordinates[1] - self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                            self.direction_path[current_row][current_col][0] = True
                            self.direction_path[current_row -
                                                1][current_col][2] = True
                            self.ship_coordinates[1] -= self.grid_square_height
                    elif event.key == K_RIGHT:
                        if self.ship_coordinates[0] + self.grid_square_width < self.grid_size * self.grid_square_width\
                                and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] + self.grid_square_width) // self.grid_square_width]:
                            self.direction_path[current_row][current_col][1] = True
                            self.direction_path[current_row][current_col + 1][3] = True
                            self.ship_coordinates[0] += self.grid_square_width
                    elif event.key == K_DOWN:
                        if self.ship_coordinates[1] + self.grid_square_height < self.grid_size * self.grid_square_height\
                                and not self.grid[(self.ship_coordinates[1] + self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                            self.direction_path[current_row][current_col][2] = True
                            self.direction_path[current_row +
                                                1][current_col][0] = True
                            self.ship_coordinates[1] += self.grid_square_height
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // self.grid_square_width
                    row = pos[1] // self.grid_square_height
                    if not self.ship_coordinates and self.is_valid(row, column):
                        self.ship_coordinates = [self.grid_square_width * column,
                                                 self.grid_square_height * row]
                    elif self.ship_coordinates and not self.goal_coordinates and\
                            self.is_valid(row, column):
                        self.goal_coordinates = [
                            self.grid_square_width * column, self.grid_square_height * row]


    def run(self):
        """
        Inicializa pygame
        """
        finished = False
        index_bfs_path = 0
        path_best_first_search = []
        path_bfs = []
        shorthest_path_bfs = []
        idx_shorthest_path_bfs = 0
        self.generate_configuration()
        while not self.done:
            self.event_loop()
            if index_bfs_path < len(path_bfs):
                self.visited[self.ship_coordinates[1] //
                                self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width] = True
                current_col = self.ship_coordinates[0] // self.grid_square_width
                current_row = self.ship_coordinates[1] // self.grid_square_height
                if path_bfs[index_bfs_path] == 'L':
                    if self.ship_coordinates[0] - self.grid_square_width >= 0\
                            and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] - self.grid_square_width) // self.grid_square_width]:
                        self.direction_path[current_row][current_col][3] = True
                        self.direction_path[current_row][current_col - 1][1] = True
                        self.ship_coordinates[0] -= self.grid_square_width
                elif path_bfs[index_bfs_path] == 'U':
                    if self.ship_coordinates[1] - self.grid_square_height >= 0\
                            and not self.grid[(self.ship_coordinates[1] - self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                        self.direction_path[current_row][current_col][0] = True
                        self.direction_path[current_row -
                                            1][current_col][2] = True
                        self.ship_coordinates[1] -= self.grid_square_height
                elif path_bfs[index_bfs_path] == 'R':
                    if self.ship_coordinates[0] + self.grid_square_width < self.grid_size * self.grid_square_width\
                            and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] + self.grid_square_width) // self.grid_square_width]:
                        self.direction_path[current_row][current_col][1] = True
                        self.direction_path[current_row][current_col + 1][3] = True
                        self.ship_coordinates[0] += self.grid_square_width
                elif path_bfs[index_bfs_path] == 'D':
                    if self.ship_coordinates[1] + self.grid_square_height < self.grid_size * self.grid_square_height\
                            and not self.grid[(self.ship_coordinates[1] + self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                        self.direction_path[current_row][current_col][2] = True
                        self.direction_path[current_row +
                                            1][current_col][0] = True
                        self.ship_coordinates[1] += self.grid_square_height
                index_bfs_path += 1
            elif idx_shorthest_path_bfs < len(shorthest_path_bfs):
                time.sleep(0.1)
                self.visited[self.ship_coordinates[1] //
                                self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width] = True
                current_col = self.ship_coordinates[0] // self.grid_square_width
                current_row = self.ship_coordinates[1] // self.grid_square_height
                if shorthest_path_bfs[idx_shorthest_path_bfs] == 'L':
                    if self.ship_coordinates[0] - self.grid_square_width >= 0\
                            and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] - self.grid_square_width) // self.grid_square_width]:
                        self.direction_path[current_row][current_col][3] = True
                        self.direction_path[current_row][current_col - 1][1] = True
                        self.ship_coordinates[0] -= self.grid_square_width
                elif shorthest_path_bfs[idx_shorthest_path_bfs] == 'U':
                    if self.ship_coordinates[1] - self.grid_square_height >= 0\
                            and not self.grid[(self.ship_coordinates[1] - self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                        self.direction_path[current_row][current_col][0] = True
                        self.direction_path[current_row -
                                            1][current_col][2] = True
                        self.ship_coordinates[1] -= self.grid_square_height
                elif shorthest_path_bfs[idx_shorthest_path_bfs] == 'R':
                    if self.ship_coordinates[0] + self.grid_square_width < self.grid_size * self.grid_square_width\
                            and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] + self.grid_square_width) // self.grid_square_width]:
                        self.direction_path[current_row][current_col][1] = True
                        self.direction_path[current_row][current_col + 1][3] = True
                        self.ship_coordinates[0] += self.grid_square_width
                elif shorthest_path_bfs[idx_shorthest_path_bfs] == 'D':
                    if self.ship_coordinates[1] + self.grid_square_height < self.grid_size * self.grid_square_height\
                            and not self.grid[(self.ship_coordinates[1] + self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                        self.direction_path[current_row][current_col][2] = True
                        self.direction_path[current_row +
                                            1][current_col][0] = True
                        self.ship_coordinates[1] += self.grid_square_height
                idx_shorthest_path_bfs += 1


            for row in range(self.grid_size):
                for column in range(self.grid_size):
                    self.screen.blit(self.background_sprite, (self.grid_square_width * column,\
                                self.grid_square_height * row))
                    if self.grid[row][column]:
                        self.screen.blit(self.meteors[self.grid[row][column]], (self.grid_square_width * column,\
                                    self.grid_square_height * row))
                    semipaths = self.direction_path[row][column]
                    if semipaths[0]:
                    	pygame.draw.line(self.screen, Space.neon_cyan, (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row), (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row + self.grid_square_height // 2), Space.line_width)
                    if semipaths[1]:
                    	pygame.draw.line(self.screen, Space.neon_cyan, (self.grid_square_width * column + self.grid_square_width // 2, self.grid_square_height * row + self.grid_square_height // 2),\
                    	(self.grid_square_width * column + self.grid_square_width, self.grid_square_height * row + self.grid_square_height // 2), Space.line_width)
                    if semipaths[2]:
                    	pygame.draw.line(self.screen, Space.neon_cyan, (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row + self.grid_square_height // 2), (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row + self.grid_square_height), Space.line_width)
                    if semipaths[3]:
                    	pygame.draw.line(self.screen, Space.neon_cyan, (self.grid_square_width * column,
                                                            self.grid_square_height * row + self.grid_square_height // 2), (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row + self.grid_square_height // 2), Space.line_width)
            if self.goal_coordinates:
                self.screen.blit(self.goal_sprite, self.goal_coordinates)
                
            if self.ship_coordinates and self.ship_coordinates != self.goal_coordinates:
                self.screen.blit(self.ship, self.ship_coordinates)
            if self.ship_coordinates and self.goal_coordinates and not finished:
                my_search = HillClimbing(
                    self.grid, [self.ship_coordinates[1] // self.grid_square_height, self.ship_coordinates[0] // self.grid_square_width], [self.goal_coordinates[1] // self.grid_square_height, self.goal_coordinates[0] // self.grid_square_width])
                path_bfs = my_search.execute_search()
                #print(path_bfs)
                shorthest_path_bfs = my_search.get_path(
                      [self.goal_coordinates[1] // self.grid_square_height, self.goal_coordinates[0] // self.grid_square_width])
                # print(shorthest_path_bfs)
                # path_best_first_search = my_search.first_the_best()
                # shorthest_path_best = my_search.get_path(
                #     [self.goal_coordinates[1] // self.grid_square_height, self.goal_coordinates[0] // self.grid_square_width])
                finished = True
            pygame.display.update()
            self.clock.tick(self.fps)


def main():
    pygame.init()
    pygame.display.set_caption("Search methods IA")
    pygame.display.set_mode(SCREEN_SIZE)
    Space(20).run()
    pygame.quit()

    
        

if __name__ == '__main__':
    main()
