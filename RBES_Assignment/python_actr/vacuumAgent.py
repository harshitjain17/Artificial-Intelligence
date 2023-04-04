##------
# Code last modified by Chris Dancy @ Penn State (2023-Feb)
#  from codebase written by Terry Stewart @ University of Waterloo
# Builds environment grid-like environment and creates a vacuum agent to clean up "mud"
##------


from AgentSupport import MotorModule, CleanSensorModule, MyCell
import AgentSupport
import python_actr
from python_actr.lib import grid
import random

# Define a class for the vacuum agent that inherits from the ACT-R class
class VacuumAgent(python_actr.ACTR):
        
	# Define the necessary variables for the ACT-R model
	goal = python_actr.Buffer() 		# Define the goal buffer
	body = grid.Body() 					# Define the body object
	motorInst = MotorModule() 			# Define the motor module object
	cleanSensor = CleanSensorModule() 	# Define the clean sensor module object

	def init():
                
		# Initialize the necessary variables for the agent
		goal.set("rsearch left 1 0 1") 	# Set the initial goal for the agent
		self.home = None 				# Set the initial home position for the agent

	#----ROOMBA----#

	# Define the necessary rules for the Roomba-like agent
	def clean_cell(cleanSensor="dirty:True", utility=0.6):
                
		# Define the rule to clean the cell if the clean sensor detects dirt
		motorInst.clean()

	# Define the rule to move forward during the random search if there is no wall ahead
	def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist", motorInst="busy:False", body="ahead_cell.wall:False"):
		motorInst.go_forward()
		print(body.ahead_cell.wall)
		curr_dist = str(int(curr_dist) - 1) 				 # Update the current distance
		goal.set("rsearch left ?dist ?num_turns ?curr_dist") # Update the goal

	# Define the rule to turn left during the random search when the agent reaches the end of a row
	def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False", utility=0.1):
		motorInst.turn_left(2)
		num_turns = str(int(num_turns) + 1) 				 # Update the number of turns made
		dist = str((int(num_turns)-1)//2+1)
		goal.set("rsearch left ?dist ?num_turns ?dist") 	 # Update the goal
    
	# Define the rule to move forward during the wall-following search if there is a wall ahead
	def forward_wsearch(goal="rsearch left ?dist ?num_turns ?curr_dist", motorInst="busy:False", body="ahead_cell.wall:True"):
		print(body.ahead_cell.wall)
		curr_dist = 0				 						 # Update the current distance
		goal.set("rsearch left ?dist ?num_turns ?curr_dist") # Update the goal


# Define the world and add the agent to it
world=grid.World(MyCell,map=AgentSupport.mymap)
agent=VacuumAgent()
agent.home=()							 # Set the initial home position for the agent
world.add(agent,5,5,dir=0,color="black") # Add the agent to the world

# Set up logging and display the world
python_actr.log_everything(agent, AgentSupport.my_log)
python_actr.display(world)

# Run the simulation
world.run()