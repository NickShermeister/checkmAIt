
from datatypes import *
from chess import Board, Move, engine
from typing import List
from graveyard import Graveyard
# import chess
import chess.uci
import random
import sys

class Game(object):
    def __init__(self):
        self.board = Board()
        self.board.reset()

        self.running = True;
        self.turn = bool(random.getrandbits(1))
        self.engine = chess.uci.popen_engine('stockfish-8-linux/src/stockfish')   
        self.engine.uci()
        self.first = self.turn

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


        # elif command == "0-0" or command == "0-0-0":
        #     print("Invalid command; no castling yet sorry.")
        #     print(self.board)
        #     self.turn = not self.turn
        #     return []
        promo = False
        moves = []
        if(len(command) > 4):
            if(command[-1] in "12345678"):
                command = command[0].upper() + command[1:]
            else:
                command = command[:-1] + command[-1].upper()
        elif(len(command) == 4):

            try:
                command = self.findLocPiece(command[0:2]).upper() + command
                if(len(command) == 4):
                    if(command[-1] in ["1", "8"]):
                        command = command + input("What piece do you want? \nKnight: N\nRook: R\nBishop: B\nQueen: Q\n").upper()
                        promo = True

            except:
                print(command)
                print("fuk off m8")
                print(self.whiteLocations)
                print(self.blackLocations)
                return []
        print(command)

        #Try a command; if it fails then prevent a change in turn and make the player go.
        try:

            if command in ["Ke1h1", "Ke1g1", "e1h1", "e1g1"]:
                command = "O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("h1", "f1")
            elif command in ["Ke1a1", "Ke1c1", "e1a1", "e1c1"]:
                command = "O-O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("a1", "d1")
            elif command in ["ke8h8", "Ke8g8", "ke8g8", "ke8h8", "e8h8", "e8g8"]:
                command = "O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("h8", "f8")
            elif command in ["ke8a8", "Ke8c8", "ke8c8", "ke8a8", "e8a8", "e8c8"]:
                command = "O-O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("a8", "d8")
            elif command == "0-0" and self.board.turn:
                command = "O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("h1", "f1")
            elif command == "0-0":
                command = "O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("h8", "f8")
            elif command == "0-0-0" and self.board.turn:
                command = "O-O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("a1", "d1")
            elif command == "0-0-0":
                command = "O-O-O"
                hi = self.board.push_san(command)
                moves = moves + self.updateLocations("a8", "d8")
            elif promo:
                if(self.board.turn):
                    pieceRevived = command[-1].upper()
                else:
                    pieceRevived = command[-1].lower()
                hi = self.board.push_san(command)
                #Send current pawn to graveyardMove
                #Revive queen...
                print("test1")
                tempmove = self.graveyardMove(command[0:2])
                moves.append(tempmove)
                print("test2")
                moves.append(self.reviveFromGraveyard(command[2:4], pieceRevived))
                print("test3")
                print("Moves:")
                print(str(moves))
                return moves
            else:
                hi = self.board.push_san(command)
        except Exception as e:
            print("We broke f00l. Error:\n", e)
            return []

        print("Hi is: " + str(hi))
        stripped_command = ''.join(l for l in hi.uci() if l in '12345678abcdefgh')  #Strip the command so that it only has the before and after coordinates.
        #make sure that the uci is correct.
        # assert (len(hi.uci()) == 4)
        if(len(hi.uci()) == 4):
        #get the before/after coordinates
            loc1 = stripped_command[0:2]
            loc2 = stripped_command[2:]

            moves = moves + self.updateLocations(loc1, loc2)    #Updates the location of PIECES
        elif(len(hi.uci()) == 5):
            print("Moves:")
            print(str(moves))
            if(not self.board.turn):
                pieceRevived = stripped_command[-1].upper()
            else:
                pieceRevived = stripped_command[-1].lower()
            #Send current pawn to graveyardMove
            #Revive queen...
            print("test1ai")
            tempmove = self.graveyardMove(stripped_command[0:2])
            moves.append(tempmove)
            print("test2ai")
            print(str(moves), '\n', pieceRevived)
            moves.append(self.reviveFromGraveyard(stripped_command[2:4], pieceRevived))
            print("test3ai")
        print("Moves:")
        print(str(moves))
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
        if piece1 is not None: #Need to run this first because of path
            if loc1 in self.whiteLocations.get(piece1.upper()):
                self.whiteLocations[piece1].remove(loc1)
                self.whiteLocations[piece1].append(loc2)
            else:
                self.blackLocations[piece1].remove(loc1)
                self.blackLocations[piece1].append(loc2)
        loc1fix, loc2fix = self.uciToLocations(loc1+loc2)
        moves.append(PieceMove(loc1fix, loc2fix))
        return moves

    def graveyardMove(self, loc, iswhite = None):
        """
        Sends a piece to the graveyard, and removes it from the record of the board
        :param loc: two-character string representing location on board
        :return:
        """
        piece = self.findLocPiece(loc)
        # print("Piece:",piece, "at", loc)
        if iswhite is not None:
            is_white = iswhite
        else:
            is_white = piece.isupper()
        # print("White Piece?",is_white)

        # Remove the piece from its current square
        try:
            (self.whiteLocations if is_white else self.blackLocations)[piece].remove(loc)
        except:
            pass
        # Add the piece to the graveyard
        dest = self.graveyard.storePiece(is_white, piece)
        loc_tuple = self.pairToLocation(loc)

        print("Sending piece {} at {} to graveyard {}".format(piece, loc_tuple, dest))
        return PieceMove(loc_tuple, dest)

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
        # if(source == None):
        #     source = self.graveyard.retrievePiece(is_white, '')
        #     piece = ''

        if piece.lower() == 'p':
            piece = ''

        (self.whiteLocations if is_white else self.blackLocations)[piece].append(dest)

        print("The source is %s" % str(source))
        return self.convertMoves(source, dest)

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
        loc = (int(ord(position[0]) - 97), int(position[1])-1)
        # print(loc)
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
        # print("convertMoves")
        print("Loc1 is a", type(loc1), "\nLoc2 is a", type(loc2))

        if(type(loc1)!=PieceCoord):
            move1 = (ord(loc1[0]) - 97 + 3, ord(loc1[1]))
            one = PieceCoord(move1[0], move2[1])
        else:
            one = loc1

        if(type(loc2)!=PieceCoord):
            move2 = (ord(loc2[0]) - 97 + 3, ord(loc2[1]))
            two = PieceCoord(move2[0], move2[1])
        else:
            two = loc2


        return PieceMove(one, two)

    def implementMove(self, command):
        """
        Allow the player to make a turn.
        Also allows other commands to view state of the board as debugging[]
        """
        moves = []
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
            moves = moves + self.movePiece("e4")
            moves = moves + self.movePiece("e5")
            moves = moves + self.movePiece("Qh5")
            moves = moves + self.movePiece("Nc6")
            moves = moves + self.movePiece("Bc4")
            moves = moves + self.movePiece("Nf6")
            moves = moves + self.movePiece("Qf7")
        elif command == "exit":
            sys.exit(0)
        else:
            moves = moves + self.movePiece(command)
            if moves != []:
                if self.checkGameOver():
                    self.gameOver()
            else:
                print("That wasn't a good move. Try again.")
        return moves

    def testImplementMove(self, move):
        """ Test version which takes a string instead of a move """
        return [PieceMove(PieceCoord(self.mapper[move[0]], int(move[1])-1), PieceCoord(self.mapper[move[2]], int(move[3])-1))]


if __name__ == "__main__":
    game = Game()
    print(game.implementMove('cm'))
