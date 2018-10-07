# encoding: utf-8
from random import randrange, seed
import pygame
from pygame.locals import *
class Space(object):
    grid_square_width = 50
    grid_square_height = 50
    background = pygame.image.load('./sprites/blue.png')
    meteors = [pygame.image.load('./sprites/Meteors/meteor'
                                 + str(i) + '.png') for i in range(1, 9)]
    ship = pygame.image.load('./sprites/blue_ship.png')
    star_goal = pygame.image.load('./sprites/star.png')
    background = pygame.transform.scale(background, (grid_square_width, grid_square_height))
    meteors = [ pygame.transform.scale(meteor, (50, 50))\
               for meteor in meteors ]
    path_vertical = pygame.image.load('./sprites/laserBlue12.png')
    path_vertical = pygame.transform.scale(path_vertical, (grid_square_width // 10, grid_square_height // 2))
    path_horizontal = pygame.transform.rotate(path_vertical, 90.0)
    

    def __init__(self, grid_size, width=30, height=30):
        self.grid_size = grid_size
        self.grid = [[False for i in range(grid_size)]\
                    for j in range(grid_size)]
        self.visited = [[False for i in range(grid_size)]
                        for j in range(grid_size)]
        self.window_size = (Space.grid_square_width * grid_size,\
                            Space.grid_square_height * grid_size)
        self.direction_path = [[[False for i in range(4)] for j in range(grid_size + 1)] for k in range(grid_size + 1)]
        self.ship = pygame.transform.scale(Space.ship, (Space.grid_square_width, Space.grid_square_height))
        self.star_goal = pygame.transform.scale(
            Space.star_goal, (Space.grid_square_width, Space.grid_square_height))
        self.ship_coordinates = None
        self.goal_coordinates = None


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
    def is_obstacle(self, idx_row, idx_col):
        """
        Verifica si hay un obstáculo en esta posición.
        """
        if 0 <= idx_row < self.grid_size and\
            0 <= idx_col < self.grid_size: 
            if self.grid[idx_row][idx_col]:
                return True
            return False
        raise Exception("Valores de los índices fuera de rango.") 
    def run(self):
        """
        Inicializa pygame
        """
        self.generate_configuration()
        pygame.init()
        screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Space Maze")
        done = False
        clock = pygame.time.Clock()
        show_image = True
        angle = 0.1

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif self.ship_coordinates and event.type == pygame.KEYDOWN:
                    self.visited[self.ship_coordinates[1] //
                                 Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width] = True
                    current_col = self.ship_coordinates[0] // Space.grid_square_width
                    current_row = self.ship_coordinates[1] // Space.grid_square_height
                    if event.key == K_LEFT:
                        # me muevo a la izquierda
                        if self.ship_coordinates[0] - Space.grid_square_width >= 0\
                            and not self.grid[self.ship_coordinates[1] // Space.grid_square_height][(self.ship_coordinates[0] - Space.grid_square_width) // Space.grid_square_width]: 
                            self.direction_path[current_row][current_col][3] = True
                            self.direction_path[current_row][current_col - 1][1] = True
                            self.ship_coordinates[0] -= Space.grid_square_width
                            
                    elif event.key == K_UP:
                        if self.ship_coordinates[1] - Space.grid_square_height >= 0\
                                and not self.grid[(self.ship_coordinates[1] - Space.grid_square_height) // Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width]:
                            self.direction_path[current_row][current_col][0] = True
                            self.direction_path[current_row - 1][current_col][2] = True
                            self.ship_coordinates[1] -= Space.grid_square_height 
                    elif event.key == K_RIGHT:
                        # self.ship = pygame.transform.rotate(self.ship, -90.0)
                        if self.ship_coordinates[0] + Space.grid_square_width < self.grid_size * Space.grid_square_width\
                                and not self.grid[self.ship_coordinates[1] // Space.grid_square_height][(self.ship_coordinates[0] + Space.grid_square_width) // Space.grid_square_width]:
                            self.direction_path[current_row][current_col][1] = True
                            self.direction_path[current_row][current_col + 1][3] = True
                            self.ship_coordinates[0] += Space.grid_square_width 
                    elif event.key == K_DOWN:
                        if self.ship_coordinates[1] + Space.grid_square_height < self.grid_size * Space.grid_square_height\
                                and not self.grid[(self.ship_coordinates[1] + Space.grid_square_height) // Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width]:
                            self.direction_path[current_row][current_col][2] = True
                            self.direction_path[current_row + 1][current_col][0] = True
                            self.ship_coordinates[1] += Space.grid_square_height
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // Space.grid_square_width
                    row = pos[1] // Space.grid_square_height
                    if not self.ship_coordinates and not self.is_obstacle(row, column):
                        self.ship_coordinates = [Space.grid_square_width * column,\
                        Space.grid_square_height * row]
                    elif self.ship_coordinates and not self.goal_coordinates and\
                            not self.is_obstacle(row, column):
                        self.goal_coordinates = [Space.grid_square_width * column,
                                                 Space.grid_square_height * row]
            for row in range(self.grid_size):
                for column in range(self.grid_size):
                    screen.blit(Space.background, (Space.grid_square_width * column,\
                                Space.grid_square_height * row))
                    if self.is_obstacle(row, column):
                        screen.blit(Space.meteors[self.grid[row][column]], (Space.grid_square_width * column,\
                                    Space.grid_square_height * row))
                    semipaths = self.direction_path[row][column]
                    if semipaths[0]:
                        screen.blit(Space.path_vertical, (Space.grid_square_width * column + Space.grid_square_width // 2,
                                                            Space.grid_square_height * row))
                    if semipaths[1]:
                        screen.blit(Space.path_horizontal, (Space.grid_square_width * column + Space.grid_square_width // 2,
                                                            Space.grid_square_height * row + Space.grid_square_height // 2))
                    if semipaths[2]:
                        screen.blit(Space.path_vertical, (Space.grid_square_width * column + Space.grid_square_width // 2,
                                                            Space.grid_square_height * row + Space.grid_square_height // 2))
                    if semipaths[3]:
                        screen.blit(Space.path_horizontal, (Space.grid_square_width * column,
                                                            Space.grid_square_height * row + Space.grid_square_height // 2))
            if self.goal_coordinates:
                if self.goal_coordinates == self.ship_coordinates:
                    self.star_goal = pygame.transform.rotate(self.star_goal, 90)
                screen.blit(self.star_goal, self.goal_coordinates)
                
            if self.ship_coordinates and self.ship_coordinates != self.goal_coordinates:
                screen.blit(self.ship, self.ship_coordinates)
            clock.tick(30)
            pygame.display.flip()
        pygame.quit()


def main():
    MySpace = Space(15)
    MySpace.run()

if __name__ == '__main__':
    main()