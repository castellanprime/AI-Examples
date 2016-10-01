#!/usr/bin/env python

"""An AI for the Othello game

File: othello.py
Date: Sept 17, 2016
Author: Okusanya David

This is a project in AI using the Othello game. It uses a minimax algorithm with alpha-beta
pruning.

"""

import re

class Othello:

	# Representation of the players on the board
	_PLAYER_BLACK = 'b'
	_PLAYER_WHITE = 'w'

	# Status codes
	ERROR = "invalid move"
	NO_MOVE = "no moves available"
	SUCCESS = "valid move"


	class Board:	

		# Gameboard: A board of 8 x 8 squares
		# The board has two extra rows and columns to make checking for bounds
		gameboard = [[0 for n in range(10)] for n in range(10)]

		def __init__(self):
			self.setUp()
		 
		def setUp(self):
			""" Initial setup script"""
			for row, value in enumerate(self.gameboard):
				value[0] = "*"
				value[-1] = "*"
			self.gameboard[0] = ["*" for n in range(len(self.gameboard[0]))]
			self.gameboard[-1] = ["*" for n in range(len(self.gameboard[-1]))]
			self.white_curr_pos = []
			self.black_curr_pos = []
			self.validpositions = [(row, col) for row in range(1, 9) for col in range(1, 9)]

		def h_setPosition(self, player, position):
			""" Helper function for to actually place the player on the board

			Args:
				player: A character indicating the colour of the player  
				position: A tuple indicating the particular cell to place the player in
			"""
			self.gameboard[position[0]][position[1]] = player
			if player == _PLAYER_BLACK:
				black_curr_pos.append(position[0], position[1])
			elif player == _PLAYER_WHITE:
				white_curr_pos.append(position[0], position[1])


		def allPositions(self, player):
			""" Returns a list of all places for a particular player 
			
			Args:
				player: character representing player
			Return:
				list: a list of tuples representing player positions

			"""
			#results = []
			if player == _PLAYER_WHITE:
				return self.white_curr_pos
			elif player == _PLAYER_BLACK:
				return self.black_curr_pos

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
				if i == 1 and (self._gameboard[row-i][col+i] == 0 or self._gameboard[row-i][col+i] == "*"):
					break 
				if self._gameboard[row-i][col+i] == 0 and self._gameboard[row-i+1][col+i-1] != player:
					moves.append((row-i, col+i))
					break

			# row, col + i
			for i in range(1, 9):
				if col + i > 8:
					break
				if i == 1 and (self._gameboard[row][col+i] == 0 or self._gameboard[row][col+i] == "*"):
					break 
				if self._gameboard[row][col+i] == 0 and self._gameboard[row][col+i-1] != player: 
					moves.append((row, col+i))
					break

			# row-i, col - i
			for i in range(1, 9):
				if col - i < 0 or row - i < 0:
					break
				if i == 1 and (self._gameboard[row-i][col-i] == 0 or self._gameboard[row-i][col-i] == "*"):
					break 
				if self._gameboard[row-i][col-i] == 0 and self._gameboard[row-i+1][col-i+1] != player: 
					moves.append((row-i, col-i))
					break

			# row+i, col + i
			for i in range(1, 9):
				if col + i > 8 or  row + i > 8:
					break
				if i == 1 and (self._gameboard[row+i][col+i] == 0 or self._gameboard[row+i][col+i] == "*"):
					break 
				if self._gameboard[row+i][col+i] == 0 and self._gameboard[row+i-1][col+i-1] != player:
					moves.append((row+i, col+i))
					break

			# row-i, col
			for i in range(1, 9):
				if row - i < 0:
					break
				if i == 1 and (self._gameboard[row-i][col] == 0 or self._gameboard[row-i][col] == "*"):
					break 
				if self._gameboard[row-i][col] == 0 and self._gameboard[row-i+1][col] != player:
					moves.append((row-i, col))
					break

			# row, col - i
			for i in range(1, 9):
				if col - i < 0:
					break
				if i == 1 and (self._gameboard[row][col-i] == 0 or self._gameboard[row][col-i] == "*"):
					break 
				if self._gameboard[row][col-i] == 0 and self._gameboard[row][col-i+1] != player:
					moves.append((row, col-i))
					break

			# row + i, col	
			for i in range(1, 9):
				if row + i > 8:
					break
				if i == 1 and (self._gameboard[row+i][col] == 0 or self._gameboard[row+i][col] == "*"):
					break 
				if self._gameboard[row+i][col] == 0 and self._gameboard[row+i-1][col] != player:
					moves.append((row+i, col))
					break

			# row + i, col - i	
			for i in range(1, 9):
				if col - i < 0 or row + i > 8:
					break
				if i == 1 and (self._gameboard[row+i][col-i] == 0 or self._gameboard[row+i][col-i] == "*"):
					break 
				if self._gameboard[row+i][col-i] == 0 and self._gameboard[row+i-1][col-i+1] != player: 
					moves.append((row+i, col-i))
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
			flag = False	# Flag indicates that we can stop
			count = 0

			# row - i, col - i
			for i in range(1, 9):
				if row - i < 0 or col - i < 0:
					break
				if i == 1 and (self._gameboard[row-i][col-i]== player or self._gameboard[row-i][col-i] == 0):
					break
				if self._gameboard[row-i][col-i] == player and self._gameboard[row-(i-1)][col-(i-1)] == opp_player:
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
				if i == 1 and (self._gameboard[row-i][col]== player or self._gameboard[row-i][col] == 0):
					break
				if self._gameboard[row-i][col] == player and self._gameboard[row-(i-1)][col] == opp_player:
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
				if i == 1 and (self._gameboard[row-i][col + i]== player or self._gameboard[row-i][col+i] == 0):
					break
				if self._gameboard[row-i][col+i] == player and self._gameboard[row-(i-1)][col+(i-1)] == opp_player:
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
				if i == 1 and (self._gameboard[row][col + i]== player or self._gameboard[row][col+i] == 0):
					break
				if self._gameboard[row][col+i] == player and self._gameboard[row][col+(i-1)] == opp_player:
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
				if i == 1 and (self._gameboard[row+i][col + i]== player or self._gameboard[row+i][col+i] == 0):
					break
				if self._gameboard[row+i][col+i] == player and self._gameboard[row+(i-1)][col+(i-1)] == opp_player:
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
				if i == 1 and (self._gameboard[row+i][col]== player or self._gameboard[row+i][col] == 0):
					break
				if self._gameboard[row+i][col] == player and self._gameboard[row+(i-1)][col] == opp_player:
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
				if i == 1 and (self._gameboard[row+i][col - i]== player or self._gameboard[row+i][col-i] == 0):
					break
				if self._gameboard[row+i][col-i] == player and self._gameboard[row+(i-1)][col-(i-1)] == opp_player:
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
				if i == 1 and (self._gameboard[row][col - i]== player or self._gameboard[row][col-i] == 0):
					break
				if self._gameboard[row][col-i] == player and self._gameboard[row][col-(i-1)] == opp_player:
					flag = True
					count = i
					break

			if flag:
				for i in range(1, count):
					flips.append((row, col-i))
				flag = False

			return flips


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

	

	def __init__(self):
		self._board = Board()
		self._board.h_setPosition(self._PLAYER_WHITE, (4, 4))
		self._board.h_setPosition(self._PLAYER_WHITE, (5, 5))
		self._board.h_setPosition(self._PLAYER_BLACK, (4, 5))
		self._board.h_setPosition(self._PLAYER_BLACK, (5, 4))

	# Making the class variables immutable
	@property
	def PLAYER_BLACK(self):
		return type(self)._PLAYER_BLACK	

	@property
	def PLAYER_WHITE(self):
		return type(self)._PLAYER_WHITE	


	def _validate_player(self, player):
		""" Checks to see if supplier player is correct
		
		Args:
			player: A character representing a player
		Raises:
			ValueError
		"""
		if player not in (self._PLAYER_WHITE, self._PLAYER_BLACK):
			raise ValueError("Player can only be PLAYER_BLACK(=1) or PLAYER_WHITE(=2)")


	def _validate_position(self, position):
		""" Checks to see if supplied position is correct
		
		Args:
			position: A tuple (row, column) of the player's position
		Raises:
			ValueError
		"""
		if position not in self.board.validpositions:
			raise ValueError("Position not valid")

	def getLegalMoves(self, player):
		""" Get the legal moves for a player
		
		Args:
			player: A character representing a player
		Return:
			results_list: A list of legal positions that the player can be placed at. Else a query_list is returned
							if there are no legal moves
		"""

		query_list = self._board.allPositions(player)
		if query_list:
			results_list = []
			for position in query_list:
				results_list.append(self._board.getMoves(position, player))
			results_list = [value[n] for idx, value in enumerate(results_list) for n in range(len(value))]
			results_list[:] = [results_list[i] for i in range(len(results_list)) if i == results_list.index(results_list[i])] 
			return results_list
		return query_list	

	def get_opp_player(self, player):
		s = [self._PLAYER_BLACK, self._PLAYER_WHITE]
		opp_player = list(set(s).difference([player]))
		return opp_player

	def win_or_lose(self):_
		if len(self._board.white_curr_pos) > len(self._board.black_curr_pos):
			return "{0} wins.He/she has {1} pieces - {2} pieces".format(_PLAYER_WHITE, len(self._board.white_curr_pos), len(self._board.black_curr_pos))
		elif len(white_curr_pos) < len(black_curr_pos):
			return "{0} wins.He/she has {1} pieces - {2} pieces".format(_PLAYER_BLACK, len(self._board.black_curr_pos), len(self._board.white_curr_pos))
		else:
			return "Draw. Neither {0} nor {1} wins!!".format(_PLAYER_BLACK, _PLAYER_WHITE)

	def flip_opp_player_positions(self, player, position_to_move):
		""" Flips all the pieces for a particular players' move

		Args:
			position: a tuple indicating the row and column to start the search
			player: character representing player
		"""

		opp_player = self.get_opp_player(player)
		#print(opp_player[0])
		l = self._board.getFlips(player, opp_player[0], position_to_move)
		print(l)
		self._board.h_setPosition(player, position_to_move)
		for value in l:
			self._board.h_setPosition(player, value)	

	def place(self, player, position_to_move):
		""" Places a player's piece on the board

		Args:
			player: A character representing a player
			position_to_move: A tuple (row, column) the player wants to move to
		Return:
			status message: Error message if the piece can not be played. If the piece can be played, the 
							method returns a success message.

		"""
		#self._validate_player(player)
		#self._validate_position(position_to_move)
		legal_moves = self.getLegalMoves(player)
		if len(legal_moves) != 0:
			print(legal_moves)
			if position_to_move not in legal_moves:
			 	return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.ERROR)
			self.flip_opp_player_positions(player, position_to_move)
			return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.SUCCESS)
		return "\n Player {0} has {1} \n".format(player, self.NO_MOVE)

	def toString(self):
		""" Print the representation of the board to console"""
		return self._board.__str__()

	def prompt(self):
		""" Header about the game rules in a prompt message"""

		print("Welcome to Othello!! Have fun!!")
		print("=" * 10)
		print("\n\n")
		print("Rules for game \n\t", 
			  " 1. Black is represented by 'b' and White is represented by 'w' ", 
			  " 1. Black plays first \n\t", 
			  " 2. If a player has no legal moves, the other player plays\n\t ", 
			  " 3. If there are no more legal moves for the two players, game ends.\n\t", 
			  " 4. The player with the maximum number of pieces wins or else there is a draw \n")


	def play(self):
		self.prompt()
		black_count = 0	# Useful for prompting 
		sec_rec_str, rec_str, player, position = " ", " ", ' ', ()
		while True:

			try:
				player, position = input("Enter your player and position (ex: 'b' (4, 3) ): ")
				self._validate_player(player)
				self._validate_position(position)
			except ValueError as e:
				print(e)

			# If a person decides to play White first
			while black_count == 0 and player != self._PLAYER_BLACK:
				print(self.ERROR)
				player, position = input("Enter your player and position (ex: 'b' (4, 3) ): ")
	 
			rec_str = self.place(player, position)
			print(rec_str)

			if black_count == 0:
				black_count = 1

			if len(re.findAll(r'no moves available', rec_str)) > 0
				opp_player = self.get_opp_player(player)
				print("{0} has no legal moves. {1} plays").format(player, opp_player[0])
				sec_rec_str = self.place(opp_player)
				print(sec_rec_str)
				if rec_str == sec_rec_str:
					print(self.win_or_lose())
					return

			if self._board.get_no_of_spaces() < 10:
				print(self.win_or_lose())
				return

	
def main_loop():
	o = Othello()
	o.play()

if __name__ == '__main__':
	main_loop()
