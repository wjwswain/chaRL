import numpy as np
import gym
from gym import spaces

class Checkers(gym.Env):
	metadata = {'render.modes': ['console']}

	def __init__(self, bankroll, name):
		super(Checkers, self).__init__()

		self.observation = 0#np...
		self.reward = 0
		self.done = False
		self.info = {}

		self.action_space = spaces.Discrete(48)
		self.observation_space = spaces.MultiBinary()

	def step(self, action):
		return self.observation, self.reward, self.done, self.info

	def reset(self):
		return self.observation

	def render(self, mode="console"):
		if mode != "console":
			raise NotImplementedError()
		else:
			pass

	def close (self):
		pass


class Board:
	def __init__(self, color):
		if color == 'B':
			self.board = [
			[Chip('W',0,0), Chip('W',0,1), Chip('W',0,2), Chip('W',0,3)],
			[Chip('W',1,0), Chip('W',1,1), Chip('W',1,2), Chip('W',1,3)],
			[Chip('W',2,0), Chip('W',2,1), Chip('W',2,2), Chip('W',2,3)],
			[Chip('E',3,0), Chip('E',3,1), Chip('E',3,2), Chip('E',3,3)],
			[Chip('E',4,0), Chip('E',4,1), Chip('E',4,2), Chip('E',4,3)],
			[Chip('B',5,0), Chip('B',5,1), Chip('B',5,2), Chip('B',5,3)],
			[Chip('B',6,0), Chip('B',6,1), Chip('B',6,2), Chip('B',6,3)],
			[Chip('B',7,0), Chip('B',7,1), Chip('B',7,2), Chip('B',7,3)]]
		else:
			self.board = [
			[Chip('B',0,0), Chip('B',0,1), Chip('B',0,2), Chip('B',0,3)],
			[Chip('B',1,0), Chip('B',1,1), Chip('B',1,2), Chip('B',1,3)],
			[Chip('B',2,0), Chip('B',2,1), Chip('B',2,2), Chip('B',2,3)],
			[Chip('E',3,0), Chip('E',3,1), Chip('E',3,2), Chip('E',3,3)],
			[Chip('E',4,0), Chip('E',4,1), Chip('E',4,2), Chip('E',4,3)],
			[Chip('W',5,0), Chip('W',5,1), Chip('W',5,2), Chip('W',5,3)],
			[Chip('W',6,0), Chip('W',6,1), Chip('W',6,2), Chip('W',6,3)],
			[Chip('W',7,0), Chip('W',7,1), Chip('W',7,2), Chip('W',7,3)]]

	def display(self):
		for row in range(8):
			chip0, chip1, chip2, chip3 = self.board[row]
			if row % 2:
				print(chip0.__str__(), '[ ]', chip1.__str__(), '[ ]', chip2.__str__(), '[ ]', chip3.__str__(), '[ ]')
			else:
				print('[ ]', chip0.__str__(), '[ ]', chip1.__str__(), '[ ]', chip2.__str__(), '[ ]', chip3.__str__())
		print()


class Chip:
	def __init__(self, color, x, y):
		self.color = color
		self.x = x
		self.y = y

	def __str__(self):
		if self.color == 'E':
			return '[ ]'
		else:
			return '['+self.color+']'
