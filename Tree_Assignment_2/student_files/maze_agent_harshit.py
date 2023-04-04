from collections import deque
import math
from queue import PriorityQueue
import random


class MazeAgent(object):
    '''
    Agent that uses path planning algorithm to figure out path to take to reach goal
    Built for Malmo discrete environment and to use Malmo discrete movements
    '''

    def __init__(self, grid=None, path_alg=None):
        '''
        Arguments
            grid -- (optional) a 2D list that represents the map
            path_alg -- (optional) a string that represents path algorithm to be
                used. Should be "bf" or "astar"
        '''
        self.__frontier_set = None
        self.__explored_set = None
        self.__goal_state = None
        self.__grid = grid
        if (path_alg is None):
            self.__path_alg = "bf"
        else:
            self.__path_alg = path_alg


    def get_eset(self):
        return self.__explored_set

    def get_fset(self):
        return self.__frontier_set

    def get_goal(self):
        return self.__goal_state

    def set_grid(self, grid):
        self.__grid = grid





    def __get_neighbors(self, curr_node):
        '''helper function to get neighbors of a node in grid'''
        neighbors = []
        x, y = curr_node
        if x > 0:
            neighbors.append((x-1, y))
        if x < len(self.__grid) - 1:
            neighbors.append((x+1, y))
        if y > 0:
            neighbors.append((x, y-1))
        if y < len(self.__grid[0]) - 1:
            neighbors.append((x, y+1))
        return neighbors

    def __reconstruct_path(self, came_from, curr_node, goal_node):
        '''helper function to get path from start to goal'''
        path = []
        while curr_node != goal_node:
            x, y = curr_node
            x_next, y_next = came_from[curr_node]
            if x_next < x:
                path.append("movenorth 1")
            elif x_next > x:
                path.append("movesouth 1")
            elif y_next < y:
                path.append("movewest 1")
            elif y_next > y:
                path.append("moveeast 1")
            curr_node = came_from[curr_node]
        return path[::-1]

    def __plan_path_breadth(self, curr_node, goal_node):
        '''Breadth-First tree search
            Arguments:
                curr_node -- Current node of algorithm
                goal_node -- The goal node to which the agent must travel
            Returns:
                ordered list that gives set of commands to move to from init to
                 goal position
        '''
        frontier_set = deque([curr_node])
        explored_set = set()
        came_from = {}
        while frontier_set:
            curr_node = frontier_set.popleft()
            if curr_node == goal_node:
                break
            for next_node in self.__get_neighbors(curr_node):
                if next_node in explored_set:
                    continue
                frontier_set.append(next_node)
                explored_set.add(next_node)
                came_from[next_node] = curr_node
        return self.__reconstruct_path(came_from, curr_node, goal_node)
# Please note that this implementation assumes that the grid is a 2D list of nodes, and the movement commands are "movenorth", "movesouth", "movewest", and "moveeast".







    def __plan_path_astar(self, curr_node, goal_node):
        '''A* tree searchReturns:
            ordered list that gives set of commands to move to from init to
             goal position

            Arguments:
                curr_node -- current node to be processed (may be initial node)
                goal_node -- goal node to be tested
            Returns:
                ordered list that gives set of commands to move to from init to
                 goal position
        '''
        self.__frontier_set = PriorityQueue()
        self.__explored_set = set()
        self.__frontier_set.put(curr_node, 0)
        came_from = {}
        cost_so_far = {}
        came_from[curr_node] = None
        cost_so_far[curr_node] = 0

        while not self.__frontier_set.empty():
            current = self.__frontier_set.get()

            if current == goal_node:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal_node, next)
                    self.__frontier_set.put(next, priority)
                    came_from[next] = current

        return self.__reconstruct_path(came_from, curr_node, goal_node)


    def get_path(self):
        '''should return list of strings where each string gives movement command
            (these should be in order)
            Example:
             ["movenorth 1", "movesouth 1", "moveeast 1", "movewest 1"]
             (these are also the only four commands that can be used, you
             cannot move diagonally)
             On a 2D grid (list), "move north" would move us
             from, say, [0][0] to [1][0]
        '''
        if self.__path_alg == "bf":
            return self.__plan_path_breadth(start_node, goal_node)
        elif self.__path_alg == "astar":
            return self.__plan_path_astar(start_node, goal_node)
        else:
            raise Exception("Invalid path algorithm specified.")

