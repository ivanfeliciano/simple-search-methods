# encoding: utf-8
from random import randrange, seed
import time
import argparse
import pygame
from pygame.locals import *


from button import Button
from blind_methods import BFS, DFS
from heuristic_methods import BestFS, HillClimbing
from optimal_search_methods import AStar


SCREEN_SIZE = (600, 650)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]

SEARCH_METHODS = {
    "BFS" : BFS, "DFS" : DFS, "BestFS": BestFS,
    "HillClimbing" : HillClimbing, "A*" : AStar
}
COLORS = {
    "BFS": (54, 187, 245), "DFS":  (222, 83, 44), "BestFS": (172, 57, 57),
    "HillClimbing": (113, 201, 55), "A*": (255, 204, 0)
}
BEST_PATH_COLOR = (178, 255, 255)
LINE_WIDTH_NORMAL_PATH = 3 
LINE_WIDTH_BEST_PATH = 2

class Space(object):
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid_square_width = SCREEN_WIDTH // self.grid_size
        self.grid_square_height = SCREEN_WIDTH // self.grid_size

        # pygame needed values
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 30



        # Load sprites
        self.background_sprite = pygame.image.load('./sprites/blue.png')
        self.meteors = [pygame.image.load('./sprites/Meteors/meteor'
                                    + str(i) + '.png') for i in range(1, 9)]
        self.goal_sprite = pygame.image.load('./sprites/blue_planet.png')
        self.init_sprite = pygame.image.load('./sprites/init.png')
        space_ships_path = './sprites/ships/'
        self.space_ships = {
            "BFS": pygame.image.load(space_ships_path + 'bfs.png'), 
            "DFS": pygame.image.load(space_ships_path + 'dfs.png'),
            "BestFS": pygame.image.load(space_ships_path + 'bestfirst.png'),
            "HillClimbing": pygame.image.load(space_ships_path + 'hillclimbing.png'),
            "A*": pygame.image.load(space_ships_path + 'astar.png'),
        }

        # Scale sprites
        self.goal_sprite = pygame.transform.scale(self.goal_sprite, (self.grid_square_width, self.grid_square_height))
        self.background_sprite = pygame.transform.scale(self.background_sprite, (self.grid_square_width, self.grid_square_height))
        self.meteors = [pygame.transform.scale(meteor, (self.grid_square_width, self.grid_square_height)) for meteor in self.meteors]
        self.init_sprite = pygame.transform.scale(self.init_sprite, (self.grid_square_width, self.grid_square_height))
        for key in self.space_ships:
            self.space_ships[key] = pygame.transform.scale(
                self.space_ships[key], (self.grid_square_width, self.grid_square_height))
        self.ship = self.init_sprite
        

        #Init data structures
        self.direction_path = [[[False for i in range(4)] for j in range(grid_size + 1)] for k in range(grid_size)]
        self.direction_best_path = [[[False for i in range(4)] for j in range(grid_size + 1)] for k in range(grid_size)]
        self.grid = [[False for i in range(grid_size)] for j in range(grid_size)]

        #init coordinates for start and finish points
        self.initial_coordinates = None
        self.ship_coordinates = None
        self.goal_coordinates = None

        # flags and others
        self.search_has_finished = False
        self.done = False
        self.current_color = BEST_PATH_COLOR
        self.no_he_dibujado_el_camino = False
        self.init_sprite_for_mouse_over = None
        self.planet_sprite_for_mouse_over = None

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
    
    def generate_path_from_list(self, direction_path, path):
        
        for instruction in path:
            current_col = self.ship_coordinates[0] // self.grid_square_width
            current_row = self.ship_coordinates[1] // self.grid_square_height
            if instruction == 'L':
                if self.ship_coordinates[0] - self.grid_square_width >= 0\
                        and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] - self.grid_square_width) // self.grid_square_width]:
                    direction_path[current_row][current_col][3] = True
                    direction_path[current_row][current_col - 1][1] = True
                    self.ship_coordinates[0] -= self.grid_square_width
            elif instruction == 'U':
                if self.ship_coordinates[1] - self.grid_square_height >= 0\
                        and not self.grid[(self.ship_coordinates[1] - self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                    direction_path[current_row][current_col][0] = True
                    direction_path[current_row -
                                        1][current_col][2] = True
                    self.ship_coordinates[1] -= self.grid_square_height
            elif instruction == 'R':
                if self.ship_coordinates[0] + self.grid_square_width < self.grid_size * self.grid_square_width\
                        and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] + self.grid_square_width) // self.grid_square_width]:
                    direction_path[current_row][current_col][1] = True
                    direction_path[current_row][current_col + 1][3] = True
                    self.ship_coordinates[0] += self.grid_square_width
            elif instruction == 'D':
                if self.ship_coordinates[1] + self.grid_square_height < self.grid_size * self.grid_square_height\
                        and not self.grid[(self.ship_coordinates[1] + self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                    direction_path[current_row][current_col][2] = True
                    direction_path[current_row +
                                        1][current_col][0] = True
                    self.ship_coordinates[1] += self.grid_square_height
        self.ship_coordinates = self.initial_coordinates.copy()
    

    def draw_line(self, direction_path, color, line_width, row, column):
        semipaths = direction_path[row][column]
        if semipaths[0]:
                    pygame.draw.line(self.screen, color, (self.grid_square_width * column + self.grid_square_width // 2,
                                    self.grid_square_height * row), (self.grid_square_width * column + self.grid_square_width // 2,
                                                                        self.grid_square_height * row + self.grid_square_height // 2), line_width)
        if semipaths[1]:
            pygame.draw.line(self.screen, color, (self.grid_square_width * column + self.grid_square_width // 2, self.grid_square_height * row + self.grid_square_height // 2),
                                (self.grid_square_width * column + self.grid_square_width, self.grid_square_height * row + self.grid_square_height // 2), line_width)
        if semipaths[2]:
            pygame.draw.line(self.screen, color, (self.grid_square_width * column + self.grid_square_width // 2,
                                                            self.grid_square_height * row + self.grid_square_height // 2), (self.grid_square_width * column + self.grid_square_width // 2,
                                                                                                                            self.grid_square_height * row + self.grid_square_height), line_width)
        if semipaths[3]:
            pygame.draw.line(self.screen, color, (self.grid_square_width * column,
                                                            self.grid_square_height * row + self.grid_square_height // 2), (self.grid_square_width * column + self.grid_square_width // 2,
                                                                                                                            self.grid_square_height * row + self.grid_square_height // 2), line_width)
    def draw(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                self.screen.blit(self.background_sprite, (self.grid_square_width * column,
                                                            self.grid_square_height * row))
                if self.grid[row][column]:
                    self.screen.blit(self.meteors[self.grid[row][column]], (self.grid_square_width * column,
                                                                            self.grid_square_height * row))
                self.draw_line(self.direction_path, self.current_color,
                               LINE_WIDTH_NORMAL_PATH, row, column)
                self.draw_line(self.direction_best_path, BEST_PATH_COLOR, LINE_WIDTH_BEST_PATH, row, column)
                if self.init_sprite_for_mouse_over and self.init_sprite_for_mouse_over[0] == row and self.init_sprite_for_mouse_over[1] == column:
                    self.screen.blit(self.init_sprite, (self.grid_square_width * column,
                                                                self.grid_square_height * row))
                if self.planet_sprite_for_mouse_over and self.planet_sprite_for_mouse_over[0] == row and self.planet_sprite_for_mouse_over[1] == column:
                    self.screen.blit(self.goal_sprite, (self.grid_square_width * column,
                                                                self.grid_square_height * row))
    
    def run_search_method(self, method):

        method_selected = SEARCH_METHODS.get(method)
        if method_selected:
            start = [self.ship_coordinates[1] // self.grid_square_height,
                     self.ship_coordinates[0] // self.grid_square_width]
            goal = [self.goal_coordinates[1] // self.grid_square_height,
                    self.goal_coordinates[0] // self.grid_square_width]
            current_search = method_selected(self.grid, start, goal)
            path = current_search.execute_search()
            best_path = current_search.get_path(goal)
            return path, best_path



    def event_loop(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif self.ship_coordinates and event.type == pygame.KEYDOWN:
                    current_col = self.ship_coordinates[0] // self.grid_square_width
                    current_row = self.ship_coordinates[1] // self.grid_square_height
                    if event.key == K_LEFT:
                        if self.ship_coordinates[0] - self.grid_square_width >= 0\
                                and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] - self.grid_square_width) // self.grid_square_width]:
                            self.direction_best_path[current_row][current_col][3] = True
                            self.direction_best_path[current_row][current_col - 1][1] = True
                            self.ship_coordinates[0] -= self.grid_square_width
                    elif event.key == K_UP:
                        if self.ship_coordinates[1] - self.grid_square_height >= 0\
                                and not self.grid[(self.ship_coordinates[1] - self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                            self.direction_best_path[current_row][current_col][0] = True
                            self.direction_best_path[current_row -
                                                1][current_col][2] = True
                            self.ship_coordinates[1] -= self.grid_square_height
                    elif event.key == K_RIGHT:
                        if self.ship_coordinates[0] + self.grid_square_width < self.grid_size * self.grid_square_width\
                                and not self.grid[self.ship_coordinates[1] // self.grid_square_height][(self.ship_coordinates[0] + self.grid_square_width) // self.grid_square_width]:
                            self.direction_best_path[current_row][current_col][1] = True
                            self.direction_best_path[current_row][current_col + 1][3] = True
                            self.ship_coordinates[0] += self.grid_square_width
                    elif event.key == K_DOWN:
                        if self.ship_coordinates[1] + self.grid_square_height < self.grid_size * self.grid_square_height\
                                and not self.grid[(self.ship_coordinates[1] + self.grid_square_height) // self.grid_square_height][self.ship_coordinates[0] // self.grid_square_width]:
                            self.direction_best_path[current_row][current_col][2] = True
                            self.direction_best_path[current_row +
                                                1][current_col][0] = True
                            self.ship_coordinates[1] += self.grid_square_height
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // self.grid_square_width
                    row = pos[1] // self.grid_square_height
                    if not self.ship_coordinates and self.is_valid(row, column):
                        self.ship_coordinates = [self.grid_square_width * column,
                                                 self.grid_square_height * row]
                        self.initial_coordinates = [self.grid_square_width * column,
                                                    self.grid_square_height * row]
                        self.init_sprite_for_mouse_over = None
                    elif self.ship_coordinates and not self.goal_coordinates and\
                            self.is_valid(row, column):
                        self.goal_coordinates = [
                            self.grid_square_width * column, self.grid_square_height * row]
                        self.planet_sprite_for_mouse_over = None
                    elif self.ship_coordinates and self.goal_coordinates and self.is_valid(row, column):
                        self.grid[row][column] = randrange(8)
                elif event.type == pygame.MOUSEMOTION and not self.ship_coordinates:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // self.grid_square_width
                    row = pos[1] // self.grid_square_height
                    if self.is_valid(row, column):
                        self.init_sprite_for_mouse_over = [row, column]
                elif event.type == pygame.MOUSEMOTION and not self.goal_coordinates:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // self.grid_square_width
                    row = pos[1] // self.grid_square_height
                    if self.is_valid(row, column):
                        self.planet_sprite_for_mouse_over = [row, column]

    def clear(self):
        self.ship = self.init_sprite
        self.direction_path = [[[False for i in range(4)] for j in range(
            self.grid_size + 1)] for k in range(self.grid_size + 1)]
        self.direction_best_path = [[[False for i in range(4)] for j in range(
            self.grid_size + 1)] for k in range(self.grid_size + 1)]
        self.search_has_finished = False
        self.ship_coordinates = self.initial_coordinates.copy()
        self.no_he_dibujado_el_camino = False

    def reset(self):
        self.no_he_dibujado_el_camino = False
        self.ship_coordinates = None
        self.goal_coordinates = None
        self.ship = self.init_sprite
        self.direction_path = [[[False for i in range(4)] for j in range(
            self.grid_size + 1)] for k in range(self.grid_size + 1)]
        self.direction_best_path = [[[False for i in range(4)] for j in range(
            self.grid_size + 1)] for k in range(self.grid_size + 1)]
        self.grid = [[False for i in range(self.grid_size)]
                    for j in range(self.grid_size)]
        self.initial_coordinates = None
        self.search_has_finished = False
        # self.generate_configuration()

    def run(self):
        """
        Bucle principal
        """
        path = []
        shorthest_path = []
        method = None
        # self.generate_configuration()
        reset_button = Button("", 0, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_reset-all.png")
        restart_button = Button("", 1 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_clear.png")
        bfs_button = Button("", 2 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_bfs.png")
        dfs_button = Button("", 3 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_dfs.png")
        best_fs_button = Button("", 4 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_best-fs.png")
        hill_climbing_button = Button("", 5 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_hill-climbing.png")
        a_star_button = Button("", 6 * SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_WIDTH // 7,
                              SCREEN_HEIGHT - SCREEN_WIDTH, "./sprites/button_a.png")

                            
        while not self.done:
            self.screen.fill((55, 60, 68))
            self.event_loop()
            reset_button.draw(self.screen)  # pygame.surface.Surface()
            restart_button.draw(self.screen)  # pygame.surface.Surface()
            bfs_button.draw(self.screen)  # pygame.surface.Surface()
            dfs_button.draw(self.screen)  # pygame.surface.Surface()
            best_fs_button.draw(self.screen)  # pygame.surface.Surface()
            hill_climbing_button.draw(self.screen)  # pygame.surface.Surface()
            a_star_button.draw(self.screen)  # pygame.surface.Surface()
            if reset_button.click():
                self.reset()
            if restart_button.click() and self.ship_coordinates and self.goal_coordinates:
                self.clear()
            if bfs_button.click() and self.ship_coordinates and self.goal_coordinates:
                method = "BFS"
            if dfs_button.click() and self.ship_coordinates and self.goal_coordinates:
                method = "DFS"
            if best_fs_button.click() and self.ship_coordinates and self.goal_coordinates:
                method = "BestFS"
            if hill_climbing_button.click() and self.ship_coordinates and self.goal_coordinates:
                method = "HillClimbing"
            if a_star_button.click() and self.ship_coordinates and self.goal_coordinates:
                method = "A*"
            self.draw()

            if path and not self.no_he_dibujado_el_camino:
                self.generate_path_from_list(self.direction_path, path)
                if shorthest_path:
                    self.generate_path_from_list(self.direction_best_path, shorthest_path)
                self.no_he_dibujado_el_camino = True
                path = []
                shorthest_path = []
            
            if self.goal_coordinates:
                self.screen.blit(self.goal_sprite, self.goal_coordinates)
            if self.ship_coordinates and self.ship_coordinates != self.goal_coordinates:
                self.screen.blit(self.ship, self.ship_coordinates)
            if self.ship_coordinates and self.goal_coordinates and not self.search_has_finished and method:
                self.current_color = COLORS[method]
                self.ship = self.space_ships[method]
                ans = self.run_search_method(method)
                if ans:
                    path = ans[0]
                    shorthest_path = ans[1]
                self.search_has_finished = True
                method = ""
                
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.fps)


def main():
    parser = argparse.ArgumentParser(
        description='A simple app for showing some simple search methods.')
    parser.add_argument("--n", help="size of the grid")
    args = parser.parse_args()
    pygame.init()
    pygame.display.set_caption("Search methods IA")
    pygame.display.set_mode(SCREEN_SIZE)
    if args.n and 2 < int(args.n) <= 50:
        Space(int(args.n)).run()
    else:
        Space(10).run()
    pygame.quit()

    
        

if __name__ == '__main__':
    main()
