from datatypes import *
from chess import Board, Move
from typing import List


class Game(object):
    def __init__(self):
        self.board = Board()
        self.board.reset()

        self.left_graveyard = "TODO: this"
        self.right_graveyard = "TODO: this"
        self.mapper = {'a':3, 'b':4, 'c':5, 'd':6,
        				'e':7, 'f':8, 'g':9, 'h':10
        }

    def testImplementMove(self, move):
    	""" Test version which takes a string instead of a move """
    	return [PieceMove(PieceCoord(self.mapper[move[0]], int(move[1])-1), PieceCoord(self.mapper[move[2]], int(move[3])-1))]

    def implementMove(self, move: Move) -> List[PieceMove]:
        return [PieceMove(PieceCoord(5, 0), PieceCoord(5, 3))]
