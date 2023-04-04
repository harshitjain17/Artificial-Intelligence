from queue import PriorityQueue

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

    def __plan_path_breadth(self, curr_node, goal_node):
        '''Breadth-First tree search
            Arguments:
                curr_node -- Current node of algorithm
                goal_node -- The goal node to which the agent must travel
            Returns:
                ordered list that gives set of commands to move to from init to
                 goal position
        '''

        self.__explored_set = [curr_node]
        self.__frontier_set = [curr_node]
        start = curr_node
        reverse_path = {}

        while len(self.__frontier_set) > 0:
            curr_node = self.__frontier_set.pop(0)
            
            # if goal found
            if curr_node == goal_node:
                break
            
            # checking all 4 neighborhood nodes
            if (curr_node[0] != 0) and (self.__grid[curr_node[0]-1][curr_node[1]] in [1, 3]) and ((curr_node[0]-1, curr_node[1]) not in self.__explored_set):
                self.__frontier_set.append((curr_node[0]-1, curr_node[1]))
                self.__explored_set.append((curr_node[0]-1, curr_node[1]))
                reverse_path[(curr_node[0]-1, curr_node[1])] = curr_node
            
            if (curr_node[0] != len(self.__grid)-1) and (self.__grid[curr_node[0]+1][curr_node[1]] in [1, 3]) and ((curr_node[0]+1, curr_node[1]) not in self.__explored_set):
                self.__frontier_set.append((curr_node[0]+1, curr_node[1]))
                self.__explored_set.append((curr_node[0]+1, curr_node[1]))
                reverse_path[(curr_node[0]+1, curr_node[1])] = curr_node
            
            if (curr_node[1] != 0) and (self.__grid[curr_node[0]][curr_node[1]-1] in [1, 3]) and ((curr_node[0], curr_node[1]-1) not in self.__explored_set):
                self.__frontier_set.append((curr_node[0], curr_node[1]-1))
                self.__explored_set.append((curr_node[0], curr_node[1]-1))
                reverse_path[(curr_node[0], curr_node[1]-1)] = curr_node
            
            if (curr_node[1] != len(self.__grid[0])-1) and (self.__grid[curr_node[0]][curr_node[1]+1] in [1, 3]) and ((curr_node[0], curr_node[1]+1) not in self.__explored_set):
                self.__frontier_set.append((curr_node[0], curr_node[1]+1))
                self.__explored_set.append((curr_node[0], curr_node[1]+1))
                reverse_path[(curr_node[0], curr_node[1]+1)] = curr_node

        #recreate the solution from reverse path
        solution={}
        temporary_node=self.get_goal()
        while temporary_node!= start:
            solution[reverse_path[temporary_node]]=temporary_node
            temporary_node=reverse_path[temporary_node]

        directions = []

        # fetching the directions from the path made
        current = start
        next = solution[start]

        for j in range(len(solution)-1):
            
            if (next[0] < current[0]):
                directions.insert(0, "movesouth 1")
            
            elif (next[0] > current[0]):
                directions.insert(0, "movenorth 1")
            
            elif (next[1] < current[1]):
                directions.insert(0, "moveeast 1")
            
            elif (next[1] > current[1]):
                directions.insert(0, "movewest 1")
            
            current = next
            next = solution[current]

        return directions


    #calculate distance
    def calculate_h_x(self, node1, node2):
        (x1, y1) = node1
        (x2, y2) = node2

        return abs(x1 - x2) + abs(y1 - y2)

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
        
        # set up g_score and f_score and other needed variable
        start = curr_node
        rows = len(self.__grid)
        columns = len(self.__grid[0])
        
        # initialize explored set and previous nodes
        self.__explored_set = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(False)
            self.__explored_set.append(row)

        previous = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(None)
            previous.append(row)

        
        # initialize g_score and f_score for each node in the grid
        g_score = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(float('inf'))
            g_score.append(row)
        g_score[start[0]][start[1]] = 0

        f_score = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(float('inf'))
            f_score.append(row)
        f_score[start[0]][start[1]] = self.calculate_h_x(start, goal_node)
        
        # initialize the frontier with the starting node
        self.__frontier_set = [(f_score[start[0]][start[1]], start)]
        path = [] 

        # loop as long as frontier is not empty
        while self.__frontier_set:

            # set current node
            current_f_score, current_pos = min(self.__frontier_set)

            # checking if goal is reached
            if (current_pos == goal_node):
                path = [current_pos]
                while previous[current_pos[0]][current_pos[1]] is not None:
                    current_pos = previous[current_pos[0]][current_pos[1]]
                    path.append(current_pos)
                path = path[::-1]
                
                # translate path into directions
                directions = []
                for i in range(len(path)-1):
                    current_pos = path[i]
                    next = path[i+1]
                    if (next[0] < current_pos[0]):
                        directions.append("movesouth 1")
                    if (next[0] > current_pos[0]):
                        directions.append("movenorth 1")
                    if (next[1] < current_pos[1]):
                        directions.append("moveeast 1")
                    if (next[1] > current_pos[1]):
                        directions.append("movewest 1")
                
                directions.reverse()
                return directions
            
            # compute neccesarry changes to sets and calculate respective heuristics
            self.__frontier_set.remove((current_f_score, current_pos))
            self.__explored_set[current_pos[0]][current_pos[1]] = True
            
            # check the neighbors of the current node
            for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current_pos[0] + d_row, current_pos[1] + d_col)
                if (neighbor[0] < 0) or (neighbor[0] >= rows) or (neighbor[1] < 0) or (neighbor[1] >= columns):
                    continue
                if (self.__grid[neighbor[0]][neighbor[1]] == 0):
                    continue
                if (self.__explored_set[neighbor[0]][neighbor[1]]):
                    continue
                
                tentative_g_score = g_score[current_pos[0]][current_pos[1]] + 1

                if tentative_g_score < g_score[neighbor[0]][neighbor[1]]:
                    previous[neighbor[0]][neighbor[1]] = current_pos
                    g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                    f_score[neighbor[0]][neighbor[1]] = tentative_g_score + self.calculate_h_x(neighbor, goal_node)
                    
                    if (f_score[neighbor[0]][neighbor[1]], neighbor) not in self.__frontier_set:
                        self.__frontier_set.append((f_score[neighbor[0]][neighbor[1]], neighbor))
        
        # if no path is found return empty set
        return []




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

        # Find goal and start nodes
        for i in range(len(self.__grid)): 
            
            for j in range(len(self.__grid[i])):
                
                if self.__grid[i][j] not in [0, 1, 2]:
                    self.__goal_state=(i,j)
                
                if self.__grid[i][j] not in [0, 1, 3]:
                    current_state=(i,j)

        # find respective path and return
        path = self.__plan_path_astar(current_state, self.__goal_state)
        return path


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
        pass

    def __local_plan_simulated_annealing(self):
        '''Simulated Annealing local search'''
        pass

    def get_next_move(self):
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
        pass