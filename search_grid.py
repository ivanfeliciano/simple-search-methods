# encoding: utf-8

from random import randrange, seed
import time
import pygame
from pygame.locals import *

DIRECT_DICT = {"L": (-1, 0), "R": (1, 0),
               "U": (0, -1), "D": (0, 1)}

OPPOSITES = {"L": "R", "R": "L",
             "U": "D", "D": "U"}

SCREEN_HEIGHT = 600 
SCREEN_WIDTH = 800 
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
MARGIN = 10
BUTTON_WIDTH = SCREEN_WIDTH - SCREEN_HEIGHT - MARGIN
BUTTON_HEIGHT = SCREEN_HEIGHT // 7 - MARGIN
TOP_LEFT_X_GRID = 0
TOP_LEFT_Y_GRID = 0
GRID_WIDTH = GRID_HEIGHT = SCREEN_WIDTH
BUTTON_COLORS = (37, 54, 62)




class Robot(object):
    """
    La clase pública que modela al robot 
    que se mueve sobre el escenario.
    """
    def __init__(self, coordinates):
        self.direction = "U"
        self.screen_coordinates = coordinates

    def change_direction(self, new_direction):
        raise NotImplementedError


class Control(object):
    def __init__(self, grid_size):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.done = False
        self.tile_width = GRID_WIDTH // (grid_size + 1)
        self.tile_height = (GRID_HEIGHT // grid_size) 
        # self.reset_all_button = pygame.Rect(GRID_WIDTH + MARGIN, MARGIN, BUTTON_WIDTH,
        #                                     BUTTON_HEIGHT)
        # self.reset_search = pygame.Rect(GRID_WIDTH + MARGIN, BUTTON_HEIGHT + 2 * MARGIN, BUTTON_WIDTH,
        #                                     BUTTON_HEIGHT)
        # self.bfs_button = pygame.Rect(GRID_WIDTH + MARGIN, 2 * BUTTON_HEIGHT + 3 * MARGIN, BUTTON_WIDTH,
        #                                 BUTTON_HEIGHT)
        # self.dfs_button = pygame.Rect(GRID_WIDTH + MARGIN, 3 * BUTTON_HEIGHT + 4 * MARGIN, BUTTON_WIDTH,
        #                                 BUTTON_HEIGHT)
        # self.best_fs_button = pygame.Rect(GRID_WIDTH + MARGIN, 4 *  BUTTON_HEIGHT + 5 * MARGIN, BUTTON_WIDTH,
        #                                 BUTTON_HEIGHT)
        # self.hill_climbing_button = pygame.Rect(GRID_WIDTH + MARGIN, 5 * BUTTON_HEIGHT + 6 * MARGIN, BUTTON_WIDTH,
        #                                 BUTTON_HEIGHT)
        # self.a_star_button = pygame.Rect(GRID_WIDTH + MARGIN, 6 * BUTTON_HEIGHT + 7 * MARGIN, BUTTON_WIDTH,
        #                                 BUTTON_HEIGHT)
        self.grid = [[False for i in range(grid_size)]
                     for j in range(grid_size)]
        self.grid_size = grid_size
        self.normal_tile_image = pygame.image.load('./sprites/tile_cropped.png')
        self.normal_tile_image = pygame.transform.scale(self.normal_tile_image, (self.tile_width, self.tile_height))
        self.character = pygame.image.load('./sprites/character.png')
        self.character = pygame.transform.scale(self.character, (self.tile_width, self.tile_width))
        self.face_height = (0.5) * self.tile_height
        self.grid_coordinates = [[[0 for i in range(6)] for j in range(self.grid_size)] for k in range(self.grid_size)]
        self.direction_path = [[[False for i in range(4)] for j in range(
            grid_size)] for k in range(grid_size)]
        self.character_coordinates = None

    def is_valid(self, col, row):
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size and not self.grid[row][col]

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done =  True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                x = pos[0]
                y = pos[1]
                grid_pos = self.check_if_inside_some_square(x, y)
                print(grid_pos)
                if grid_pos and not self.character_coordinates and not self.grid[grid_pos[0]][grid_pos[1]]:
                    self.character_coordinates = grid_pos
            elif self.character_coordinates and event.type == pygame.KEYDOWN:
                    current_col = self.character_coordinates[1]
                    current_row = self.character_coordinates[0]
                    print(self.character_coordinates)
                    if event.key == K_LEFT:
                        if self.is_valid(current_col - 1, current_row):
                            self.character_coordinates[0] -= 1
                            print("LEFT")
                            print(self.character_coordinates)
                    elif event.key == K_UP:
                        if self.is_valid(current_col - 1, current_row + 1):
                            self.character_coordinates[0] -= 1
                            # self.character_coordinates[1] -= 1
                            print("UP")
                            print(self.character_coordinates)
                    elif event.key == K_RIGHT:
                        if self.is_valid(current_col + 1, current_row + 1):
                            self.character_coordinates[0] += 1
                            self.character_coordinates[1] += 1
                            print("RIGHT")
                            print(self.character_coordinates)
                    elif event.key == K_DOWN:
                        if self.is_valid(current_col + 1, current_row):
                            self.character_coordinates[0] += 1
                            print("DOWN")
                            print(self.character_coordinates)



    def generate_configuration(self):
        """
        Define la posición de los obstáculos.
        """
        seed()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if randrange(100) >= 75:
                    self.grid[i][j] = randrange(8)
                else:
                    self.grid[i][j] = False
    def set_squares_in_grid_coordinates(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                x = column * self.tile_width + self.tile_width / \
                    2 - (row % 2) * self.tile_width / 2
                y = row * self.face_height / 2
                # print(x, y)
                self.grid_coordinates[column][row][0] = x + self.tile_width / 2
                self.grid_coordinates[column][row][1] = y
                self.grid_coordinates[column][row][2] = x + self.tile_width
                self.grid_coordinates[column][row][3] = y + self.face_height / 2
                self.grid_coordinates[column][row][4] = x
                self.grid_coordinates[column][row][5] = y + self.face_height / 2
        print(self.grid_coordinates)

    def check_if_inside_some_square(self, x, y):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                x1 = self.grid_coordinates[column][row][0]
                y1 = self.grid_coordinates[column][row][1]
                x2 = self.grid_coordinates[column][row][2]
                y2 = self.grid_coordinates[column][row][3]
                x4 = self.grid_coordinates[column][row][4]
                y4 = self.grid_coordinates[column][row][5]
                p21 = (x2 - x1, y2 - y1)
                p41 = (x4 - x1, y4 - y1)
                p = (x - x1, y - y1)
                p21magnitude_squared = p21[0] ** 2 + p21[1] ** 2
                p41magnitude_squared = p41[0] ** 2 + p41[1] ** 2
                if 0 <= p[0] * p21[0] + p[1] * p21[1]  <= p21magnitude_squared:
                    if 0 <= p[0] * p41[0] + p[1] * p41[1] <= p41magnitude_squared:
                        return [row, column]
                    else:
                        continue
                else:
                    continue
        return None
                



    def draw(self):
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.reset_all_button)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.reset_search)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.bfs_button)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.dfs_button)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.best_fs_button)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.hill_climbing_button)
        # pygame.draw.rect(self.screen, BUTTON_COLORS, self.a_star_button)
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                x = column * self.tile_width + self.tile_width / 2 - (row % 2) * self.tile_width / 2
                y = row * self.face_height / 2 
                if not self.grid[row][column]:
                    self.screen.blit(self.normal_tile_image, (x, y))
        if self.character_coordinates:
            x = self.character_coordinates[1] * self.tile_width + self.tile_width / \
                2 - (self.character_coordinates[0] % 2) * self.tile_width / 2
            y = self.character_coordinates[0] * self.face_height / 2
            self.screen.blit(self.character, (x, y))

    
    def main_loop(self):
        self.generate_configuration()
        self.set_squares_in_grid_coordinates()
        # print(self.grid_coordinates)
        while not self.done:
            self.screen.fill((82, 96, 99))
            self.event_loop()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
        


def main():
    """
    Inicia pygame y ejecuta la aplicación
    """
    pygame.init()
    pygame.display.set_caption("Search methods IA")
    pygame.display.set_mode(SCREEN_SIZE)
    Control(10).main_loop()
    pygame.quit()


if __name__ == '__main__':
    main()
