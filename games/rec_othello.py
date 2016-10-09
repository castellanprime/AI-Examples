#!/usr/bin/env python

"""An AI for the Othello game

File: rec_othello.py
Date: Sept 17, 2016
Author: Okusanya David

This is a barebones Othello two player game.

"""

import re, sys, os

class Othello:

    # Representation of the players on the board
    __PLAYER_BLACK = 'b'
    __PLAYER_WHITE = 'w'

    # Status codes
    ERROR = "invalid move"
    __NO_MOVE = "no moves available"
    __SUCCESS = "valid move"
    __GAME_END = "Game end"


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
                if self.gameboard[row-i][col+i] == '-' and self.gameboard[row-i+1][col+i-1] != player:
                    moves.append((row-i, col+i))
                    break

            # row, col + i
            for i in range(1, 9):
                if col + i > 8:
                    break
                if i == 1 and (self.gameboard[row][col+i] == '-' or self.gameboard[row][col+i] == "*"):
                    break 
                if self.gameboard[row][col+i] == '-' and self.gameboard[row][col+i-1] != player: 
                    moves.append((row, col+i))
                    break

            # row-i, col - i
            for i in range(1, 9):
                if col - i < 0 or row - i < 0:
                    break
                if i == 1 and (self.gameboard[row-i][col-i] == '-' or self.gameboard[row-i][col-i] == "*"):
                    break 
                if self.gameboard[row-i][col-i] == '-' and self.gameboard[row-i+1][col-i+1] != player: 
                    moves.append((row-i, col-i))
                    break

            # row+i, col + i
            for i in range(1, 9):
                if col + i > 8 or  row + i > 8:
                    break
                if i == 1 and (self.gameboard[row+i][col+i] == '-' or self.gameboard[row+i][col+i] == "*"):
                    break 
                if self.gameboard[row+i][col+i] == '-' and self.gameboard[row+i-1][col+i-1] != player:
                    moves.append((row+i, col+i))
                    break

            # row-i, col
            for i in range(1, 9):
                if row - i < 0:
                    break
                if i == 1 and (self.gameboard[row-i][col] == '-' or self.gameboard[row-i][col] == "*"):
                    break 
                if self.gameboard[row-i][col] == '-' and self.gameboard[row-i+1][col] != player:
                    moves.append((row-i, col))
                    break

            # row, col - i
            for i in range(1, 9):
                if col - i < 0:
                    break
                if i == 1 and (self.gameboard[row][col-i] == '-' or self.gameboard[row][col-i] == "*"):
                    break 
                if self.gameboard[row][col-i] == '-' and self.gameboard[row][col-i+1] != player:
                    moves.append((row, col-i))
                    break

            # row + i, col  
            for i in range(1, 9):
                if row + i > 8:
                    break
                if i == 1 and (self.gameboard[row+i][col] == '-' or self.gameboard[row+i][col] == "*"):
                    break 
                if self.gameboard[row+i][col] == '-' and self.gameboard[row+i-1][col] != player:
                    moves.append((row+i, col))
                    break

            # row + i, col - i  
            for i in range(1, 9):
                if col - i < 0 or row + i > 8:
                    break
                if i == 1 and (self.gameboard[row+i][col-i] == '-' or self.gameboard[row+i][col-i] == "*"):
                    break 
                if self.gameboard[row+i][col-i] == '-' and self.gameboard[row+i-1][col-i+1] != player: 
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
        self.__board = self.Board(self.__PLAYER_BLACK, self.__PLAYER_WHITE)
        self.__board.h_setPosition(self.__PLAYER_WHITE, (4, 4))
        self.__board.h_setPosition(self.__PLAYER_WHITE, (5, 5))
        self.__board.h_setPosition(self.__PLAYER_BLACK, (4, 5))
        self.__board.h_setPosition(self.__PLAYER_BLACK, (5, 4))

    # Making the class variables immutable
    @property
    def PLAYER_BLACK(self):
        return type(self).__PLAYER_BLACK    

    @property
    def PLAYER_WHITE(self):
        return type(self).__PLAYER_WHITE    


    def __validate_player(self, player):
        """ Checks to see if supplier player is correct
        
        Args:
            player: A character representing a player
        Raises:
            ValueError
        """
        if player not in (self.__PLAYER_WHITE, self.__PLAYER_BLACK):
            raise ValueError("Player can only be PLAYER_BLACK(='b') or PLAYER_WHITE(='w')")


    def __validate_position(self, position):
        """ Checks to see if supplied position is correct
        
        Args:
            position: A tuple (row, column) of the player's position
        Raises:
            ValueError
        """
        if position not in self.__board.validpositions:
            raise ValueError("Position not valid")

    def getLegalMoves(self, player):
        """ Get the legal moves for a player
        
        Args:
            player: A character representing a player
        Return:
            results_list: A list of legal positions that the player can be placed at. Else a query_list is returned
                            if there are no legal moves
        """

        query_list = self.__board.allPositions(player)
        print(player, "('s) currently occupied positions = ", query_list)
        if len(query_list) != 0:
            results_list = []
            for position in query_list:
                results_list.append(self.__board.getMoves(position, player))
            results_list = [value[n] for idx, value in enumerate(results_list) for n in range(len(value))]
            #print(results_list)
            results_list[:] = [results_list[i] for i in range(len(results_list)) if i == results_list.index(results_list[i])] 
            return results_list
        return query_list   

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

    def win_or_lose(self):
        """ Determines who wins the game"""

        if len(self.__board.white_curr_pos) > len(self.__board.black_curr_pos):
            return "{0} wins.He/she has {1} pieces - {2} pieces".format(__PLAYER_WHITE, len(self.__board.white_curr_pos), len(self.__board.black_curr_pos))
        elif len(white_curr_pos) < len(black_curr_pos):
            return "{0} wins.He/she has {1} pieces - {2} pieces".format(__PLAYER_BLACK, len(self.__board.black_curr_pos), len(self.__board.white_curr_pos))
        else:
            return "Draw. Neither {0} nor {1} wins!!".format(__PLAYER_BLACK, __PLAYER_WHITE)

    def flip_opp_player_positions(self, player, position_to_move):
        """ Flips all the pieces for a particular players' move

        Args:
            position: a tuple indicating the row and column to start the search
            player: character representing player
        """

        opp_player = self.get_opp_player(player)
        #print(opp_player[0])
        l = self.__board.getFlips(player, opp_player[0], position_to_move)
        print(opp_player[0], "'s positions to flip = " , l)
        self.__board.h_setPosition(player, position_to_move)
        for value in l:
            self.__board.h_setPosition(player, value)
            self.__board.removePiece(opp_player[0], value)   

    def place(self, player, position_to_move):
        """ Places a player's piece on the board

        Args:
            player: A character representing a player
            position_to_move: A tuple (row, column) the player wants to move to
        Return:
            status message: Error message if the piece can not be played. If the piece can be played, the 
                            method returns a __SUCCESS message.

        """
        legal_moves = self.getLegalMoves(player)
        if len(legal_moves) != 0:
            print(player, "'s legal_moves = ", legal_moves)
            if position_to_move not in legal_moves:
                return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.ERROR)
            self.flip_opp_player_positions(player, position_to_move)
            return "\nPlayer {0}'s move:{1} Return_code:{2}\n".format(player, position_to_move, self.__SUCCESS)
        return "\n Player {0} has {1} \n".format(player, self.__NO_MOVE)

    def toString(self):
        """ Print the representation of the board to console"""
        return self.__board.__str__()

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

    def get_input(self, input_player=None):
        """ User input from the command line 
        
        Args:
            input_player: Default value is None. A character representing the player
        Return:
            input_player: A character representing the player
            input_position: A tuple representing the row and col to place player's piece
        Raise:
            ValueError
        """
        return_one = True
        try:
            if input_player == None:
                input_player = input("Enter your player(ex: b ) : ")
                return_one = False
            self.__validate_player(input_player)
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
        if return_one == False:
            return input_player, input_position
        else: 
            return input_position
        
    def __check_if_player_has_legal_moves(self, rec_str, has_black_played, has_white_played):
        """ Check if a player during a play has any legal moves
        
        Args:
            rec_str: Status message string of the place method
            has_black_played: A boolean value denoted if player with the black piece has placed a piece on the board
            has_white_played: A boolean value denoted if player with the white piece has placed a piece on the board
        Return:
            str: If neither player has a legal move, return a error code.
        """
        
        if len(re.findall(r'no moves available', rec_str)) > 0:
            print("\nEntering legal moves play")
            opp_player = self.get_opp_player(player)
            print("{0} has no legal moves. {1} plays").format(player, opp_player[0])
            opp_player_position = self.get_input(opp_player[0])
            sec_rec_str = self.place(opp_player[0], opp_position)
            print(sec_rec_str)
            if rec_str == sec_rec_str:
                print(self.win_or_lose())
                return self.__GAME_END
            if opp_player == self.__PLAYER_BLACK and has_white_played:
                has_black_played = True
                has_white_played = False
            elif opp_player == self.__PLAYER_WHITE and has_black_played:
                has_white_played = True
                has_black_played = False
        return 'Nothing'

    def play(self):
        """ This does the actual playing of the game"""

        self.prompt()
        black_count = 0
        rec_str, player, position = " ", ' ', ()
        has_black_played, has_white_played = False, False

        while True:
             print(self.__board.__str__())

             input_tuple = self.get_input()
             player = input_tuple[0]
             position = input_tuple[1]

             if has_black_played == False and has_white_played == False:
                while player != self.__PLAYER_BLACK:
                    print("\nBlack must go first")
                    input_tuple = self.get_input()
                    player = input_tuple[0]
                    position = input_tuple[1]
                has_black_played = True
             elif has_black_played == True and has_white_played == False:
                while player != self.__PLAYER_WHITE:
                    print("\nWhite must go now")
                    input_tuple = self.get_input()
                    player = input_tuple[0]
                    position = input_tuple[1]
                has_white_played = True
                has_black_played = False
             elif has_black_played == False and has_white_played == True:
                while player != self.__PLAYER_BLACK:
                    print("\nBlack must go now")
                    input_tuple = self.get_input()
                    player = input_tuple[0]
                    position = input_tuple[1]
                has_black_played = True
                has_white_played = False

             rec_str = self.place(player, position)

            # invalid moves
             while len(re.findall(r'invalid move', rec_str)) > 0:
                position = self.get_input(player)
                rec_str = self.place(player, position)

            # if one of the players has no valid moves left
             status_message = self.__check_if_player_has_legal_moves(rec_str, has_black_played, has_white_played)
             if status_message == self.__GAME_END:
                print(self.__GAME_END)
                return

             if self.__board.get_no_of_spaces() == 0:
                print(self.win_or_lose())
                print(self.__GAME_END)
                return
    
def main_loop():
    o = Othello()
    o.play()

if __name__ == '__main__':
    main_loop()
