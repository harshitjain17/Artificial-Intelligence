import python_actr
from python_actr.lib import grid
#from python_actr import *

import random

mymap="""
##########
#DDDDDDDC#
#DDDDDDDD#
#DDDDDDDD#
#DDDDDDDD#
#DDDDDDDD#
#DDDDDDDD#
#DDDDDDDD#
##########
"""

my_log = python_actr.log()#data=True, directory="/Users/cld5070/teaching-repos/AI-Course/RBES")

class MyCell(grid.Cell):
	dirty=False
	chargingsquare=False
	def color(self):
		if self.chargingsquare: return "green"
		elif self.dirty: return 'brown'
		elif self.wall: return 'black'
		else: return 'white'

	def load(self,char):
		if char=='#': self.wall=True
		elif char=='D': self.dirty=True
		elif char=='C': self.chargingsquare=True

class MotorModule(python_actr.Model):
	FORWARD_TIME = .1
	FORWARD_ENERGY_COST = 1
	TURN_TIME = 0.025
	TURN_ENERGY_COST = 1
	CLEAN_TIME = 0.025
	CLEAN_ENERGY_COST = 1
	INIT_ENERGY = 35

	def __init__(self):
		python_actr.Model.__init__(self)
		self.busy=False
		self.energy=MotorModule.INIT_ENERGY

	def turn_left(self, amount=1):
		if self.busy: return
		self.busy=True
		self.action="turning left"
		amount *= -1
		self.parent.body.turn(amount)
		yield MotorModule.TURN_TIME
		self.busy=False

	def turn_right(self, amount=1):
		if self.busy: return
		self.busy=True
		self.action="turning left"
		self.parent.body.turn(amount)
		yield MotorModule.TURN_TIME
		self.busy=False

	def turn_around(self):
		if self.busy: return
		self.busy=True
		self.action="turning around"
		self.parent.body.turn_around()
		yield MotorModule.TURN_TIME
		self.busy=False

	def go_forward(self, dist=1):
		if self.busy: return
		self.busy=True
		self.action="going forward"
		for i in range(dist):
			self.parent.body.go_forward()
			yield MotorModule.FORWARD_TIME
		self.action=None
		self.busy=False

	def go_left(self,dist=1):
		if self.busy: return
		self.busy=True
		self.action='turning left'
		yield MotorModule.TURN_TIME
		self.parent.body.turn_left()
		self.action="going forward"
		for i in range(dist):
			self.parent.body.go_forward()
			yield MotorModule.FORWARD_TIME
		self.action=None
		self.busy=False

	def go_right(self):
		if self.busy: return
		self.busy=True
		self.action='turning right'
		yield 0.1
		self.parent.body.turn_right()
		self.action='going forward'
		self.parent.body.go_forward()
		yield MotorModule.FORWARD_TIME
		self.action=None
		self.busy=False

	def go_towards(self,x,y):
		if self.busy: return
		self.busy=True
		self.clean_if_dirty()
		self.action='going towards %s %s'%(x,y)
		yield MotorModule.FORWARD_TIME
		self.parent.body.go_towards(x,y)
		self.action=None
		self.busy=False

	def clean_if_dirty(self):
		"Clean cell if dirty"
		if (self.energy < 5):
			print("EnergyLow!")
			self.action=None
		if (self.parent.body.cell.dirty):
			self.action="cleaning cell"
			self.clean()

	def clean(self):
		self.energy -= MotorModule.CLEAN_ENERGY_COST
		self.parent.body.cell.dirty=False
		my_log.clean_at = (self.parent.body.x, self.parent.body.y)
		#After we add our agent to the world, the world makes the agent's parent itself.
		#Check if our world is clean (and thus can stop the simulation)
		if (self.parent.parent.check_clean()):
			self.stop()
		yield MotorModule.CLEAN_TIME



class ObstacleModule(python_actr.ProductionSystem):
	production_time=0

	def init():
		self.ahead=body.ahead_cell.wall
		self.left=body.left90_cell.wall
		self.right=body.right90_cell.wall
		self.left45=body.left_cell.wall
		self.right45=body.right_cell.wall


	def check_ahead(self='ahead:False',body='ahead_cell.wall:True'):
		self.ahead=True

	def check_left(self='left:False',body='left90_cell.wall:True'):
		self.left=True

	def check_left45(self='left45:False',body='left_cell.wall:True'):
		self.left45=True

	def check_right(self='right:False',body='right90_cell.wall:True'):
		self.right=True

	def check_right45(self='right45:False',body='right_cell.wall:True'):
		self.right45=True

	def check_ahead2(self='ahead:True',body='ahead_cell.wall:False'):
		self.ahead=False

	def check_left2(self='left:True',body='left90_cell.wall:False'):
		self.left=False

	def check_left452(self='left45:True',body='left_cell.wall:False'):
		self.left45=False

	def check_right2(self='right:True',body='right90_cell.wall:False'):
		self.right=False

	def check_right452(self='right45:True',body='right_cell.wall:False'):
		self.right45=False

class CleanSensorModule(python_actr.ProductionSystem):
	production_time = 0
	dirty=False

	def found_dirty(self="dirty:False", body="cell.dirty:True"):
		self.dirty=True

	def found_clean(self="dirty:True", body="cell.dirty:False"):
		self.dirty=False
