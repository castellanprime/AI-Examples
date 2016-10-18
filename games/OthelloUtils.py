#!/usr/bin/env python

"""
	This module contains the implementation of a board and 
	gamestate.

	File: OthelloUtils.py
	Date: Oct 10, 2016
	Author: Okusanya David
"""

import copy

class GameState:
	""" State object """


	# Global weights for SEF
	
	w_flip_num = 2				# weight attached to the number of flipped pieces
	w_corner_num = 1000 		# weight attached to the number of corner held by a player
	w_edge_num = 30				# weight attached to the number of edges held by a player
	w_corner_adj_num = -100		# weight attached to the corner adjacent positions held by the player
	#w_empty_adj_num = 20		# weight attached to the empty spaces related to the number

	def __init__(self, player, board, computer= False, minimax=False, weights=None):
		self.board = board
		self.turn = player
		self.next_moves = self.board.getLegalMoves(self.turn)
		self.minimax_move = None
		if weights:
			self.changeWeights(weights)
		if minimax:
			self.sef = SEF(self.board)
		else:
			self.sef = 0

	def SEF(self, board):
		""" This computes the SEF for a particular board from the following values

		Args:
			board: A gameboard
		Return:
			utility: A value that indicates how good the position is
		"""
		flip_num = self.board.getNoOfFlippedPieces(self.turn)
		corner_num = self.board.getNoOfCornerPieces(self.turn)
		edge_num = self.board.getNoOfEdgePieces(self.turn)
		corner_adj_num = self.board.getNoOfCornerAdjacentPieces(self.turn)
		#empty_adj_num = self.board.getNoOfEmptyAdjNum(self.turn)

		return (w_flip_num * flip_num) + (w_corner_num * corner_num) + (w_edge_num * edge_num) + (w_corner_adj_num * corner_adj_num) 

	def setMinimaxMove(self, move):
		self.minmax_move = move

	def changeWeights(weights):
		for key, value in weights.items():
			if key == 'w_corner_num':
				w_corner_num = value
			elif key == 'w_edge_num':
				w_edge_num = value
			elif key == 'w_flip_num':
				w_flip_num = value
			elif key == 'w_corner_adj_num':
				w_corner_adj_num = value