# We don't have to worry about this right now, but if you wanted to increase your difficulty (in the sense you NEED MOAR THINGS TO DO), this isn't a bad place to start!
class OnlineMazeAgent(object):
    '''
    Agent that uses online search algorithms to figure out path to take to reach goal
    Built for Malmo discrete environment and to use Malmo discrete movements
    '''

    def __init__(self, grid=None):
        '''
        Arguments
            grid -- (optional) a 2D list that represents the map
        '''
        self.__frontier_set = None
        self.__explored_set = None
        self.__goal_state = None
        self.__grid = grid


    def get_eset(self):
        return self.__explored_set

    def get_fset(self):
        return self.__frontier_set

    def get_goal(self):
        return self.__goal_state

    def set_grid(self, grid):
        self.__grid = grid

    def __local_plan_hill_climbing(self):
        '''Hill Climbing local search'''
        curr_node = self.__current_position
        while True:
            neighbors = self.__get_neighbors(curr_node)
            neighbor_scores = [self.__get_heuristic(neighbor) for neighbor in neighbors]
            best_neighbor = neighbors[neighbor_scores.index(max(neighbor_scores))]
            if self.__get_heuristic(best_neighbor) <= self.__get_heuristic(curr_node):
                return self.__get_path_to_node(best_neighbor)
            curr_node = best_neighbor

    def __local_plan_simulated_annealing(self):
        '''Simulated Annealing local search'''
        curr_state = self.get_current_state()
        curr_cost = self.get_cost(curr_state)
        T = self.get_temperature()
        while T > 1e-10:
            next_state = self.get_neighbor(curr_state)
            next_cost = self.get_cost(next_state)
            delta_cost = next_cost - curr_cost
            if delta_cost > 0:
                curr_state = next_state
                curr_cost = next_cost
            else:
                acceptance_probability = math.exp(delta_cost / T)
                if random.uniform(0, 1) < acceptance_probability:
                    curr_state = next_state
                    curr_cost = next_cost
            T = self.cooling_schedule(T)
        return curr_state
# Note: The get_current_state, get_cost, get_temperature, get_neighbor, and cooling_schedule methods are not defined in the code you provided and would need to be implemented for this to work.






    def get_next_move(self, current_pos, goal_pos, T, alpha):
        '''Should return a string where the string gives movement command
            (these should be in order)
            Example:
             "movenorth 1"
             XOR "movesouth 1"
             XOR "moveeast 1"
             XOR "movewest 1"
             (these are also the only four commands that can be used, you
             cannot move diagonally)
             On a 2D grid (list), "move north" would move us
             from, say, [0][0] to [1][0]
        '''
        if T <= 0:
            return current_pos
        
        next_move = None
        if random.uniform(0, 1) < 0.5:
            next_move = __local_plan_hill_climbing(current_pos, goal_pos)
        else:
            next_move = __local_plan_simulated_annealing(current_pos, goal_pos, T)
        
        if next_move == current_pos:
            return current_pos
        
        return get_next_move(next_move, goal_pos, T * alpha, alpha)


# import collections
# from queue import PriorityQueue, Queue

# class MazeAgent(object):
#     '''
#     Agent that uses path planning algorithm to figure out path to take to reach goal
#     Built for Malmo discrete environment and to use Malmo discrete movements
#     '''

#     def __init__(self, grid=None, path_alg=None):
#         '''
#         Arguments
#             grid -- (optional) a 2D list that represents the map
#             path_alg -- (optional) a string that represents path algorithm to be
#                 used. Should be "bf" or "astar"
#         '''
#         self.__frontier_set = None
#         self.__explored_set = None
#         self.__goal_state = None
#         self.__grid = grid
#         if (path_alg is None):
#             self.__path_alg = "bf"
#         else:
#             self.__path_alg = path_alg


#     def get_eset(self):
#         return self.__explored_set

#     def get_fset(self):
#         return self.__frontier_set

#     def get_goal(self): 
#         return self.__goal_state

#     def set_grid(self, grid):
#         self.__grid = grid


#     def get_neighbor(self, i, j):
#         coordinates = []
#         z_length = len(self.__grid)
#         x_length = len(self.__grid[0])

#         if i < z_length - 1:
#             coordinates.append(["north",i+1,j])
#         if i >= 1:
#             coordinates.append(["south",i-1,j])
#         if j < x_length + 1:
#             coordinates.append(["west",i,j-1])
#         if j+1 >=0:
#             coordinates.append(["east",i,j+1])
#         return coordinates


#     def __plan_path_breadth(self, curr_node, goal_node):
#         '''Breadth-First tree search
#             Arguments:
#                 curr_node -- Current node of algorithm - tuple
#                 goal_node -- The goal node to which the agent must travel - tuple
#             Returns:
#                 ordered list that gives set of commands to move to from init to
#                  goal position
#         '''

#         grid = self.__grid # 2D Array
#         self.__frontier_set = []
#         self.__explored_set = {( curr_node[0], curr_node[1] ): 'start'}

#         while (curr_node != goal_node):
            
#             # fetching the neighbors for the current node
#             neighbors = self.get_neighbor(curr_node[0], curr_node[1])

