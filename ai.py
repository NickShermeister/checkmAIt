"""
The ai behind our Wiznerds Chess.
"""
import chess
import chess.uci
from chess import Board, Move


class aiController:

    def __init__(self):
        self.engine = chess.uci.popen_engine('libs/stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        self.time = 300      #Time that we allow the engine to think.

    def changeTime(self, newTime):
        #change the amount of time the engine takes between turns
        self.time = newTime

    def getMove(self, boardState: Board, selectedMove = 0)->Move:
        """
        :param Board boardState: The state of the board
        :return Move: What the AI wants to do in the format (@#@#) [we need to search that location for the piece in order to have a valid command]
        """
        self.engine.position(boardState)    #Pass in the board's current state to the game engine.
        test = self.engine.go(movetime=self.time-selectedMove) #Movetime in milliseconds to generate best move.
        print(test)
        full_move_string = str(test[selectedMove])

        #Old code left in to show what we did
        # part1 = self.findLocPiece(full_move[0:2]) #get the piece from the dictionary
        # move_for_board = part1.upper() +full_move_string
        # print("Being passed into movePiece: %s " % move_for_board)
        # self.movePiece(move_for_board)

        return Move.from_uci(full_move_string)
