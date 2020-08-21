import numpy as np
import random
import gym
from gym import error, spaces, utils

class ChessEnv(gym.Env):
  metadata = {'render.modes': ['console']}

  def __init__(self):
    self.turn = 'W'
    self.play = 0
    self.wboard = Board('W')
    self.bboard = Board('B')


  def step(self, action):
    return self.observation, self.reward, self.done, self.info

  def reset(self):
    return self.observation

  def render(self, mode='console', close=False):
    print(self.board)
    if self.turn == 'W':
    	print(str(self.play) + '.' + self.prevmove.record() + ' ' + self.move.record())
    	self.play += 1

  def close(self):
  	pass


class Board:
	def __init__(self, template=None):
		if template is None:
			self.board = [
				[Rook(0,0,'W'), Pawn(0,1,'W'), Empty(0,2), Empty(0,3), \
				Empty(0,4), Empty(0,5), Pawn(0,6,'B'), Rook(0,7,'B')],
				[Knight(1,0,'W'), Pawn(1,1,'W'), Empty(1,2), Empty(1,3), \
				Empty(1,4), Empty(1,5), Pawn(1,6,'B'), Knight(1,7,'B')],
				[Bishop(2,0,'W'), Pawn(2,1,'W'), Empty(2,2), Empty(2,3), \
				Empty(2,4), Empty(2,5), Pawn(2,6,'B'), Bishop(2,7,'B')],
				[Queen(3,0,'W'), Pawn(3,1,'W'), Empty(3,2), Empty(3,3), \
				Empty(3,4), Empty(3,5), Pawn(3,6,'B'), Queen(3,7,'B')],
				[King(4,0,'W'), Pawn(4,1,'W'), Empty(4,2), Empty(4,3), \
				Empty(4,4), Empty(4,5), Pawn(4,6,'B'), King(4,7,'B')],
				[Bishop(5,0,'W'), Pawn(5,1,'W'), Empty(5,2), Empty(5,3), \
				Empty(5,4), Empty(5,5), Pawn(5,6,'B'), Bishop(5,7,'B')],
				[Knight(6,0,'W'), Pawn(6,1,'W'), Empty(6,2), Empty(6,3), \
				Empty(6,4), Empty(6,5), Pawn(6,6,'B'), Knight(6,7,'B')],
				[Rook(7,0,'W'), Pawn(7,1,'W'), Empty(7,2), Empty(7,3), \
				Empty(7,4), Empty(7,5), Pawn(7,6,'B'), Rook(7,7,'B')]
			]
		else:
			self.board = template
		self.check = False
		self.checkmate = False
	def __str__(self):
		board_str = "   a   b   c   d   e   f   g   h\n"
		for row_i in range(7,-1,-1):
			row_str = str(row_i + 1) + ' '
			for col_i in range(8):
				row_str += self.board[col_i][row_i].__str__()
			board_str += row_str + '\n'
		return board_str
	def all_legal_moves(self, color):
		moves = list()
		for row in self.board:
			for piece in row:
				if piece.color == color:
					moves.extend(piece.legal_moves(self.board))
		for move in moves:
			print(move.record())
		return moves

class Piece:
	def __init__(self, char_id, x, y, color, px, py, moved=False):
		self.id = char_id
		self.x = x
		self.y = y
		self.color = color
		self.enemy = 'B'
		if self.color == 'B':
			self.enemy = 'W'
		self.moved = moved
		self.px = px
		self.py = py
	def __str__(self):
		return '[' + self.color + self.id + ']'
	def record(self):
		x_char = "abcdefgh"
		return self.id + x_char[self.x] + str(self.y+1)
	def legal_moves(self, board):
		pass

class Empty(Piece):
	def __init__(self, x, y):
		super().__init__(' ', x, y, ' ', x, y)
		self.enemy = ' '