class Board:    

	# Gameboard: A board of 8 x 8 squares
	# The board has two extra rows and columns to make checking for bounds
	gameboard = [['-' for n in range(10)] for n in range(10)]

	def __init__(self, player_one, player_two):
		self.setUp(player_one, player_two)

	def setUp(self, player_one, player_two):
		""" Initial setup script"""
		for row, value in enumerate(self.gameboard):
			value[0] = "*"
			value[-1] = "*"
		self.gameboard[0] = ["*" for n in range(len(self.gameboard[0]))]
		self.gameboard[-1] = ["*" for n in range(len(self.gameboard[-1]))]
		self.white_curr_pos = []
		self.black_curr_pos = []
		self.validpositions = [(row,col) for row in range(1, 9) for col in range(1, 9)]
		self.edges = [(3, 1), (4, 1), (5, 1), (6, 1) , (8, 1),
			(1, 3),(1, 4), (1, 5), (1, 6), (3, 8), (4, 8), (5, 8), 
			(6, 8), (8, 3), (8, 4), (8, 5), (8, 6)]
		self.corners = [(1, 1),(8, 8), (8, 1), (1, 8)]
		self.corner_adj_positions = [(1, 2), (2, 1), (2, 2), (1, 7), (2, 7), (2, 8), (7, 1),
			(8, 2), (7, 2), (7, 8), (8, 7), (7, 7)]
		self.player_one = player_one
		self.player_two = player_two

	def h_setPosition(self, player, position):
		""" Helper function for to actually place the player on the board

			Args:
				player: A character indicating the colour of the player  
			position: A tuple indicating the particular cell to place the player in
		"""
		self.gameboard[position[0]][position[1]] = player
		if player == self.player_one:
			self.black_curr_pos.append((position[0],position[1]))
		elif player == self.player_two:
			self.white_curr_pos.append((position[0],position[1]))

	def removePiece(self, player, position):
		""" Removes a piece from the board 

			Args:
				player: A character indicating the colour of the player  
				position: A tuple indicating the particular cell to place the player in 
		"""
		if player == self.player_one:
			self.black_curr_pos.remove(position)
		elif player == self.player_two:
			self.white_curr_pos.remove(position)


	def getNoOfFlippedPieces(self, player):
		""" Gets number of flipped pieces

			Args:
				player: A character indicating the colour of the player
			Returns:
				value: An integer number
		"""
		if player == self.player_one:
			return len(self.black_curr_pos)
		elif player == self.player_two:
			return len(self.white_curr_pos)

	def getNoOfCornerPieces(self, player):
		""" Gets number of corner pieces

			Args:
				player: A character indicating the colour of the player
			Returns:
				value: An integer number 
		"""
		if player == self.player_one:
			return len([val for val in self.black_curr_pos if val in self.corners])
		elif player == self.player_two:
			return len([val for val in self.white_curr_pos if val in self.corners])

	def getNoOfEdgePieces(self,player):
		""" Gets number of edges pieces

			Args:
				player: A character indicating the colour of the player
			Returns:
				value: An integer number 
		"""

		if player == self.player_one:
			return len([val for val in self.black_curr_pos if val in self.edges])
		elif player == self.player_two:
			return len([val for val in self.white_curr_pos if val in self.edges])

	def getNoOfCornerAdjacentPieces(self, player):
		""" Gets number of corner adjacent pieces

			Args:
				player: A character indicating the colour of the player
			Returns:
				value: An integer number 
		"""

		if player == self.player_one:
			return len([val for val in self.black_curr_pos if val in self.corner_adj_positions])
		elif player == self.player_two:
			return len([val for val in self.white_curr_pos if val in self.corner_adj_positions])

	def allPositions(self, player):
		""" Returns a list of all places for a particular player 

			Args:
				player: character representing player
			Return:
				list: a list of tuples representing player positions

		"""
		#results = []
		if player == self.player_one:
			return self.black_curr_pos
		elif player == self.player_two:
			return self.white_curr_pos

	def get_no_of_spaces(self):
		return(64 - (len(self.black_curr_pos) + len(self.white_curr_pos)))

	def getMoves(self, position, player):
		"""
			This helper method returns a list of moves for a given position. The algorithm goes thus:

			While the number of columns or rows have not been exceeded:
				if position has execceded the bounds of the board
					break
				if there is a space adjacent to the position on the path of the search
					break
				if there is a space on the path of search and it is not preceeded by the same colour as the 
				given position
					add that to the moves list 

			Args:
				position: a tuple indicating the row and column to start the search
				player: character representing player

			Returns:
				moves: a list of legal positions or moves
		"""

		moves = []
		row, col = position


		# row-i, col + i
		for i in range(1, 9):
			if col + i > 8 and row - i < 0:
				break
			if i == 1 and (self.gameboard[row-i][col+i] == '-' or self.gameboard[row-i][col+i] == "*"):
				break
			if self.gameboard[row-i][col+i] == '*':
				break
			if self.gameboard[row-i][col+i] == '-' and (self.gameboard[(row-i)+1][col+(i-1)] != player and self.gameboard[(row-i)+1][col+(i-1)] != '-'):
				moves.append((row-i, col+i))
				#print(player, " You have appended me ", (row-i, col+i))
				break

		# row, col + i
		for i in range(1, 9):
			if col + i > 8:
				break
			if i == 1 and (self.gameboard[row][col+i] == '-' or self.gameboard[row][col+i] == "*"):
				break
			if self.gameboard[row][col+i] == '*':
				break 
			if self.gameboard[row][col+i] == '-' and (self.gameboard[row][col+(i-1)] != player and self.gameboard[row][col+(i-1)] != '-'): 
				moves.append((row, col+i))
				#print(player, " You have appended me ", (row, col+i))
				break

		# row-i, col - i
		for i in range(1, 9):
			if col - i < 0 or row - i < 0:
				break
			if i == 1 and (self.gameboard[row-i][col-i] == '-' or self.gameboard[row-i][col-i] == "*"):
				break 
			if self.gameboard[row-i][col-i] == '*':
				break
			if self.gameboard[row-i][col-i] == '-' and (self.gameboard[(row-i)+1][(col-i)+1] != player and self.gameboard[(row-i)+1][(col-i)+1] != '-') : 
				moves.append((row-i, col-i))
				#print(player, " You have appended me ", (row-i, col-i))
				break

		# row+i, col + i
		for i in range(1, 9):
			if col + i > 8 or  row + i > 8:
				break
			if i == 1 and (self.gameboard[row+i][col+i] == '-' or self.gameboard[row+i][col+i] == "*"):
				break 
			if self.gameboard[row+i][col+i] == '*':
				break
			if self.gameboard[row+i][col+i] == '-' and (self.gameboard[row+(i-1)][col+(i-1)] != player and self.gameboard[row+(i-1)][col+(i-1)] != '-'):
				moves.append((row+i, col+i))
				#print(player, " You have appended me ", (row+i, col+i))
				break

		# row-i, col
		for i in range(1, 9):
			if row - i < 0:
				break
			if i == 1 and (self.gameboard[row-i][col] == '-' or self.gameboard[row-i][col] == "*"):
				break 
			if self.gameboard[row-i][col] == '*':
				break
			if self.gameboard[row-i][col] == '-' and (self.gameboard[(row-i)+1][col] != player and self.gameboard[(row-i)+1][col] != '-'):
				moves.append((row-i, col))
				#print(player, " You have appended me ", (row-i, col))
				break

		# row, col - i
		for i in range(1, 9):
			if col - i < 0:
				break
			if i == 1 and (self.gameboard[row][col-i] == '-' or self.gameboard[row][col-i] == "*"):
				break 
			if self.gameboard[row][col-i] == '*':
				break
			if self.gameboard[row][col-i] == '-' and (self.gameboard[row][(col-i)+1] != player and self.gameboard[row][(col-i)+1] != '='):
				moves.append((row, col-i))
				#print(player, " You have appended me ", (row, col-i))
				break

		# row + i, col  
		for i in range(1, 9):
			if row + i > 8:
				break
			if i == 1 and (self.gameboard[row+i][col] == '-' or self.gameboard[row+i][col] == "*"):
				break 
			if self.gameboard[row+i][col] == '*':
				break
			if self.gameboard[row+i][col] == '-' and (self.gameboard[row+(i-1)][col] != player and self.gameboard[row+(i-1)][col] != '-'):
				moves.append((row+i, col))
				#print(player, " You have appended me ", (row+i, col))
				break

		# row + i, col - i  
		for i in range(1, 9):
			if col - i < 0 or row + i > 8:
				break
			if i == 1 and (self.gameboard[row+i][col-i] == '-' or self.gameboard[row+i][col-i] == "*"):
				break 
			if self.gameboard[row+i][col-i] == '*':
				break
			if self.gameboard[row+i][col-i] == '-' and (self.gameboard[row+(i-1)][(col-i)+1] != player and self.gameboard[row+(i-1)][(col - i)+1] != '-'): 
				moves.append((row+i, col-i))
				#print(player, " You have appended me ", (row+i, col-i))
				break

		return moves


	def getFlips(self, player, opp_player, position_to_move):

		""" Return the opposing player positions to flip

			Args:
				player: character representing player
				opp_player: character representing the opposing player
				position_to_move: A tuple indicating the particular cell to flip
			Return:
				flips: A list of opp_player positions to flip

		"""

		flips = []
		row, col = position_to_move[0], position_to_move[1]
		flag = False    # Flag indicates that we can stop
		count = 0

		# row - i, col - i
		for i in range(1, 9):
			if row - i < 0 or col - i < 0:
				break
			if i == 1 and (self.gameboard[row-i][col-i]== player or self.gameboard[row-i][col-i] == '-'):
				break
			if self.gameboard[row-i][col-i] == player and self.gameboard[row-(i-1)][col-(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row-i, col-i))
			flag = False

		# row - i , col
		for i in range(1, 9):
			if row - i < 0:
				break
			if i == 1 and (self.gameboard[row-i][col]== player or self.gameboard[row-i][col] == '-'):
				break
			if self.gameboard[row-i][col] == player and self.gameboard[row-(i-1)][col] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row-i, col))
			flag = False

		# row - i , col + i
		for i in range(1, 9):
			if row - i < 0 or col + i > 8:
				break
			if i == 1 and (self.gameboard[row-i][col + i]== player or self.gameboard[row-i][col+i] == '-'):
				break
			if self.gameboard[row-i][col+i] == player and self.gameboard[row-(i-1)][col+(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row-i, col+i))
			flag = False

		# row , col + i
		for i in range(1, 9):
			if col + i > 8:
				break
			if i == 1 and (self.gameboard[row][col + i]== player or self.gameboard[row][col+i] == '-'):
				break
			if self.gameboard[row][col+i] == player and self.gameboard[row][col+(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row, col+i))
			flag = False

		# row + i , col + i
		for i in range(1, 9):
			if row + i > 8  or col + i > 8:
				break
			if i == 1 and (self.gameboard[row+i][col + i]== player or self.gameboard[row+i][col+i] == '-'):
				break
			if self.gameboard[row+i][col+i] == player and self.gameboard[row+(i-1)][col+(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row+i, col+i))
			flag = False

		# row+i , col
		for i in range(1, 9):
			if row + i > 8:
				break
			if i == 1 and (self.gameboard[row+i][col]== player or self.gameboard[row+i][col] == '-'):
				break
			if self.gameboard[row+i][col] == player and self.gameboard[row+(i-1)][col] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row+i, col))
			flag = False

		# row+i , col - i
		for i in range(1, 9):
			if row + i > 8 or col - i < 0:
				break
			if i == 1 and (self.gameboard[row+i][col - i]== player or self.gameboard[row+i][col-i] == '-'):
				break
			if self.gameboard[row+i][col-i] == player and self.gameboard[row+(i-1)][col-(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row+i, col-i))
			flag = False

		# row , col - i
		for i in range(1, 9):
			if col - i < 0:
				break
			if i == 1 and (self.gameboard[row][col - i]== player or self.gameboard[row][col-i] == '-'):
				break
			if self.gameboard[row][col-i] == player and self.gameboard[row][col-(i-1)] == opp_player:
				flag = True
				count = i
				break

		if flag:
			for i in range(1, count):
				flips.append((row, col-i))
			flag = False

		return flips


	def getLegalMoves(self, player):
		""" Get the legal moves for a player

			Args:
				player: A character representing a player
			Return:
				results_list: A list of legal positions that the player can be placed at. Else a query_list is returned
			            if there are no legal moves
		"""

		query_list = self.allPositions(player)
		print(player, "('s) currently occupied positions = ", query_list)
		if len(query_list) != 0:
			results_list = []
			for position in query_list:
				results_list.append(self.getMoves(position, player))
			results_list = [value[n] for idx, value in enumerate(results_list) for n in range(len(value))]
			#print("Nice job = ", results_list)
			results_list[:] = [results_list[i] for i in range(len(results_list)) if i == results_list.index(results_list[i])] 
			return results_list
		return query_list  

	def win_or_lose(self):
		""" Determines who wins the game"""

		if len(self.white_curr_pos) > len(self.black_curr_pos):
			return "{0} wins.He/she has {1} pieces - {2} pieces".format(self.player_two, len(self.white_curr_pos), len(self.black_curr_pos))
		elif len(self.white_curr_pos) < len(self.black_curr_pos):
			return "{0} wins.He/she has {1} pieces - {2} pieces".format(self.player_one, len(self.black_curr_pos), len(self.white_curr_pos))
		else:
			return "Draw. Neither {0} nor {1} wins!!".format(self.player_one, self.player_two)

	def __str__(self):
		string = "  "
		for i in range(1, 9):
			string += "".join([" ", str(i)])
		string += "\n"

		print_list = self.gameboard[1: -1]
		for i, value in enumerate(print_list, 1):
			print_l = [["|", value[j]] for j in range(1, len(value) - 1)]
			print_l[:] = [val[n] for val in print_l for n in range(len(val))]
			string += "".join([str(i), " ", "".join(str(e) for e in print_l), "|", "\n"])
		return string