from datatypes import *
from chess import Board, Move, engine
from typing import List
from graveyard import Graveyard
# import chess
import chess.uci
import random

class Game(object):
    def __init__(self):
        self.board = Board()
        self.board.reset()

        self.running = True;
        self.turn = bool(random.getrandbits(1))
        self.engine = chess.uci.popen_engine('libs/stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        self.first = self.turn

        #TODO: THIS
        self.left_graveyard = Graveyard()
        self.right_graveyard = Graveyard()

        #Full location list
        self.whiteLocations = {'': [], 'R': [], 'N': [], 'B': [], 'K': [], 'Q': []}
        self.blackLocations = {'': [], 'r': [], 'n': [], 'b': [], 'k': [], 'q': []}

        # White Pieces
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

        #Misc. creation
        self.graveyard = Graveyard()

    def movePiece(self, command):
        """
            Moves a singular piece using a given command (in algebraic; no spaces).
            :param command: String
        """

        # TODO: HANDLE CASTLING AND IN PASSING (this block of code)
        if command == "Ke8g8":
            #kingside black castle attempt
            command ==  "Ke8f8"
        elif command == "Ke8c8":
            #queenside black castle attempt
            command == "Ke8d8"
        elif command == "Ke1g1":
            command == "Ke1f1"
        elif command == "Ke1c1":
            command == "Ke1d1"
        elif command == "0-0" or command == "0-0-0":
            print("Invalid command; no castling yet sorry.")
            print(self.board)
            self.turn = not self.turn
            return []
        print(command)

        #Try a command; if it fails then prevent a change in turn and make the player go.
        try:
            hi = self.board.push_san(command)
        except:
            return []

        stripped_command = ''.join(l for l in hi.uci() if l in '12345678abcdefgh')  #Strip the command so that it only has the before and after coordinates.
        #make sure that the uci is correct.
        assert (len(hi.uci()) == 4)

        #get the before/after coordinates
        loc1, loc2 = uciToLocations(stripped_command)

        moves = self.updateLocations(loc1, loc2)    #Updates the location of PIECES

        moves = moves + convertMoves(loc1, loc2)
        return moves

    def updateLocations(self, loc1, loc2):
        """
            Update the location of a piece by taking its original location (loc1) and moving it to the new location (loc2)
            :param loc1: String (letterNumber ex. a2)
            :param loc2: String (letterNumber ex. a3)
        """
        moves = [] # create a list to add the moves to
        #Get the pieces based on the locations passed in
        piece1 = self.findLocPiece(loc1)
        piece2 = self.findLocPiece(loc2)

        #Make sure that the second piece is moved to the graveyard first.
        if piece2 is not None: #Need to run this first because of path
            if loc2 in self.whiteLocations.get(piece2.upper()):
                print("Attempted white graveyard move")
                #black takes white, so true
                moves.append(self.graveyardMove(loc2, True))
            elif loc2 in self.blackLocations.get(piece2):
                print("Attempted black graveyard move")
                #white takes black, so false
                moves.append(self.graveyardMove(loc2, False))
            return moves + self.updateLocations(loc1, loc2)

        #Make the move, depending on whose turn it is.
        try:
            self.whiteLocations[piece1].remove(loc1)
            self.whiteLocations[piece1].append(loc2)
        except:
            pass
        try:
            self.blackLocations[piece1].remove(loc1)
            self.blackLocations[piece1].append(loc2)
        except:
            pass
        moves.append(convertMoves(loc1, loc2))
        return moves

    def graveyardMove(self, loc, iswhite = None):
        """
        Sends a piece to the graveyard, and removes it from the record of the board
        :param loc: two-character string representing location on board
        :return:
        """
        piece = self.findLocPiece(loc)
        print("Piece:",piece, "at", loc)
        if iswhite is not None:
            is_white = iswhite
        else:
            is_white = piece.isupper()
        print("White Piece?",is_white)

        # Remove the piece from its current square
        try:
            (self.whiteLocations if is_white else self.blackLocations)[piece].remove(loc)
        except:
            pass

        # Add the piece to the graveyard
        dest = self.graveyard.storePiece(is_white, piece)

        print("Sending piece {} at {} to graveyard {}".format(piece, loc, dest))
        return convertMoves(loc, dest)

    def reviveFromGraveyard(self, dest, piece):
        """
        Makes a move to revive the given piece from the graveyard, and marks its new position.
        :param dest: two-character code of space to fill
        :param piece: piece character (capital = white) to revive
        :return: A piece move from the source to the destination
        """

        is_white = piece.isupper()
        source = self.graveyard.retrievePiece(is_white, piece)
        # assert source is not None, "Tried to revive piece not in graveyard"

        if piece.lower() == 'p':
            piece = ''

        (self.whiteLocations if is_white else self.blackLocations)[piece].append(dest)

        print("The source is %s" % str(source))
        return convertMoves(source, dest)

    def printLocations(self):
        """
        Print the locations of all pieces saved by the game.
        """
        print("White locations")
        print(self.whiteLocations)
        print("Black locations")
        print(self.blackLocations)

    def findLocPiece(self, location):
        """
        Takes in a 2 letter/number string thatgives a square (e.g. a1, h8, etc.)
        returns P for white pawn, p for black pawn.
        """
        for x in self.whiteLocations:
            if location in self.whiteLocations[x]:
                return x
        for x in self.blackLocations:
            if location in self.blackLocations[x]:
                return x
        return None

    def printBoard(self):
        """
        Prints the board. Included as a separate function in case we want to print more than just the board when printing board in the future.
        """
        print(self.board)

    def resetBoard(self):
        """
        Resets the board to its starting (default) position.
        """
        toRevive = dict()
        moves = []

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

        #Actually revive the pieces
        for piece in toRevive:
            for locs in toRevive[piece]:
                moves.append(self.reviveFromGraveyard(locs, piece))

        #Make the board in the computer know it's reset.
        self.board.reset()
        #Prove that it's reset/print the start.
        self.printBoard()
        return moves

    @staticmethod
    def pairToLocation(position):
        """
        Takes in a string of length 2 formatted as 'e7'
        and returns a tuple of floats that index onto
        the board.
        :param position: string of length 2
        :return: tuple of location
        """
        assert(len(position) == 2)

        # Converts a 2-character UCI coordinate to a tuple
        loc = (float(ord(position[0]) - 97), float(position[1])-1)
        print(loc)
        assert (0. <= loc[0] < 8 and 0. <= loc[1] < 8)
        return loc

    def uciToLocations(self, command):
        """
        :param command: 4-character uci formatted string ex. "e5e7"
        :return: a pair of tuples
        """

        comm_string = str(command)
        return self.pairToLocation(comm_string[:2]), self.pairToLocation(comm_string[2:])

    def gameOver(self):
        """
        If the game is over, report the result and ask if people want to play again. If they don't, running becomes false and the game will stop.
        """

        # TODO: what happens when the game ends (do more?)
        resultant = self.board.result()
        if resultant == "1-0":
            print("Congratulations! White wins!")
        elif resultant == "0-1":
            print("Congratulations! Black wins!")
        else:
            print("It's a draw!")

        #reset the physical board as well as the saved board state
        self.resetBoard()

        #Ask the user if they want to play again.
        again = input("Want to play again? (y/n): ")
        if again.lower() == "n":
            self.running = False

    def checkGameOver(self):
        """
        Check to see if the game is over.
        :return: Boolean (true if game is over, else false)
        """
        if self.board.is_game_over():
            self.printBoard()
            return True
        else:
            return False

    def printKey(self):
        print("p: Print the board state.")
        print("k: Print the key." )
        print("m: Print legal moves.")
        print("r: Reset the board/game.")
        print("g: Print what's in the graveyard.")
        print("pl: Print locations of all pieces.")
        print("cm: Complete an easy checkmate.")

    def convertMoves(self, loc1, loc2):
        """
        Returns a PieceMove
        """
        #a is 97 in ascii, we're ofsetting by 3 in the long-direction (x)
        move1 = (ord(loc1[0]) - 97 + 3, ord(loc1[1]))
        move2 = (ord(loc2[0]) - 97 + 3, ord(loc2[1]))

        one = PieceCoord(move1[0], move2[1])
        two = PieceCoord(move2[0], move2[1])

        return PieceMove(one, two)

    def implementMove(self, command):
        """
        Allow the player to make a turn.
        Also allows other commands to view state of the board as debugging[]
        """
        # move = main()
        command = command.lower()
        if command == "p":
            self.printBoard()
        elif command == "k":
            self.printKey()
        elif command == "m":  # print legal moves
            print(self.board.legal_moves)
            for x in self.board.legal_moves:
                print(x)
        elif command == "r":  # fast reset of board
            self.resetBoard()
        elif command == "g":
            self.graveyard.printHi()
        elif command == "pl":
            self.printLocations()
        elif command == "cm":  # a very easy checkmate, for endgame testing
            moves = self.movePiece("e4")
            moves = self.movePiece("e5")
            moves = self.movePiece("Qh5")
            moves = self.movePiece("Nc6")
            moves = self.movePiece("Bc4")
            moves = self.movePiece("Nf6")
            moves = self.movePiece("Qf7")
        else:
            moves = movePiece(command)
            if moves != []:
                if self.checkGameOver():
                    self.gameOver()
                    return moves
                return moves
            else:
                print("That wasn't a good move. Try again.")

    def testImplementMove(self, move):
        """ Test version which takes a string instead of a move """
        return [PieceMove(PieceCoord(self.mapper[move[0]], int(move[1])-1), PieceCoord(self.mapper[move[2]], int(move[3])-1))]


if __name__ == "__main__":
    game = Game()
    print(game.implementMove('cm'))