#             # populating frontier set
#             for pair in neighbors:
#                 self.__frontier_set.append(pair)


#             for i in range(len(neighbors)):

#                 popped_node = self.__frontier_set.pop(0)

#                 # if popped node is not in explored set; the node has grid value = 1
#                 if ( (popped_node[1], popped_node[2]) not in self.__explored_set ) and (self.__grid[ popped_node[1] ][ popped_node[2] ] == 1):
                    
#                     self.__explored_set[ (popped_node[1], popped_node[2]) ] = popped_node[ 0 ] # coordinates: direction => (i, j): north
#                     neighbor = self.get_neighbor( popped_node[1], popped_node[2] )
#                     for pair in neighbor:
#                         self.__frontier_set.append(pair)
#                     curr_node = (popped_node[1], popped_node[2])
#                     continue
                
#                 # if popped node is not in explored set; the node has grid value = 0
#                 elif ( (popped_node[1], popped_node[2]) not in self.__explored_set ) and (self.__grid[ popped_node[1] ][ popped_node[2] ] == 0):
#                     continue
                
#                 # if popped node is in explored set
#                 elif ( (popped_node[1], popped_node[2]) in self.__explored_set ):
#                     continue





#         lst = self.__grid
#         (i,j) = curr_node
#         self.__frontier_set = [' ']
#         self.__explored_set = {(i, j): 'start'}

#         # self.__frontier_set.append([ "start", i, j ])

#         while self.__frontier_set != []:


#             # to remove the first ' ' element from the frontier set (just to enter the While Loop)
#             if (len(self.__frontier_set) == 1) and (self.__frontier_set[0] == ' '):
#                 self.__frontier_set.clear()

#             # fetching the neighbors for the current node
#             neighbors = self.get_neighbor(curr_node[0], curr_node[1])
            
#             # populating frontier set
#             for pair in neighbors:
#                 # if tuple(pair[1:]) not in self.__explored_set:
#                 self.__frontier_set.append(pair)
            
            
#             # exploring the set
#             popped = self.__frontier_set.pop(0)
#             print(popped)
#             self.__explored_set[tuple(popped[1:])] = popped[0]

#             # changind the current node to the one which is explored
#             curr_node = (popped[1], popped[2])
            
#             # if the goal node is found
#             if(tuple(popped[1:]) == goal_node):
#                 lst = []
#                 for pair in self.__explored_set:
#                     lst.append("move" + self.__explored_set[pair] + " 1")
#                 return lst[1:]

        
                    
                    

#     def __plan_path_astar(self, curr_node, goal_node):
#         '''A* tree searchReturns:
#             ordered list that gives set of commands to move to from init to
#              goal position

#             Arguments:
#                 curr_node -- current node to be processed (may be initial node)
#                 goal_node -- goal node to be tested
#             Returns:
#                 ordered list that gives set of commands to move to from init to
#                  goal position
#         '''

#         #set up g_score and h_score
#         start = curr_node
#         g_score= {}
#         f_score ={} 
#         for i in range(len(self.__grid)):
#             for j in range(len(self.__grid[i])):
#                 g_score[(i, j)]= float('inf')
#                 f_score[(i, j)] =float('inf') 
#         g_score[start] = 0
#         f_score[start] = self.manhattan(start, goal_node)

#         #set up frontier and explore set
#         self.__frontier_set= PriorityQueue()
#         self.__frontier_set.put(((f_score[start], f_score[start]), start))
#         self.__explored_set = {}

#         #go until at goal node or set is empty(i.e no path)
#         while not self.__frontier_set.empty():
#             curr_node = self.__frontier_set.get()[1]
#             print(curr_node)
#             if curr_node == goal_node:
#                 break
            
#             #check all four directions for potential nodes and add them to the sets
#             if curr_node[0] is not 0 and self.__grid[curr_node[0]-1][curr_node[1]]  in  [1, 3] and (curr_node[0]-1, curr_node[1]) not in self.__explored_set:
#                 childCell = (curr_node[0]-1, curr_node[1])
#                 temp_g_score=g_score[curr_node]+1
#                 temp_f_score=temp_g_score+self.manhattan(childCell,(1,1))
#                 if temp_f_score < f_score[childCell]:
#                     g_score[childCell]= temp_g_score
#                     f_score[childCell]= temp_f_score
#                     self.__frontier_set.put(((temp_f_score,self.manhattan(childCell,(1,1))),childCell))
#                     self.__explored_set[childCell]=curr_node
            
