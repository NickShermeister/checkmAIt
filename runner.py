"""
Chess Running script for Hack Holyoke 2017.
in order to import chess, run:
pip3 install python-chess
"""
import chess
import chess.uci
from motionPlanner import *
from collections import defaultdict
from speech_reognition.speech_test import main


class ChessGame:
    """docstring for ChessGame."""

    def __init__(self):

        self.board = chess.Board()
        self.running = True
        self.turn = True    #True means player makes first move; else AI makes first move.
        #first player is always white
        self.engine = chess.uci.popen_engine('stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        self.first = self.turn
        self.whiteLocations = {'': [], 'R': [], 'N': [], 'B': [], 'K': [], 'Q': []}
        self.blackLocations = {'': [], 'r': [], 'n': [], 'b': [], 'k': [], 'q': []}
        self.whiteLocations[''] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.whiteLocations['R'] = ['a1', 'h1']
        self.whiteLocations['N'] = ['b1', 'g1']
        self.whiteLocations['B'] = ['c1', 'f1']
        self.whiteLocations['K'] = ['e1']
        self.whiteLocations['Q'] = ['d1']

        # Black pieces
        self.blackLocations[''] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        self.blackLocations['r'] = ['a8', 'h8']
        self.blackLocations['n'] = ['b8', 'g8']
        self.blackLocations['b'] = ['c8', 'f8']
        self.blackLocations['k'] = ['e8']
        self.blackLocations['q'] = ['d8']
        self.graveyard = Graveyard()
        self.mp = MotionPlanner()

        # self.resetBoard()

        self.gameLoop()

    def movePiece(self, command):
        # TODO: HANDLE CASTLING AND IN PASSING
        try:
            hi = self.board.push_san(command)

        except:
            print("Invalid command.")
            print(self.board)
            self.turn = not self.turn
            return
        stripped_command = ''.join(l for l in hi.uci() if l in '12345678abcdefgh')
        loc1 = stripped_command[0:2]
        loc2 = stripped_command[2:]
        self.updateLocations(loc1, loc2)
        assert (len(hi.uci()) == 4)
        src, dest = self.uciToLocations(hi.uci())
        self.output_move(src, dest)

    def updateLocations(self, loc1, loc2):
        # print("Loc 1: %s" % loc1)
        # print("Loc 1: %s" % loc2)
        piece1 = self.findLocPiece(loc1)
        piece2 = self.findLocPiece(loc2)
        print(piece1)
        print(piece2)
        # print("Good1")
        # print("Piece1 : %s " % piece1)
        # print("Piece2 : %s " % piece2)
        if self.turn:
            # print(self.whiteLocations[piece1])
            self.whiteLocations[piece1].remove(loc1)
            self.whiteLocations[piece1].append(loc2)

        else:
            self.blackLocations[piece1].remove(loc1)
            self.blackLocations[piece1].append(loc2)

        if piece2:
            self.graveyardMove(loc2)

    def graveyardMove(self, loc):
        """
        Sends a piece to the graveyard, and removes it from the record of the board
        :param loc: two-character string representing location on board
        :return:
        """
        piece = self.findLocPiece(loc)
        is_white = piece.isupper()

        # Remove the piece from its current square
        (self.whiteLocations if is_white else self.blackLocations)[piece].remove(loc)

        # Add the piece to the graveyard
        dest = self.graveyard.storePiece(is_white, piece)

        print("Sending piece {} at {} to graveyard {}".format(piece, loc, dest))
        self.output_move(loc, dest)

    def reviveFromGraveyard(self, dest, piece):
        """
        Makes a move to revive the given piece from the graveyard, and marks its new position.
        :param dest: two-character code of space to fill
        :param piece: piece character (capital = white) to revive
        :return:
        """

        is_white = piece.isupper()
        source = self.graveyard.retrievePiece(is_white, piece)
        assert source is not None, "Tried to revive piece not in graveyard"

        if piece.lower() == 'p':
            piece = ''

        (self.whiteLocations if is_white else self.blackLocations)[piece].append(dest)

        print("The source is %s" % str(source))
        self.output_move(source, self.pairToLocation(dest))


    def printLocations(self):
        print("White locations")
        print(self.whiteLocations)
        print("Black locations")
        print(self.blackLocations)

    def findLocPiece(self, location):
        """
        Takes in a 2 letter/number string thatgives a square (e.g. a1, h8, etc.)
        returns P for white pawn, p for black pawn.
        """
        print(self.whiteLocations)
        print(location)
        for x in self.whiteLocations:
            if location in self.whiteLocations[x]:
                return x
        for x in self.blackLocations:
            if location in self.blackLocations[x]:
                return x
        return None

    def printBoard(self):
        print(self.board)

    def resetBoard(self):
        # TODO: ROUTE TO MOVE PIECES BACK
        toRevive = dict()

        # White pieces
        toRevive[''] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        toRevive['R'] = ['a1', 'h1']
        toRevive['N'] = ['b1', 'g1']
        toRevive['B'] = ['c1', 'f1']
        toRevive['K'] = ['e1']
        toRevive['Q'] = ['d1']

        # Black pieces
        toRevive[''] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        toRevive['r'] = ['a8', 'h8']
        toRevive['n'] = ['b8', 'g8']
        toRevive['b'] = ['c8', 'f8']
        toRevive['k'] = ['e8']
        toRevive['q'] = ['d8']

        for piece in toRevive:
            for locs in toRevive[piece]:
                self.reviveFromGraveyard(locs, piece)

        self.board.reset()
        self.printBoard()

    def output_move(self, source, dest):
        """

        :param source: Coordinates of the source (tuple in board coordinates)
        :param dest: Coordinates of the destination (tuple in board coordinates
        :return: The string output
        """

        string = '{} {} -> {} {} \n'.format(*source, *dest)

        print("OUTPUT: \n\t", string)
        self.mp.run(string)

        return string

    @staticmethod
    def pairToLocation(pair):
        print(pair)
        print(len(pair))
        assert(len(pair) == 2)

        # Converts a 2-character UCI coordinate to a tuple
        loc = (float(ord(pair[0]) - 96), float(pair[1]))
        assert (0. <= loc[0] < 8 and 0. <= loc[1] < 8)
        return loc

    def uciToLocations(self, command):
        """

        :param command: 4-character uci formatted string ex. "e5e7"
        :return:
        """

        assert (len(command) == 4)

        return self.pairToLocation(command[:2]), self.pairToLocation(command[2:])

    def aiMove(self):
        self.engine.position(self.board)
        test = self.engine.go(movetime=300)
        hi = str(test[0])
        print(hi)
        # self.movePiece(hi)
        hi1 = self.findLocPiece(hi[0:2])
        print(hi1)
        hi2 = hi1+hi
        self.movePiece(hi2)
        # self.board.push(Nf3)

        # self.movePiece(hi)
        self.turn = not self.turn

    def gameOver(self):
        # TODO: what happens when the game ends
        resultant = self.board.result()
        if resultant == "1-0":
            print("Congratulations! White wins!")
        elif resultant == "0-1":
            print("Congratulations! Black wins!")
        else:
            print("It's a draw!")
        self.resetBoard()
        again = input("Want to play again? (y/n): ")
        if again.lower() == "n":
            self.running = False

    def checkGameOver(self):
        if self.board.is_game_over():
            # TODO: get why it is over (stalemate, checkmate)
            return True
        else:
            return False

    def playerTurn(self):
        move = main()
        #move = input('Move: ')
        if move == "p":
            self.printBoard()
        elif move == "m":  # print legal moves
            print(self.board.legal_moves)
            for x in self.board.legal_moves:
                print(x)
        elif move == "r":  # fast reset of board
            self.resetBoard()
        elif move == "g":
            self.graveyard.printHi()
        elif move == "pl":
            self.printLocations()
        elif move == "cm":  # a very easy checkmate, for endgame testing
            self.movePiece("e4")
            self.turn = not self.turn
            self.movePiece("e5")
            self.turn = not self.turn
            self.movePiece("Qh5")
            self.turn = not self.turn
            self.movePiece("Nc6")
            self.turn = not self.turn
            self.movePiece("Bc4")
            self.turn = not self.turn
            self.movePiece("Nf6")
            self.turn = not self.turn
            self.movePiece("Qxf7")
        else:
            self.movePiece(move)
            self.turn = not self.turn

    def gameLoop(self):
        while (self.running):
            print("Player turn (T=white, F=black): %s" % self.turn)
            if (self.turn):  # player turn
                self.playerTurn()

            else:  # AI turn=
                self.aiMove()

            if self.checkGameOver():
                self.gameOver()
        print("Baiiiiiii")


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
                self.empty.append((i < 0, (i, j)))

        self.empty.sort(key=lambda x: self._earliness(x[1]))

    @staticmethod
    def _earliness(coord):
        """
        How early do we want to fill this coordinate? Outer columns first, inner rows first.
        :param coord:
        :return:
        """
        x, y = coord
        return 2.1 * abs(x) - abs(y)

    def storePiece(self, color, kind):
        """

        :param (bool) color: Is this piece white?
        :param (str) kind: What is the kind of this piece?
        :return (tuple) coord: The coordinate to which the piece should be sent.
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
        for k, v in self.stored:
            if len(v) == 0:
                continue
            print('Color: {}, Type: {}'.format('White' if k[0] else 'Black', k[1]))
            for loc in v:
                print('\t{}'.format(loc))


if __name__ == "__main__":
    game = ChessGame()
