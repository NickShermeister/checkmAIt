"""
The ai behind our Wiznerds Chess.
"""
import chess
import chess.uci
from chess import Board, Move
import random
from motionPlanner import *
from collections import defaultdict

class aiController:

    def __init__(self):
        self.engine = chess.uci.popen_engine('libs/stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        

    def getMove(self, boardState, color="w"):
        """

        :param Board boardState: The state of the board
        :param str color: Whose move it is
        :return Move: What the AI wants to do
        """
        return Move.from_uci('a1a1')
