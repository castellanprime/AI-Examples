#!/usr/bin/env python

"""
File: othello.py
Date: Sept 17. 2016
Author: Okusanya David
Brief: An Othello game-playing AI with the minimax algorithm
"""

#from collections import OrderedDict
#keeping insertion order, generate a unique list
#self.white_currPos = list(OrderedDict.fromkeys(self.white_currPos))

class Othello:
	"""Othello game"""

	_PLAYER_BLACK = 1
	_PLAYER_WHITE = 2

	""" A board is an 8 x 8 matrix of squares """
	_gameboard = [[0 for n in range(10)] for n in range(10)]

	# These are hardcorded values
	_validpositions = [(row, col) for row in range(1, 9) for col in range(1, 9)]

	_edges = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1) ,(7, 1), (8, 1),
			(1, 2), (1, 3),(1, 4), (1, 5), (1, 6), (1, 7), (2, 8), (3, 8), (4, 8), (5, 8), 
			(6, 8), (7, 8), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)]

	_corners = [(1, 1),(8, 8), (8, 1), (1, 8)]

	# This is just for representation/state objects purposes
	#_position_value_board = {value: [k, 0] for k, value in enumerate(_validpositions)}

	
	ERROR = "invalid move"
	NO_MOVE = "no moves available"
	SUCCESS = "valid move"

	def __init__(self):
		self.setUp()
		self._gameboard[4][4] = self._PLAYER_WHITE
		self._gameboard[4][5] = self._PLAYER_BLACK
		self._gameboard[5][4] = self._PLAYER_BLACK
		self._gameboard[5][5] = self._PLAYER_WHITE

	def setUp(self):
		for row, value in enumerate(self._gameboard):
			value[0] = "*"
			value[-1] = "*"
		self._gameboard[0] = ["*" for n in range(len(self._gameboard[0]))]
		self._gameboard[-1] = ["*" for n in range(len(self._gameboard[-1]))]
		self.white_curr_pos = []
		self.black_curr_pos = []
		

	# Making the class variables immutable
	@property
	def PLAYER_BLACK(self):
		return type(self)._PLAYER_BLACK	

	@property
	def PLAYER_WHITE(self):
		return type(self)._PLAYER_WHITE	

	def _validate_player(self, player):
		if player not in (self._PLAYER_WHITE, self._PLAYER_BLACK):
			raise ValueError("Player can only be PLAYER_BLACK(=1) or PLAYER_WHITE(=2)")

	def _validate_position(self, position):
		if position not in self._validpositions:
			raise ValueError("Position not valid")

	def setPosition(self, player, position):
		self._gameboard[position[0]][position[1]] = player 

	def allPositions(self, player):
		self._validate_player(player)
		results = []
		if player == self._PLAYER_WHITE:
			if len(self.white_curr_pos) == 0:
				for idx in range(1, len(self._gameboard)- 1):
					for col in range(1, len(self._gameboard[idx]) - 1):
						if self._gameboard[idx][col] == player:
							results.append((idx, col))
				self.white_curr_pos.append(results)
				self.white_curr_pos = [value[n] for idx, value in enumerate(self.white_curr_pos) for n in range(len(value))]
				return self.white_curr_pos
			else:
				return self.white_curr_pos
		elif player == self._PLAYER_BLACK:
			if len(self.black_curr_pos) == 0:
				for idx in range(1, len(self._gameboard)- 1):
					for col in range(1, len(self._gameboard[idx]) - 1):
						if self._gameboard[idx][col] == player:
							results.append((idx, col))
				self.black_curr_pos.append(results)
				self.black_curr_pos = [value[n] for idx, value in enumerate(self.black_curr_pos) for n in range(len(value))]
				return self.black_curr_pos
			else:
				return self.black_curr_pos

	
	def getMoves(self, position, player):
		"""
		The operator not yields True if its argument is false, False otherwise.

		The expression x and y first evaluates x; if x is false, its value is returned; otherwise, y is evaluated and the resulting value is returned.

		The expression x or y first evaluates x; if x is true, its value is returned; otherwise, y is evaluated and the resulting value is returned.
		"""
		moves = []
		row, col = position
		#s = [self._PLAYER_WHITE, self._PLAYER_BLACK]
		#opp_player = list(set(s).difference([player]))
		
		# row-i, col + i
		for i in range(1, 9):
			if col + i > 8 and row - i < 0:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row-i][col+i] == 0 or self._gameboard[row-i][col+i] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row-i][col+i] == 0 and self._gameboard[row-i+1][col+i-1] != player:
				#print("Move appended: row-i, col+i, ",row-i, col+i) 
				moves.append((row-i, col+i))
				break

		# row, col + i
		for i in range(1, 9):
			if col + i > 8:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row][col+i] == 0 or self._gameboard[row][col+i] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row][col+i] == 0 and self._gameboard[row][col+i-1] != player:
				#print("Move appended: row, col+i ", row, col+i) 
				moves.append((row, col+i))
				break

		# row-i, col - i
		for i in range(1, 9):
			if col - i < 0 or row - i < 0:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row-i][col-i] == 0 or self._gameboard[row-i][col-i] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row-i][col-i] == 0 and self._gameboard[row-i+1][col-i+1] != player: 
				#print("Move appended: row-i, col-i ", row-i, col-i)
				moves.append((row-i, col-i))
				break

		# row+i, col + i
		for i in range(1, 9):
			if col + i > 8 or  row + i > 8:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row+i][col+i] == 0 or self._gameboard[row+i][col+i] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row+i][col+i] == 0 and self._gameboard[row+i-1][col+i-1] != player:
				#print("Move appended: row+i, col+i ", row+i, col+i) 
				moves.append((row+i, col+i))
				break

		# row-i, col
		for i in range(1, 9):
			if row - i < 0:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row-i][col] == 0 or self._gameboard[row-i][col] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row-i][col] == 0 and self._gameboard[row-i+1][col] != player:
				#print("Move appended: row-i, col ", row-i, col) 
				moves.append((row-i, col))
				break

		# row, col - i
		for i in range(1, 9):
			if col - i < 0:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row][col-i] == 0 or self._gameboard[row][col-i] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row][col-i] == 0 and self._gameboard[row][col-i+1] != player:
				#print("Move appended: row, col-i ", row, col-i) 
				moves.append((row, col-i))
				break

		# row + i, col	
		for i in range(1, 9):
			if row + i > 8:
				#print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row+i][col] == 0 or self._gameboard[row+i][col] == "*"):
				#print("I broke her", row, col)
				break 
			if self._gameboard[row+i][col] == 0 and self._gameboard[row+i-1][col] != player:
				#print("Move appended: row+i, col ", row+i, col) 
				moves.append((row+i, col))
				break

		# row + i, col - i	
		for i in range(1, 9):
			if col - i < 0 or row + i > 8:
				print("I broke here", row, col)
				break
			if i == 1 and (self._gameboard[row+i][col-i] == 0 or self._gameboard[row+i][col-i] == "*"):
				print("I broke her", row, col)
				break 
			if self._gameboard[row+i][col-i] == 0 and self._gameboard[row+i-1][col-i+1] != player:
				print("Move appended: row+i, col-i ", row+i, col-i ) 
				moves.append((row+i, col-i))
				break

		return moves
	
	def getLegalMoves(self, player):
		self._validate_player(player)
		query_list = self.allPositions(player)
		print(query_list)
		results_list = []
		for position in query_list:
			results_list.append(self.getMoves(position, player))
		results_list = [value[n] for idx, value in enumerate(results_list) for n in range(len(value))]
		results_list[:] = [results_list[i] for i in range(len(results_list)) if i == results_list.index(results_list[i])] 
		print(results_list)
		return results_list
	
	def place(self, player, position_to_move):
		self._validate_player(player)
		self._validate_position(position_to_move)
		if position_to_move not in self.getLegalMoves(player):
			 return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.ERROR)
		#setPosition(player, position_to_move)
		return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.SUCCESS)
	
	def _resetBoard(self):
		self._gameboard = [[0 for n in range(10)] for n in range(10)]
		self.setUp()

	def generateBoards(self, black_list, white_list):
		self._resetBoard()
		for i in range(len(black_list)):
			self.setPosition(self._PLAYER_BLACK, black_list[i])
		for i in range(len(white_list)):
			self.setPosition(self._PLAYER_WHITE, white_list[i])

	def __str__(self):
		string = "  "
		for i in range(1, 9):
			string += "".join([" ", str(i)])
		string += "\n"

		print_list = self._gameboard[1: -1]
		for i, value in enumerate(print_list, 1):
			print_l = [["|", value[j]] for j in range(1, len(value) - 1)]
			print_l[:] = [val[n] for val in print_l for n in range(len(val))]
			string += "".join([str(i), " ", "".join(str(e) for e in print_l), "|", "\n"])
		return string

	def print_actualBoard(self):
		print(self._gameboard)


if __name__ == '__main__':
	o = Othello()
	print(o)
	white_list = [(3, 6), (4, 2), (5, 4), (5, 5), (5, 7), (5, 8), (6, 4), (7, 3)]
	black_list = [(3, 3), (3, 4), (3, 5), (3, 8), (4, 3),(4, 4), (4, 5), (4, 6),
				(4, 7), (5, 2), (5, 3), (5, 6), (6, 5), (6, 6), (7, 5)]
	o.generateBoards(black_list, white_list)
	print(o)
	#print(o.allPositions(o.PLAYER_BLACK))
	#print(o.allPositions(o.PLAYER_WHITE))
	print(o.place(o.PLAYER_WHITE, (8, 2)))
