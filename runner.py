"""
Chess Running script for Hack Holyoke 2017.
in order to import chess, run:
pip3 install python-chess
"""
import chess
import chess.uci

class ChessGame():
    """docstring for ChessGame."""
    def __init__(self):
        self.board = chess.Board()
        self.running = True
        self.turn = True    #True means player makes first move; else AI makes first move.
        #first player is always white
        self.engine = chess.uci.popen_engine('stockfish-8-linux/Linux/stockfish_8_x64')
        self.engine.uci()
        self.first = self.turn
        self.whiteGraveyard = {'':[], 'R':[], 'N':[], 'B':[], 'K':[], 'Q':[]} #empty string = pawn
        self.blackGraveyard = {'':[], 'r':[], 'n':[], 'b':[], 'k':[], 'q':[]}
        self.whiteLocations = {'':[], 'R':[], 'N':[], 'B':[], 'K':[], 'Q':[]}
        self.blackLocations = {'':[], 'r':[], 'n':[], 'b':[], 'k':[], 'q':[]}
        self.whiteGraves = 0
        self.blackGraves = 0
        self.resetBoard()

        self.gameLoop()

    def movePiece(self, command):
        #TODO: HANDLE CASTLING AND IN PASSING
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
        if len(hi.uci()) == 4:
            self.convertToLocation(hi.uci())



    def updateLocations(self, loc1, loc2):
        # print("Loc 1: %s" % loc1)
        # print("Loc 1: %s" % loc2)
        piece1 = self.findLocPiece(loc1)
        piece2 = self.findLocPiece(loc2)
        # print("Good1")
        # print("Piece1 : %s " % piece1)
        # print("Piece2 : %s " % piece2)
        if self.turn:
            # print(self.whiteLocations[piece1])
            self.whiteLocations[piece1].remove(loc1)
            self.whiteLocations[piece1].append(loc2)
            # print("Good2")
            if piece2:
                print("Good3")
                self.graveyardMove(loc2, False)
                self.blackLocations[piece2].remove(loc2)
                self.blackGraveyard[piece2].append(self.blackGraves)
                self.blackGraves+=1
        else:
            # print("Oh Boy.")
            # print(self.blackLocations[piece1])
            self.blackLocations[piece1].remove(loc1)
            self.blackLocations[piece1].append(loc2)
            if piece2:
                self.graveyardMove(loc2, True)
                self.whiteLocations[piece2].remove(loc2)
                self.whiteGraveyard[piece2].append(self.whiteGraves)
                self.whiteGraves+=1

    def graveyardMove(self, loc, color): #false for black, true for white

        pass

    def printLocations(self):
        print("White locations")
        print(self.whiteLocations)
        print("Black locations")
        print(self.blackLocations)

    def printGraves(self):
        print("White graves/graveyard:")
        print(self.whiteGraves)
        print(self.whiteGraveyard)
        print("Black graves/graveyard;")
        print(self.blackGraves)
        print(self.blackGraveyard)

    def findLocPiece(self, location):
        """
        Takes in a 2 letter/number string thatgives a square (e.g. a1, h8, etc.)
        returns P for white pawn, p for black pawn.
        """
        # print(location)
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
        #TODO: ROUTE TO MOVE PIECES BACK



        self.whiteLocations[''] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.whiteLocations['R'] = ['a1', 'h1']
        self.whiteLocations['N'] = ['b1', 'g1']
        self.whiteLocations['B'] = ['c1', 'f1']
        self.whiteLocations['K'] = ['e1']
        self.whiteLocations['Q'] = ['d1']

        self.blackLocations[''] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        self.blackLocations['r'] = ['a8', 'h8']
        self.blackLocations['n'] = ['b8', 'g8']
        self.blackLocations['b'] = ['c8', 'f8']
        self.blackLocations['k'] = ['e8']
        self.blackLocations['q'] = ['d8']

        self.board.reset()
        self.printBoard()

    def convertToLocation(self, command):
        """Command types:
        "xinitial yinitial -> xfinal yfinal"
        """
        final_string = ""
        count = 0
        for x in command:
            count += 1
            if x in "abcdefgh":
                final_string += str(ord(x) - 96)+".0 "
            elif x in "12345678":
                final_string += str(x)+".0 "
            if count == 2:
                final_string += "-> "
        final_string+="\n"
        print(final_string)

    def aiMove(self):
        self.engine.position(self.board)
        test = self.engine.go(movetime=300)
        hi = str(test[0])
        print(hi)
        Nf3 = chess.Move.from_uci(hi)
        self.board.push(Nf3)

        # self.movePiece(hi)
        self.turn = not self.turn

    def gameOver(self):
        #TODO: what happens when the gamae ends
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
            self.running=False


    def checkGameOver(self):
        if self.board.is_game_over():
            #TODO: get why it is over (stalemate, checkmate)
            return True
        else:
            return False

    def playerTurn(self):
        move = input('Move: ')
        if move == "p":
            self.printBoard()
        elif move == "m": #print legal moves
            print(self.board.legal_moves)
            for x in self.board.legal_moves:
                print(x)
        elif move == "r": #fast reset of board
            self.resetBoard()
        elif move == "g":
            self.printGraves()
        elif move == "pl":
            self.printLocations()
        elif move == "cm": #a very easy checkmate, for endgame testing
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
        while(self.running):
            print("Player turn (T=white, F=black): %s" % self.turn)
            if(self.turn): #player turn
                self.playerTurn()

            else: #AI turn=
                self.aiMove()

            if self.checkGameOver():
                self.gameOver()
        print("Baiiiiiii")

if __name__ == "__main__":
    game = ChessGame()
