# generate random maze files
import numpy as np
import random
import math

def maze(size, filename):
    # write to the given file a maze with size x size dimensions
    # create a list of size x size with all 0's and switch some entries to 1 randomly, with some probability.
    # assign any two random start and goal nodes as 2 and 3 respectively.
    maze_grid = [[0 for i in range(size)] for j in range(size)]
    
    for i in range(size):
        for j in range(size):
            value = np.random.choice(2, p = [0.3, 0.7])
            maze_grid[i][j] = value

    start = (random.randint(1, math.floor(size/2)), random.randint(1, math.floor(size/2)))
    goal = (random.randint(math.ceil(size/2), size - 1), random.randint(math.ceil(size/2), size - 1))
    maze_grid[start[0]][start[1]] = 2
    maze_grid[goal[0]][goal[1]] = 3

    f = open(filename, "w")
    # now write maze_grid to a file
    for i in range(size):
        for j in range(size):
            f.write(str(maze_grid[i][j]))
        f.write('\n')
    f.close()

filename = 'maze_new.txt'
# change the size here to generate a maze file of size: size x size
size = 100
maze(size, filename)