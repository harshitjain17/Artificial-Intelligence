'''
 Modified from Maze python example by Chris Dancy @ Bucknell University for
 AI & Cognitive Science course
'''

import os, random, argparse, sys, time, json, errno
import malmoenv
from MazeAgent import MazeAgent

class MazeSim():
	MAP_SIZE = 60
	MS_PER_TICK = 50

	FLOOR_BLOCK = "grass"
	GAP_BLOCK = "stone"
	PATH_BLOCK = "sandstone"
	START_BLOCK = "emerald_block"
	GOAL_BLOCK = "gold_block"

	#Canvas params
	CANVAS_BORDER = 20
	CANVAS_WIDTH = 400
	CANVAS_HEIGHT = CANVAS_BORDER + ((CANVAS_WIDTH - CANVAS_BORDER))
	CANVAS_SCALEX = (CANVAS_WIDTH-CANVAS_BORDER)/MAP_SIZE
	CANVAS_SCALEY = (CANVAS_HEIGHT-CANVAS_BORDER)/MAP_SIZE
	CANVAS_ORGX = -MAP_SIZE/CANVAS_SCALEX
	CANVAS_ORGY = -MAP_SIZE/CANVAS_SCALEY

	DEFAULT_MAZE = '''
		<MazeDecorator>
			<SizeAndPosition length="''' + str(MAP_SIZE-1) + '''"\
				width="''' + str(MAP_SIZE-1) + '''" \
				yOrigin="225" zOrigin="0" height="180"/>
			<GapProbability variance="0.4">0.5</GapProbability>
			<Seed>15</Seed>
			<MaterialSeed>random</MaterialSeed>
			<AllowDiagonalMovement>false</AllowDiagonalMovement>
			<StartBlock fixedToEdge="true" type="emerald_block"/>
			<EndBlock fixedToEdge="true" type="''' + GOAL_BLOCK + '''" height="12"/>
			<PathBlock type="''' + PATH_BLOCK + '''" colour="WHITE ORANGE MAGENTA LIGHT_BLUE YELLOW LIME PINK GRAY SILVER CYAN PURPLE BLUE BROWN GREEN RED BLACK" height="1"/>
			<FloorBlock type="''' + FLOOR_BLOCK + '''"/>
			<GapBlock type="'''+ GAP_BLOCK + '''" height="2"/>
			<AddQuitProducer description="finished maze"/>
		</MazeDecorator>
	'''

	def __init__(self, maze_str=None, agent=None):
		if (not(maze_str is None)):
			self.__maze_str = maze_str
		else:
			self.__maze_str = MazeSim.DEFAULT_MAZE

		self.__maze_grid = [["Empty" for x in range(MazeSim.MAP_SIZE)] \
							for x in range(MazeSim.MAP_SIZE)]
		self.agent = agent

	def get_mission_xml(self):
		return '''<?xml version="1.0" encoding="UTF-8" ?>
		<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			<About>
				<Summary>Run the maze!</Summary>
			</About>

			<ModSettings>
				<MsPerTick>''' + str(MazeSim.MS_PER_TICK) + '''</MsPerTick>
			</ModSettings>

			<ServerSection>
				<ServerInitialConditions>
					<AllowSpawning>false</AllowSpawning>
				</ServerInitialConditions>
				<ServerHandlers>
					<FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
					''' + self.__maze_str + '''
					<ServerQuitFromTimeUp timeLimitMs="45000"/>
					<ServerQuitWhenAnyAgentFinishes />
				</ServerHandlers>
			</ServerSection>

			<AgentSection mode="Survival">
				<Name>A* Smart Guy</Name>
				<AgentStart>
					<Placement x="10" y="228" z="1"/>
				</AgentStart>
				<AgentHandlers>
					<VideoProducer want_depth="false">
						<Width>640</Width>
						<Height>480</Height>
					</VideoProducer>
					<ObservationFromGrid>
						<Grid name="World" absoluteCoords="true">
							<min x="0" y="226" z="0"/>
							<max x="''' + str(MazeSim.MAP_SIZE-1) + \
							'''" y="226" z="''' + str(MazeSim.MAP_SIZE-1) + '''"/>
						</Grid>
					</ObservationFromGrid>
					<DiscreteMovementCommands />
				</AgentHandlers>
			</AgentSection>

		</Mission>'''

	def __fill_grid(self, observations):
		'''
		Converts observation string grid (which is flat) into 2D list of observations
		This simplifies the list so that the initial location is marked with a 2,
		goal location is marked with a 3,
		 all invalid locations/blocks are marked with a 0,
		 and all valid moves/blocks are marked with a 1
		Arguments:
			observations -- list of strings in order by a flattened grid
		'''
		flat_grid_max = len(observations)
		grid_max = len(self.__maze_grid)
		for i in range(flat_grid_max):
			curr_row = ((flat_grid_max-1)-i)//grid_max
			curr_col = ((flat_grid_max-1)-i)%grid_max
			self.__maze_grid[curr_row][curr_col] = self.conv_obs_str(observations[i])

	def conv_obs_str(self, obs_str):
		'''
		Converts a given object string to the numerical representation for our
		 grid according to a few simple tests
		'''
		if (obs_str == MazeSim.GOAL_BLOCK):
			return 3
		elif (obs_str == MazeSim.START_BLOCK):
			return 2
		elif (obs_str == MazeSim.PATH_BLOCK):
			return 1
		else:
			return 0

	def create_actions(self):
		'''Returns dictionary of actions that make up agent action space (discrete movements)
		'''
		actions = [0] * 5
		actions[0] = "movenorth 1"
		actions[1] = "moveeast 1"
		actions[2] = "movesouth 1"
		actions[3] = "movewest 1"
		actions[4] = "move 0"

		return (actions)


	def run_sim(self, exp_role, num_episodes, port1, serv1, serv2, exp_id, epi, rsync):
		'''Code to actually run simulation
		'''
		validate = True
		movements = None

		env = malmoenv.make()

		env.init(self.get_mission_xml(),
				 port1, server=serv1,
				 server2=serv2, port2=(port1 + exp_role),
				 role=exp_role,
				 exp_uid=exp_id,
				 episode=epi,
				 resync=rsync,
				 action_space = malmoenv.ActionSpace(self.create_actions()))

		max_num_steps = 1000

		for r in range(num_episodes):
			print("Reset [" + str(exp_role) + "] " + str(r) )
			movements = None
			max_retries = 3

			env.reset()
			num_steps = 0

			sim_done = False
			total_reward = 0
			total_commands = 0

			(obs, reward, sim_done, info) = env.step(4)
			while not sim_done:
				num_steps += 1

				if (info is None or len(info) == 0):
					(obs, reward, sim_done, info) = env.step(4)
				elif (movements is None):
					info_json = json.loads(info)
					self.__fill_grid(info_json["World"])
					self.__maze_grid

					self.agent.set_grid(self.__maze_grid)

					#You need to make it so this works! :-)
					if (movements is None):
						movements = self.agent.get_path()
						print(movements)
						print(len(movements))

				else:
					try:
						#Moves are presented in reverse order (last move 1st)
						next_move = movements.pop()
						(obs, reward, sim_done, info) = env.step(env.action_space.actions.index(next_move))
					except RuntimeError as e:
						print("Issue with command/action: ",e)
						pass
				time.sleep(0.05)


			#print "Mission has stopped."
			time.sleep(0.5) # Give mod a little time to get back to dormant state.

