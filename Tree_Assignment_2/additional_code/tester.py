# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:45:52 2023

@author: wasih
"""
from MazeAgent import *
import matplotlib.pyplot as plt
# Requirements: have matplotlib installed.
# usage: just make sure your maze file (maze_test.txt) and MazeAgent.py are in the same directory as this script.
# the output should be a 'map.png' file showing you the path that was found by your BFS/Astar algorithm.
import time

def parse_mapfile(filename):
    # parse the given textfile, and return a 2D map list of integers
    maze = []
    row = []
    start = ()
    goal = ()
    i = 0
    j = 0
    with open(filename) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            elif c == '\n':
                i += 1
                j = 0
                # print(row)
                maze.append(row)
                row = []
                # print()
            else:
                # print(c, end = ' ')
                row.append(int(c))
                if c == '2':
                    start = (i, j)
                elif c == '3':
                    goal = (i, j)
                j += 1
    return (maze, start, goal)

def visualize_path(maze, start, goal, command_list):
    # in the description, the commands must be returned in reverse order;
    # so just reverse them back here again
    command_list.reverse()
    # given the list of path commands and the actual maze, visualize the path
    fig, ax = plt.subplots(figsize=(12,12))
    ax.imshow(maze)
    ax.scatter(start[1], start[0], c = 'r', marker = 's')
    ax.scatter(goal[1], goal[0], c = 'g', marker = 's')
    
    vertices_x = [start[1]]
    vertices_y = [start[0]]
    for cm in command_list:
        last_x = vertices_x[-1]
        last_y = vertices_y[-1]
        if 'movenorth' in cm:
            vertices_y.append(last_y + 1)
            vertices_x.append(last_x)
        elif 'movesouth' in cm:
            vertices_y.append(last_y - 1)
            vertices_x.append(last_x)
        elif 'movewest' in cm:
            vertices_y.append(last_y)
            vertices_x.append(last_x + 1)
        else:
            vertices_y.append(last_y)
            vertices_x.append(last_x - 1)
    ax.plot(vertices_x, vertices_y, 'r-')
    plt.savefig('map.png')
    
# first parse the maze text file to get the maze 2D list, start and goal nodes
filename = 'maze_test.txt'
# change the filename to test for your own custom maze files as well!
maze, start, goal = parse_mapfile(filename)
# create your agent. Change the second argument to either "bf" (BFS) or "astar" (for Astar)
agent = MazeAgent(maze, "bf")
# get the command list to reach goal from start
start_t = time.time()
commands = agent.get_path()
end_t = time.time() - start_t
print('Time it took {} seconds:'.format(end_t))
print('Number of steps in your solution: ', len(commands))
# visualize the path now.
# this would save the file as: 'map.png'
visualize_path(maze, start, goal, commands)
