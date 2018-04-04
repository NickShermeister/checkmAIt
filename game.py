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
        # self.mp = MotionPlanner()

        #enter main loop
        # self.gameLoop()

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
            return False
        print(command)

        #Try a command; if it fails then prevent a change in turn and make the player go.
        try:
            hi = self.board.push_san(command)
        except:
            return False

        stripped_command = ''.join(l for l in hi.uci() if l in '12345678abcdefgh')  #Strip the command so that it only has the before and after coordinates.

        #get the before/after coordinates
        loc1 = stripped_command[0:2]
        loc2 = stripped_command[2:]

        self.updateLocations(loc1, loc2)    #Updates the location of PIECES

        #make sure that the uci is correct.
        assert (len(hi.uci()) == 4)

        #Move the piece (currently inactive as we switch to Gantry).
        src, dest = self.uciToLocations(self.convertMoves(loc1, loc2))
        return True
        # self.mp.run(self.output_move(src, dest))

    def updateLocations(self, loc1, loc2):
        """
            Update the location of a piece by taking its original location (loc1) and moving it to the new location (loc2)
            :param loc1: String (letterNumber ex. a2)
            :param loc2: String (letterNumber ex. a3)
        """

        #Get the pieces based on the locations passed in
        piece1 = self.findLocPiece(loc1)
        piece2 = self.findLocPiece(loc2)

        #TODO: DETERMINE WHY THIS IS HERE; seems redundant/useless
        # if piece1 == piece2:
        #     piece2 = None

        # Print debugging code.
        # print("Loc 1: %s" % loc1)
        # print("Loc 2: %s" % loc2)
        # print(piece1)
        # print(piece2)
        # print("Good1")
        # print("Piece1 : %s " % piece1)
        # print("Piece2 : %s " % piece2)

        #Make sure that the second piece is moved to the graveyard first.
        if piece2 is not None: #Need to run this first because of pathing
            # print(piece2 + ".")
            # print(loc2)
            # print("Should we be here?")
            # hi = loc1+loc2
            # src, dest = self.uciToLocations(hi)
            # print(dest)
            # temp = self.mp.capture(self.output_move(src, dest))
            # temp = self.convertBack(temp)
            if loc2 in self.whiteLocations.get(piece2.upper()):
                print("Attempted white graveyard move")
                #black takes white, so true
                self.graveyardMove(loc2, True)
            elif loc2 in self.blackLocations.get(piece2):
                print("Attempted black graveyard move")
                #white takes black, so false
                self.graveyardMove(loc2, False)
            return self.updateLocations(loc1, loc2)

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

    def convertBack(self, numerals):
        """
            Converts a numeral command to a string Command. Used for captures.
            :param numerals: String (of numerical command)
            :return: String (algebraic notation)
        """
        # print("Numerals: ")
        # print(numerals)
        # print(type(numerals))
        part1 = str(chr(int(numerals[0])+97))
        part2 = str(int(numerals[1]+1))
        return part1+part2

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
        # print(self.output_move(loc,dest))
        # temp = self.pairToLocation(loc)
        # print(temp)
        # self.mp.run(self.output_move(self.pairToLocation(loc), dest))

    def reviveFromGraveyard(self, dest, piece):
        """
        Makes a move to revive the given piece from the graveyard, and marks its new position.
        :param dest: two-character code of space to fill
        :param piece: piece character (capital = white) to revive
        :return:
        """

        is_white = piece.isupper()
        source = self.graveyard.retrievePiece(is_white, piece)
        # assert source is not None, "Tried to revive piece not in graveyard"

        if piece.lower() == 'p':
            piece = ''

        (self.whiteLocations if is_white else self.blackLocations)[piece].append(dest)

        print("The source is %s" % str(source))
        # self.mp.run(self.output_move(source, self.pairToLocation(dest)))

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
        # print(self.whiteLocations)
        # print(location)
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

        #Actually revive the pieces
        for piece in toRevive:
            for locs in toRevive[piece]:
                self.reviveFromGraveyard(locs, piece)

        #Make the board in the computer know it's reset.
        self.board.reset()
        #Prove that it's reset/print the start.
        self.printBoard()

    def output_move(self, source, dest):
        """
        :param source: Coordinates of the source (tuple in board coordinates)
        :param dest: Coordinates of the destination (tuple in board coordinates
        :return: corresponding PieceMove
        """

        src = PieceCoord(source[0]+3, source[1])
        dest = PieceCoord(dest[0]+3, dest[1])
        return PieceMove(src, dest)

    @staticmethod
    def pairToLocation(pair):
        """
        Take in a touple of length two and convert it to numbers for movement purposes.
        :param pair: tuple of strings len 2
        """
        # print(pair)
        # print(len(pair))
        assert(len(pair) == 2)

        # Converts a 2-character UCI coordinate to a tuple
        loc = (float(ord(pair[0]) - 97), float(pair[1])-1)
        print(loc)
        assert (0. <= loc[0] < 8 and 0. <= loc[1] < 8)
        return loc

    def uciToLocations(self, command):
        """
        :param command: 4-character uci formatted string ex. "e5e7"
        :return:
        """

        comm_string = str(command)
        return self.pairToLocation(comm_string[:2]), self.pairToLocation(comm_string[2:])

    def aiMove(self):
        """
        Function to have the AI move.
        TODO: Allow AI to start as black.
        """
        self.engine.position(self.board)    #Pass in the board's current state to the game engine.
        test = self.engine.go(movetime=300) #Movetime in milliseconds to generate best move.
        full_move_string = str(test[0])
        # print("hi")
        # print(full_move_string)


        #Need this because we need to get the piece name; the AI just returns locations.
        part1 = self.findLocPiece(full_move_string[0:2]) #get the piece from the dictionary
        move_for_board = part1.upper() +full_move_string  #sum the two parts again.
        print("Being passed into movePiece: %s " % move_for_board)
        self.movePiece(move_for_board)

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
            # TODO: get why it is over (stalemate, checkmate)
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


    def playerTurn(self):
        """
        Allow the player to make a turn.
        Also allows other commands to view state of the board as debugging[]
        """
        # move = main()
        move = input('Move: ')
        move = move.lower()
        if move == "p":
            self.printBoard()
        elif move == "k":
            self.printKey()
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
            self.movePiece("e5")
            self.movePiece("Qh5")
            self.movePiece("Nc6")
            self.movePiece("Bc4")
            self.movePiece("Nf6")
            self.movePiece("Qf7")
        else:
            if(self.movePiece(move)):
                if self.checkGameOver():
                    self.gameOver()
                self.aiMove()
            else:
                print("That wasn't a good move. Try again.")

    def gameLoop(self):
        if(not self.turn):
            self.aiMove()
        while (self.running):
            self.playerTurn()
            if self.checkGameOver():
                self.gameOver()
        print("Thanks for playing!")

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

    def validateMove(self, Move):
        """ Checks to make sure the move is valid """
        move = move.lower()
        if move == "p":
            self.printBoard()
        elif move == "k":
            self.printKey()
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
        else:
            mv = self.movePiece(move)
            if mv[0]:
                src = PieceCoord(mv[1][0], mv[1][1])
                dest = PieceCoord(mv[2][0], mv[2][1])
                if self.checkGameOver():
                    self.gameOver()
                return PieceMove(src, dest)
            else:
                print("That wasn't a good move. Try again.")

    def testImplementMove(self, move):
        """ Test version which takes a string instead of a move """
        return [PieceMove(PieceCoord(self.mapper[move[0]], int(move[1])-1), PieceCoord(self.mapper[move[2]], int(move[3])-1))]
    #
    def implementMove(self, move): # -> List[PieceMove]:
        moves = []
        moves.append(validateMove(move))
        return validateMove(move)
        # return [PieceMove(PieceCoord(5, 0), PieceCoord(5, 3))]


if __name__ == "__main__":
    game = Game()
    game.gameLoop()


# =======
#         self.left_graveyard = "TODO: this"
#         self.right_graveyard = "TODO: this"
#         self.mapper = {'a':3, 'b':4, 'c':5, 'd':6,
#         				'e':7, 'f':8, 'g':9, 'h':10
#         }
#