# Change the MazeAgent as needed, but that should be the only part of the code that
# you need to change
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='malmovnv test')
	parser.add_argument('--port', type=int, default=9000, help='the mission server port')
	parser.add_argument('--server', type=str, default='127.0.0.1', help='the mission server DNS or IP address')
	parser.add_argument('--server2', type=str, default=None, help="(Multi-agent) role N's server DNS or IP")
	parser.add_argument('--port2', type=int, default=9000, help="(Multi-agent) role N's mission port")
	parser.add_argument('--episodes', type=int, default=10, help='the number of resets to perform - default is 1')
	parser.add_argument('--episode', type=int, default=0, help='the start episode - default is 0')
	parser.add_argument('--resync', type=int, default=0, help='exit and re-sync on every N - default 0 meaning never')
	parser.add_argument('--experimentUniqueId', type=str, default='test1', help="the experiment's unique id.")
	args = parser.parse_args()
	if args.server2 is None:
		args.server2 = args.server

	#smart_guy = MazeAgent()
	smart_guy = MazeAgent(None, "astar")
	smart_guy_sim = MazeSim(agent=smart_guy)
	smart_guy_sim.run_sim(0, args.episodes, args.port, args.server, args.server2,
					args.experimentUniqueId, args.episode, args.resync)
	print(len(smart_guy.get_eset()))
	print(len(smart_guy.get_fset()))
