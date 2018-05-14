import chess
import chess.uci
import random
from collections import defaultdict
from typing import List, Tuple, Dict

from datatypes import PieceCoord


class Graveyard(object):
    def __init__(self):
        self.empty = []  # type: List[Tuple[bool, PieceCoord]]
        self.stored = defaultdict(list)  # type: Dict[Tuple[bool, str], List[PieceCoord]]
        # with the last added at the end.
        self._initspaces()

    def _initspaces(self):

        # White spaces
        for x in [-3, -2, 9, 10]:
            for y in range(0, 8):
                self.empty.append((x < 0, PieceCoord(x, y)))

        self.empty.sort(key=lambda mt: self._earliness(mt[1]))

    @staticmethod
    def _earliness(coord: PieceCoord):
        """
        How early do we want to fill this coordinate? Outer columns first, inner rows first.
        """
        return 2.1 * abs(coord.y) - abs(coord.x)

    def reset(self):
        self.stored = defaultdict(list)
        self._initspaces()
        
    def storePiece(self, color: bool, kind: str) -> PieceCoord:
        """
        :param color: Is this piece white?
        :param kind: What is the kind of this piece?
        :return coord: The coordinate to which the piece should be sent.
        """

        kind = kind.upper()
        (color, location) = [(c, l) for c, l in self.empty if c == color][-1]
        self.empty.remove((color, location))

        self.stored[(color, kind)].append(location)

        return location

    def retrievePiece(self, color, kind):
        """

        :param color: True for white, False for black
        :param kind:
        :return:  The coordinates from which a piece can be retrieved, or None.
        """
        kind = kind.upper()

        if len(self.stored[(color, kind)]) == 0:
            return None

        return self.stored[(color, kind)].pop()

    def printHi(self):
        print(self.stored)
        for k, v in self.stored.items():
            if len(v) == 0:
                continue
            print("k is {}, v is {}".format(k, v))
            print('Color: {}, Type: {}'.format('White' if k[0] else 'Black', k[1]))
            for loc in v:
                print('\t{}'.format(loc))
