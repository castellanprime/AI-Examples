#!/usr/bin/env python

"""
	This module contains the implementation of a board and 
	gamestate.

	File: rec_othello_ai.py
	Date: Oct 15, 2016
	Author: Okusanya David
"""
import sys
import re
import os
import random
import copy
import logging
from OthelloUtils import GameState, Board


logging.basicConfig(filename="game.log", filemode='a', level=logging.INFO)

class Othello:

	# Representation of the players on the board
	__PLAYER_BLACK = 'b'
	__PLAYER_WHITE = 'w'

	# Status codes
	ERROR = "invalid move"
	__NO_MOVE = "no moves available"
	__SUCCESS = "valid move"
	__GAME_END = "Game end"

	def __init__(self):
		self.board = Board(self.__PLAYER_BLACK, self.__PLAYER_WHITE)
		self.board.h_setPosition(self.__PLAYER_WHITE, (4, 4))
		self.board.h_setPosition(self.__PLAYER_WHITE, (5, 5))
		self.board.h_setPosition(self.__PLAYER_BLACK, (4, 5))
		self.board.h_setPosition(self.__PLAYER_BLACK, (5, 4))
		self.state = GameState(self.__PLAYER_BLACK, self.board)

	# Making the class variables immutable
	@property
	def PLAYER_BLACK(self):
		return type(self).__PLAYER_BLACK    

	@property
	def PLAYER_WHITE(self):
		return type(self).__PLAYER_WHITE   


	def __validate_position(self, position):
		""" Checks to see if supplied position is correct 
			
			Args:
				position: A tuple (row, column) of the player's position
			Raises:
				ValueError
		"""
		if position not in self.state.board.validpositions:
			raise ValueError("Position not valid")

	def place(self, position_to_move, player_opp=None):
		""" Places a player's piece on the board

		Args:
			player: A character representing a player
			position_to_move: A tuple (row, column) the player wants to move to
		Return:
			status message: Error message if the piece can not be played. If the piece can be played, the 
		        method returns a __SUCCESS message.

		"""

		player = self.state.turn
		opp_player = ''
		if player_opp == None:
			opp_player = self.get_opp_player(player)[0]
		else:
			opp_player = player_opp

		# If player has legal moves	
		if self.state.next_moves:
			print("Legal moves for ", player, " = ", self.state.next_moves)
			logging.info("Legal moves for %s = %s", player, self.state.next_moves)
			if position_to_move not in self.state.next_moves:
				return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.ERROR)
			self.flip_opp_player_positions(player, opp_player, position_to_move)
			self.state = GameState(opp_player, self.state.board)
		return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.__SUCCESS)

		# If player does not have legal moves
		if player_opp != None:
			self.state = Gamestate(opp_player, self.state.board)
			if self.state.next_moves:
				#print("Legal moves for ", opp_player, " = ", self.state.next_moves)
				logging.info("Legal moves for %s = %s", player, self.state.next_moves)
				if position_to_move not in self.state.next_moves:
					return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.ERROR)
				self.flip_opp_player_positions(player, opp_player, position_to_move)
				self.state = GameState(opp_player, self.state.board)
			return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.__SUCCESS)

		return "\n Player {0} has {1} \n".format(player, self.__NO_MOVE)

	def get_opp_player(self, player):
		""" Returns the opposite player in the music set

		Args:
			player: A character representing a player
		Return:
			opp_player: A list containing the opp_player

		"""
		s = [self.__PLAYER_BLACK, self.__PLAYER_WHITE]
		opp_player = list(set(s).difference([player]))
		return opp_player


	def flip_opp_player_positions(self, player, opp_player, position_to_move):
		""" Flips all the pieces for a particular players' move

		Args:
			position: a tuple indicating the row and column to start the search
			player: character representing player
		"""

		l = self.state.board.getFlips(player, opp_player, position_to_move)
		#print(opp_player, "'s positions to flip = " , l)
		logging.info("%s 's positions to flip = %s", opp_player, l)
		self.state.board.h_setPosition(player, position_to_move)
		for value in l:
			self.state.board.h_setPosition(player, value)
			self.state.board.removePiece(opp_player, value)  

	def toString(self):
		""" Print the representation of the board to console"""
		return self.state.board.__str__()

	def prompt(self):
		""" Header about the game rules in a prompt message"""

		print("Welcome to Othello!! Have fun!!")
		print("=" * 10)
		print("\n\n")
		print("Rules for game \n\n", 
		" 1. Black is represented by 'b' and White is represented by 'w' \n", 
		" 2. Black plays first \n", 
		" 3. If a player has no legal moves, the other player plays\n ", 
		" 4. If there are no more legal moves for the two players, game ends.\n", 
		" 5. The player with the maximum number of pieces wins or else there is a draw \n")

	def get_input(self):
		""" User input from the command line 

		Args:
			input_player: Default value is None. A character representing the player
		Return:
			input_player: A character representing the player
			input_position: A tuple representing the row and col to place player's piece
		Raise:
			ValueError
		"""
		input_position = ()
		try:
			str = "{0} plays now".format(self.state.turn)
			print(str)
			logging.info("%s", str)
			temp_input = input("Enter your position(row, col) (ex: 4 3): ")
			input_position = tuple(map(int, temp_input.split(' ')))
			self.__validate_position(input_position)
		except ValueError as e:
			print(e)
		except KeyboardInterrupt:
			print("\nInterrupted\n")
			try :
				sys.exit(0)
			except SystemExit:
				os._exit(0)
		logging.info("%s", input_position)
		return input_position
    
	def human_play(self):

		position = ()

		while True:
			print(self.state.board.__str__())
			logging.info("%s", self.state.board.__str__())

			# First input
			position = self.get_input()									

			# If first input is wrong
			while len(position) == 0:
				position = self.get_input()

			# First place							
			status_message = self.place(position)							

			# If move is not in self.state.moves
			while len(re.findall(r'invalid move', status_message)) > 0:	
				print(status_message)
				logging.info("%s", status_message)		
				position = self.get_input()
				status_message = self.place(position) 

			# If there are not legal moves
			if len(re.findall(r'no moves available', status_message)) > 0:
				print(status_message)
				logging.info("%s", status_message)		
				print("Entering legal moves")
				# Get the opposite player to play
				opp_player = self.get_opp_player(self.state.turn)				
				status_message = self.place(position, opp_player)
				# If oppposite player does not have legal moves
				if len(re.findall(r'no moves available', status_message)) > 0:
					print(self.state.board.win_or_lose())
					logging.info("%s", self.state.board.win_or_lose())
					print(self.__GAME_END)
					logging.info("%s", self.__GAME_END)
					return

			# If the game is finished
			if self.state.board.get_no_of_spaces() == 0:
				print(self.state.board.win_or_lose())
				logging.info("%s", self.state.board.win_or_lose())
				print(self.__GAME_END)
				logging.info("%s", self.__GAME_END)
				return

def main_loop():
	o = Othello()
	o.prompt()
	o.human_play()

if __name__ == '__main__':
	main_loop()
