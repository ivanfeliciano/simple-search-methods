import queue

class Search(object):
    def __init__(self, grid_size, obstacle, start, goal):
        self.grid_size = grid_size
        self.color = [['WHITE' for i in range(
            grid_size)] for j in range(grid_size)]
        self.parent = [[None for i in range(
            grid_size)] for j in range(grid_size)]
        self.distance = [[10e100 for i in range(
            grid_size)] for j in range(grid_size)]
        self.obstacle = obstacle
        self.start = start
        self.goal = goal
        print(self.start)
        print(self.goal)
    def is_valid(self, coordinates):
        return 0 <= coordinates[0] < self.grid_size and\
            0 <= coordinates[1] < self.grid_size and\
            not self.obstacle[coordinates[0]][coordinates[1]]
    def bfs(self):
        path = []
        Q = queue.Queue()
        self.color[self.start[0]][self.start[1]] = 'GRAY'
        self.distance[self.start[0]][self.start[1]] = 0
        self.parent[self.start[0]][self.start[1]] = None
        Q.put(self.start)
        while not Q.empty():
            current_pos = Q.get()
            if self.parent[current_pos[0]][current_pos[1]]:
                path.append(self.parent[current_pos[0]][current_pos[1]][1])
            if current_pos == self.goal:
                break
            up_pos_coord = [current_pos[0]- 1, current_pos[1]]
            if self.is_valid(up_pos_coord) and self.color[up_pos_coord[0]][up_pos_coord[1]] == 'WHITE':
                self.color[up_pos_coord[0]][up_pos_coord[1]] = 'GRAY'
                self.distance[up_pos_coord[0]][up_pos_coord[1]] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[up_pos_coord[0]][up_pos_coord[1]] = ([current_pos[0], current_pos[1]], 'U')
                Q.put(up_pos_coord)
            right_pos_coord = [current_pos[0], current_pos[1] + 1]
            if self.is_valid(right_pos_coord) and\
                    self.color[right_pos_coord[0]][right_pos_coord[1]] == 'WHITE':
                self.color[right_pos_coord[0]][right_pos_coord[1]] = 'GRAY'
                self.distance[right_pos_coord[0]][right_pos_coord[1]] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[right_pos_coord[0]][right_pos_coord[1]] = ([current_pos[0], current_pos[1]], 'R')
                Q.put(right_pos_coord)
            down_pos_coord = [current_pos[0] + 1, current_pos[1]]
            if self.is_valid(down_pos_coord) and\
                    self.color[down_pos_coord[0]][down_pos_coord[1]] == 'WHITE':
                self.color[down_pos_coord[0]][down_pos_coord[1]] = 'GRAY'
                self.distance[down_pos_coord[0]][down_pos_coord[1]] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[down_pos_coord[0]][down_pos_coord[1]] = ([current_pos[0], current_pos[1]], 'D')
                Q.put(down_pos_coord)
            left_pos_coord = [current_pos[0], current_pos[1] - 1]
            if self.is_valid(left_pos_coord) and\
                    self.color[left_pos_coord[0]][left_pos_coord[1]] == 'WHITE':
                self.color[left_pos_coord[0]][left_pos_coord[1]] = 'GRAY'
                self.distance[left_pos_coord[0]][left_pos_coord[1]] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[left_pos_coord[0]][left_pos_coord[1]] = ([current_pos[0], current_pos[1]], 'L')
                Q.put(left_pos_coord)
            self.color[current_pos[0]][current_pos[1]] = 'BLACK'
        return path
    def get_path(self):
        path_stack = []
        current_parent = self.parent[self.goal[0]][self.goal[1]]
        while current_parent:
            path_stack.append(current_parent[1])
            current_parent = self.parent[current_parent[0][0]][current_parent[0][1]]
        return path_stack[::-1]
    def manhattan_distance(self, coordinates):
        return abs(coordinates[0] - self.goal[0]) + abs(coordinates[1] - self.goal[1])
    def first_the_best(self):
        path = []
        my_bests = queue.PriorityQueue()
        self.parent = [[None for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.color = [['WHITE' for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.parent = [[None for i in range(
            self.grid_size)] for j in range(self.grid_size)]
        self.distance = [[10e100 for i in range(
            self.grid_size)] for j in range(self.grid_size)]

        self.parent[self.start[0]][self.start[1]] = None
        my_bests.put((self.manhattan_distance(self.start), self.start))
        while not my_bests.empty():
            current_pos = my_bests.get()
            current_pos = current_pos[1]
            if current_pos == self.goal:
                break
            up_pos_coord = [current_pos[0] - 1, current_pos[1]]
            if self.is_valid(up_pos_coord) and self.color[up_pos_coord[0]][up_pos_coord[1]] == 'WHITE':
                self.color[up_pos_coord[0]][up_pos_coord[1]] = 'GRAY'
                self.distance[up_pos_coord[0]][up_pos_coord[1]
                                               ] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[up_pos_coord[0]][up_pos_coord[1]] = (
                    [current_pos[0], current_pos[1]], 'U')
                path.append('U')
                my_bests.put((self.manhattan_distance(up_pos_coord), up_pos_coord))
            right_pos_coord = [current_pos[0], current_pos[1] + 1]
            if self.is_valid(right_pos_coord) and\
                    self.color[right_pos_coord[0]][right_pos_coord[1]] == 'WHITE':
                self.color[right_pos_coord[0]][right_pos_coord[1]] = 'GRAY'
                self.distance[right_pos_coord[0]][right_pos_coord[1]
                                                  ] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[right_pos_coord[0]][right_pos_coord[1]] = (
                    [current_pos[0], current_pos[1]], 'R')
                path.append('R')
                my_bests.put((self.manhattan_distance(right_pos_coord), right_pos_coord))
            down_pos_coord = [current_pos[0] + 1, current_pos[1]]
            if self.is_valid(down_pos_coord) and\
                    self.color[down_pos_coord[0]][down_pos_coord[1]] == 'WHITE':
                self.color[down_pos_coord[0]][down_pos_coord[1]] = 'GRAY'
                self.distance[down_pos_coord[0]][down_pos_coord[1]
                                                 ] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[down_pos_coord[0]][down_pos_coord[1]] = (
                    [current_pos[0], current_pos[1]], 'D')
                path.append('D')
                my_bests.put((self.manhattan_distance(down_pos_coord), down_pos_coord))
            left_pos_coord = [current_pos[0], current_pos[1] - 1]
            if self.is_valid(left_pos_coord) and\
                    self.color[left_pos_coord[0]][left_pos_coord[1]] == 'WHITE':
                self.color[left_pos_coord[0]][left_pos_coord[1]] = 'GRAY'
                self.distance[left_pos_coord[0]][left_pos_coord[1]
                                                 ] = self.distance[current_pos[0]][current_pos[1]] + 1
                self.parent[left_pos_coord[0]][left_pos_coord[1]] = (
                    [current_pos[0], current_pos[1]], 'L')
                path.append('L')
                my_bests.put((self.manhattan_distance(left_pos_coord), left_pos_coord))
            self.color[current_pos[0]][current_pos[1]] = 'BLACK'
    def a_star(self):
        pass
        
        



        

