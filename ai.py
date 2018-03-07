"""
The ai behind our Wiznerds Chess.
"""
import chess
import chess.uci
import random
from motionPlanner import *
from collections import defaultdict

class aiController:

    def __init__(self):
        self.engine = chess.uci.popen_engine('libs/stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        
