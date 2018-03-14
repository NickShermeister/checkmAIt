from datatypes import *
from chess import Board, Move
from typing import List


class Game(object):
    def __init__(self):
        self.board = Board()
        self.board.reset()

        self.left_graveyard = "TODO: this"
        self.right_graveyard = "TODO: this"

    def implementMove(self, move: Move) -> List[PieceMove]:
        # TODO: This
        return [PieceMove(PieceCoord(5, 0), PieceCoord(5, 3))]
