import python_actr
import math

from . import cellular

Cell = cellular.Cell


class World(cellular.World, python_actr.Model):
	rate = 1
	fade_time = 0.5

	def __init__(self, cell=None, width=None, height=None, directions=8, filename=None, map=None, **keys):
		cellular.World.__init__(
			self, cell, width, height, directions, filename, map)
		python_actr.Model.__init__(self, **keys)

	def start(self):
		while True:
			self.update()
			self._update_time = self.now()
			yield self.rate

	def add(self, agent, *arg, **args):
		if isinstance(agent, python_actr.Model):
			self._ensure_converted()
			agent.parent = self
			agent._ensure_converted()
			if hasattr(agent, 'body'):
				agent = agent.body
		cellular.World.add(self, agent, *arg, **args)

	#Added by Chris Dancy to check and see if we've cleaned the whole board
	def check_clean(self, dirty_color="brown"):
		for x in range(self.width):
			for y in range(self.height):
				if (self.grid[y][x].color() == "brown"):
					return False
		return True


def list_pts(x0, y0, x1, y1):
	steep = abs(y1 - y0) > abs(x1 - x0)
	if steep:
		x0, y0 = y0, x0
		x1, y1 = y1, x1
	if x0 > x1:
		x0, x1 = x1, x0
		y0, y1 = y1, y0
	deltax = x1 - x0
	if deltax == 0:
		for y in range(y0, y1):
			if steep:
				yield (y, x0)
			else:
				yield (x0, y)
		return

	deltay = abs(y1 - y0)
	error = 0
	deltaerr = float(deltay) / deltax
	y = y0
	if y0 < y1:
		ystep = 1
	else:
		ystep = -1
	for x in range(x0, x1 + 1):
		if steep:
			yield (y, x)
		else:
			yield (x, y)
		error += deltaerr
		if error > 0.5:
			y += ystep
			error -= 1.0


class Body(python_actr.Model, cellular.Agent):
	def __init__(self):
		python_actr.Model.__init__(self)
		print("Initialized")

	def __setattr__(self, key, value):
		if key == 'cell':
			if value is None:
				self.x = None
				self.y = None
			else:
				self.x = value.x
				self.y = value.y
		python_actr.Model.__setattr__(self, key, value)

	def _list_visible_objects(self):
		print("Objects")
		for row in self.world.grid:
			for cell in row:
				for x, y in list_pts(self.cell.x, self.cell.y, cell.x, cell.y):
					obs = self.world.grid[y][x]
					if obs.wall:
						break
				else:
					yield cell
		for obj in self.world.agents:
			for x, y in list_pts(self.cell.x, self.cell.y, obj.cell.x, obj.cell.y):
				obs = self.world.grid[y][x]
				if obs.wall:
					break
			else:
				yield obj

class VisionScanner(python_actr.Model):
	def __init__(self, body, visual, scan_time=0.01):
		python_actr.Model.__init__(self)
		self._visual = visual
		self._body = body
		self.scan_time = scan_time

	def start(self):
		for obj in self._body._list_visible_objects():
			if hasattr(obj, 'cell'):
				if getattr(obj, 'x', None) != obj.cell.x:
					obj.x = obj.cell.x
				if getattr(obj, 'y', None) != obj.cell.y:
					obj.y = obj.cell.y
			try:
				ox, oy = obj.x, obj.y
				x, y = self._body.x, self._body.y
				salience = self.salience(ox - x, oy - y)
			except AttributeError:
				salience = 1

			self._visual.add(obj)
		# Modified by Chris Dancy
		# Any agents in the environment are now included in the list of items returned
		#  May want to remove ground object at same location in future
		try:
			for agent in self._body.world.agents:
				try:
					ox, oy = agent.x, agent.y
					x, y = self._body.x, self._body.y
					salience = self.salience(ox - x, oy - y)
				except AttributeError:
					salience = 1
		except AttributeError:
			pass

		yield self.scan_time


	def salience(self, dx, dy):
		dist = dx * dx + dy * dy
		s = 4 / (math.sqrt(dist) + 1)
		if s > 1:
			s = 1
		return s
