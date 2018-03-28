import chess
import chess.uci
import random
from collections import defaultdict


class Graveyard(object):
    def __init__(self):
        self.empty = []  # Available spaces, tuples of (color, coords) with first-used ones at the end
        self.stored = defaultdict(list)  # Map from tuples (bool isWhite, string type) to coords,
        # with the last added at the end.
        self._initspaces()

    def _initspaces(self):

        # White spaces
        for i in [-3, -2, 9, 10]:
            for j in range(0, 8):
                self.empty.append((i < 0, (j, i)))

        self.empty.sort(key=lambda x: self._earliness(x[1]))

    @staticmethod
    def _earliness(coord):
        """
        How early do we want to fill this coordinate? Outer columns first, inner rows first.
        :param coord:
        :return:
        """
        x, y = coord
        return 2.1 * abs(y) - abs(x)

    def storePiece(self, color, kind):
        """

        :param (bool) color: Is this piece white?
        :param (str) kind: What is the kind of this piece?
        :return (tuple) coord: The coordinate to which the piece should be sent.
        """

        kind = kind.upper()
        try:
            (color, location) = [(c, l) for c, l in self.empty if c == color][-1]
        except:
            print("You broke it.")
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
        for k, v in self.stored:
            if len(v) == 0:
                continue
            print('Color: {}, Type: {}'.format('White' if k[0] else 'Black', k[1]))
            for loc in v:
                print('\t{}'.format(loc))