#             if curr_node[0] is not len(self.__grid)-1 and self.__grid[curr_node[0]+1][curr_node[1]]  in  [1, 3] and (curr_node[0]+1, curr_node[1]) not in self.__explored_set:
#                 childCell = (curr_node[0]+1, curr_node[1])
#                 temp_g_score=g_score[curr_node]+1
#                 temp_f_score=temp_g_score+self.manhattan(childCell,(1,1))
#                 if temp_f_score < f_score[childCell]:
#                     g_score[childCell]= temp_g_score
#                     f_score[childCell]= temp_f_score
#                     self.__frontier_set.put(((temp_f_score,self.manhattan(childCell,(1,1))),childCell))
#                     self.__explored_set[childCell]=curr_node
            
#             if curr_node[1] is not 0 and self.__grid[curr_node[0]][curr_node[1]-1]  in  [1, 3] and (curr_node[0], curr_node[1]-1) not in self.__explored_set:
#                 childCell = (curr_node[0], curr_node[1]-1)
#                 temp_g_score=g_score[curr_node]+1
#                 temp_f_score=temp_g_score+self.manhattan(childCell,(1,1))
#                 if temp_f_score < f_score[childCell]:
#                     g_score[childCell]= temp_g_score
#                     f_score[childCell]= temp_f_score
#                     self.__frontier_set.put(((temp_f_score,self.manhattan(childCell,(1,1))),childCell))
#                     self.__explored_set[childCell]=curr_node

#             if curr_node[1] is not len(self.__grid[0])-1 and self.__grid[curr_node[0]][curr_node[1]+1]   in  [1, 3] and (curr_node[0], curr_node[1]+1) not in self.__explored_set:
#                 childCell = (curr_node[0], curr_node[1]+1)
#                 temp_g_score=g_score[curr_node]+1
#                 temp_f_score=temp_g_score+self.manhattan(childCell,(1,1))
#                 if temp_f_score < f_score[childCell]:
#                     g_score[childCell]= temp_g_score
#                     f_score[childCell]= temp_f_score
#                     self.__frontier_set.put(((temp_f_score,self.manhattan(childCell,(1,1))),childCell))
#                     self.__explored_set[childCell]=curr_node

                    
#         # recreate the path without excess checked nodes
#         solMap={}
#         tempCell=self.get_goal()
#         while tempCell!= start:
#             solMap[self.__explored_set[tempCell]]=tempCell
#             tempCell=self.__explored_set[tempCell]

#         #translate path into directions and return
#         directions=[]
#         current = start
#         next = solMap[start]
#         for i in range(len(solMap)-1):
#             if next[0]<current[0]:
#                 directions.insert(0, "movesouth 1")
#             if next[0]>current[0]:
#                 directions.insert(0, "movenorth 1")
#             if next[1]<current[1]:
#                 directions.insert(0, "moveeast 1")
#             if next[1]>current[1]:
#                 directions.insert(0, "movewest 1")
#             current = next
#             next = solMap[current]

#         return directions

#     def get_path(self, curr_node, goal_node):
#         '''should return list of strings where each string gives movement command
#             (these should be in order)
#             Example:
#              ["movenorth 1", "movesouth 1", "moveeast 1", "movewest 1"]
#              (these are also the only four commands that can be used, you
#              cannot move diagonally)
#              On a 2D grid (list), "move north" would move us
#              from, say, [0][0] to [1][0]
#         '''
#         if self.__path_alg == "bf":
#             return self.__plan_path_breadth(curr_node, goal_node)
#         elif self.__path_alg == "astar":
#             return self.__plan_path_astar(curr_node, goal_node)

# # We don't have to worry about this right now, but if you wanted to increase your difficulty (in the sense you NEED MORE THINGS TO DO), this isn't a bad place to start!
# class OnlineMazeAgent(object):
#     '''
#     Agent that uses online search algorithms to figure out path to take to reach goal
#     Built for Malmo discrete environment and to use Malmo discrete movements
#     '''

#     def __init__(self, grid=None):
#         '''
#         Arguments
#             grid -- (optional) a 2D list that represents the map
#         '''
#         self.__frontier_set = None
#         self.__explored_set = None
#         self.__goal_state = None
#         self.__grid = grid


#     def get_eset(self):
#         return self.__explored_set

#     def get_fset(self):
#         return self.__frontier_set

#     def get_goal(self):
#         return self.__goal_state

#     def set_grid(self, grid):
#         self.__grid = grid

#     def __local_plan_hill_climbing(self):
#         '''Hill Climbing local search'''
#         pass

#     def __local_plan_simulated_annealing(self):
#         '''Simulated Annealing local search'''
#         pass

#     def get_next_move(self):
#         '''Should return a string where the string gives movement command
#             (these should be in order)
#             Example:
#              "movenorth 1"
#              XOR "movesouth 1"
#              XOR "moveeast 1"
#              XOR "movewest 1"
#              (these are also the only four commands that can be used, you
#              cannot move diagonally)
#              On a 2D grid (list), "move north" would move us
#              from, say, [0][0] to [1][0]
#         '''
#         pass
