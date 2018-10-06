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
    star_goal = pygame.image.load('./sprites/star_gold.png')
    background = pygame.transform.scale(background, (grid_square_width, grid_square_height))
    meteors = [ pygame.transform.scale(meteor, (50, 50))\
               for meteor in meteors ]
    trail = pygame.image.load('./sprites/star2.png')
    trail = pygame.transform.scale(trail, (grid_square_width // 3, grid_square_height // 3))

    def __init__(self, grid_size, width=30, height=30):
        self.grid_size = grid_size
        self.grid = [[False for i in range(grid_size)]\
                    for j in range(grid_size)]
        self.visited = [[False for i in range(grid_size)]
                        for j in range(grid_size)]
        self.window_size = (Space.grid_square_width * grid_size,\
                            Space.grid_square_height * grid_size)
        self.ship = pygame.transform.scale(Space.ship, (Space.grid_square_width, Space.grid_square_height))

        self.ship_coordinates = None

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

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif self.ship_coordinates and event.type == pygame.KEYDOWN:
                    self.visited[self.ship_coordinates[1] //
                                 Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width] = True
                    if event.key == K_LEFT:
                        # self.ship = pygame.transform.rotate(self.ship, 90.0)
                        if self.ship_coordinates[0] - Space.grid_square_width >= 0\
                            and not self.grid[self.ship_coordinates[1] // Space.grid_square_height][(self.ship_coordinates[0] - Space.grid_square_width) // Space.grid_square_width]: 
                            self.ship_coordinates[0] -= Space.grid_square_width 
                    elif event.key == K_UP:
                        if self.ship_coordinates[1] - Space.grid_square_height >= 0\
                                and not self.grid[(self.ship_coordinates[1] - Space.grid_square_height) // Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width]:
                            self.ship_coordinates[1] -= Space.grid_square_height 
                    elif event.key == K_RIGHT:
                        # self.ship = pygame.transform.rotate(self.ship, -90.0)
                        if self.ship_coordinates[0] + Space.grid_square_width < self.grid_size * Space.grid_square_width\
                                and not self.grid[self.ship_coordinates[1] // Space.grid_square_height][(self.ship_coordinates[0] + Space.grid_square_width) // Space.grid_square_width]:
                            self.ship_coordinates[0] += Space.grid_square_width 
                    elif event.key == K_DOWN:
                        if self.ship_coordinates[1] + Space.grid_square_height < self.grid_size * Space.grid_square_height\
                                and not self.grid[(self.ship_coordinates[1] + Space.grid_square_height) // Space.grid_square_height][self.ship_coordinates[0] // Space.grid_square_width]:
                            self.ship_coordinates[1] += Space.grid_square_height
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // Space.grid_square_width
                    row = pos[1] // Space.grid_square_height
                    if not self.ship_coordinates:
                        self.ship_coordinates = [Space.grid_square_width * column,\
                        Space.grid_square_height * row]
                        print("Click ", pos, "Grid coordinates: ", row, column)
            for row in range(self.grid_size):
                for column in range(self.grid_size):
                    screen.blit(Space.background, (Space.grid_square_width * column,\
                                Space.grid_square_height * row))
                    if self.is_obstacle(row, column):
                        screen.blit(Space.meteors[self.grid[row][column]], (Space.grid_square_width * column,\
                                    Space.grid_square_height * row))
                    if self.visited[row][column]:
                        screen.blit(Space.trail, (Space.grid_square_width * column + Space.grid_square_width // 3,
                                                  Space.grid_square_height * row + Space.grid_square_height // 3 ))
            if self.ship_coordinates:
                screen.blit(self.ship, self.ship_coordinates)
            clock.tick(30)
            pygame.display.flip()
        pygame.quit()


def main():
    MySpace = Space(15)
    MySpace.run()

if __name__ == '__main__':
    main()