class Pawn(Piece):
	def __init__(self, x, y, color, px=None, py=None, moved=False):
		super().__init__('P', x, y, color, px, py, moved)
	def legal_moves(self, board):
		moves = list()
		if self.color == 'B':
			vecs = [(0,-1),(0,-2),(-1,-1),(1,-1)]
		else:
			vecs = [(0,1),(0,2),(-1,1),(1,1)]
		for i, (x_vec, y_vec) in enumerate(vecs):
			x = self.x + x_vec
			y = self.y + y_vec
			if x in range(8) and y in range(8):
				cur_occ = board[x][y].color
				if i == 0:
					if cur_occ == ' ':
						moves.append(Pawn(x, y, self.color, px=self.x, py=self.y, moved=True))
					else:
						break
				elif i == 1 and not self.moved and cur_occ == ' ':
					moves.append(Pawn(x, y, self.color, px=self.x, py=self.y, moved=True))
				elif cur_occ == self.enemy:
					moves.append(Pawn(x, y, self.color, px=self.x, py=self.y, moved=True))
		return moves

class Knight(Piece):
	def __init__(self, x, y, color, px=None, py=None):
		super().__init__('N', x, y, color, px, py)
	def legal_moves(self, board):
		moves = list()
		vecs = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
		for x_vec, y_vec in vecs:
			x = self.x + x_vec
			y = self.y + y_vec
			if x in range(8) and y in range(8):
				cur_occ = board[x][y].color
				if cur_occ != self.color:
					moves.append(Knight(x, y, self.color, px=self.x, py=self.y))
		return moves

class Bishop(Piece):
	def __init__(self, x, y, color, px=None, py=None):
		super().__init__('B', x, y, color, px, py)
	def legal_moves(self, board):
		moves = list()
		vecs = [(-1,-1),(-1,1),(1,-1),(1,1)]
		for x_vec, y_vec in vecs:
			for mag in range(1,8):
				x = self.x + (x_vec*mag)
				y = self.y + (y_vec*mag)
				if x in range(8) and y in range(8):
					cur_occ = board[x][y].color
					if cur_occ != self.color:
						moves.append(Bishop(x, y, self.color, px=self.x, py=self.y))
					if cur_occ != ' ': #can't continue diagonal
						break
				else:
					break #outside board dims
		return moves				

class Rook(Piece):
	def __init__(self, x, y, color, px=None, py=None):
		super().__init__('R', x, y, color, px, py)
	def legal_moves(self, board):
		moves = list()
		vecs = [(-1,0),(0,-1),(0,1),(1,0)]
		for x_vec, y_vec in vecs:
			for mag in range(1,8):
				x = self.x + (x_vec*mag)
				y = self.y + (y_vec*mag)
				if x in range(8) and y in range(8):
					cur_occ = board[x][y].color
					if cur_occ != self.color:
						moves.append(Rook(x, y, self.color, px=self.x, py=self.y))
					if cur_occ != ' ': #can't continue line
						break
				else:
					break #outside board dims
		return moves	

class Queen(Piece):
	def __init__(self, x, y, color, px=None, py=None):
		super().__init__('Q', x, y, color, px, py)
	def legal_moves(self, board):
		moves = list()
		vecs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		for x_vec, y_vec in vecs:
			for mag in range(1,8):
				x = self.x + (x_vec*mag)
				y = self.y + (y_vec*mag)
				if x in range(8) and y in range(8):
					cur_occ = board[x][y].color
					if cur_occ != self.color:
						moves.append(Queen(x, y, self.color, px=self.x, py=self.y))
					if cur_occ != ' ': #can't continue line/diagonal
						break
				else:
					break #outside board dims
		return moves	

class King(Piece):
	def __init__(self, x, y, color, px=None, py=None):
		super().__init__('K', x, y, color, px, py)
	def legal_moves(self, board):
		moves = list()
		vecs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		for x_vec, y_vec in vecs:
			x = self.x + x_vec
			y = self.y + y_vec
			if x in range(8) and y in range(8):
				cur_occ = board[x][y].color
				if cur_occ != self.color:
					moves.append(King(x, y, self.color, px=self.x, py=self.y))
		return moves
