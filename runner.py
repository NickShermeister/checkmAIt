"""
Chess Running script for Hack Holyoke 2017.
in order to import chess, run:
pip3 install python-chess
"""
import chess

class ChessGame():
    """docstring for ChessGame."""
    def __init__(self):
        self.board = chess.Board()
        self.running = True
        self.turn = True    #True means player makes first move; else AI makes first move.
        self.first = self.turn
        self.whiteGraveyard = {'':[], 'R':[], 'N':[], 'B':[], 'K':[], 'Q':[]} #empty string = pawn
        self.blackGraveyard = {'':[], 'r':[], 'n':[], 'b':[], 'k':[], 'q':[]}
        self.whiteLocations = {'':[], 'R':[], 'N':[], 'B':[], 'K':[], 'Q':[]}
        self.blackLocations = {'':[], 'r':[], 'n':[], 'b':[], 'k':[], 'q':[]}
        self.resetBoard()

        self.gameLoop()

    def movePiece(self, command):
        try:
            hi = self.board.push_san(command)
            # self.convertToLocation(stripped_command)
        except:
            print(stripped_command)
            hi = "Invalid command."
        print(hi)

        if len(hi.uci()) == 4:
            self.convertToLocation(hi.uci())

    def findLocPiece(self, location):
        """
        Takes in a 2 letter/number string thatgives a square (e.g. a1, h8, etc.)
        returns P for white pawn, p for black pawn.
        """
        for x in self.whiteLocations:
            if location in self.whiteLocations[x]:
                if x == "":
                    return "P"
                else:
                    return x
        for x in self.blackLocations:
            if location in self.blackLocations[x]:
                if x == "":
                    return "p"
                else:
                    return x
        return -1


    def printBoard(self):
        print(self.board)

    def resetBoard(self):
        #TODO: ROUTE TO MOVE PIECES BACK


        self.whiteLocations[''] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.whiteLocations['R'] = ['a1', 'h1']
        self.whiteLocations['N'] = ['b1', 'g1']
        self.whiteLocations['B'] = ['c1', 'f1']
        self.whiteLocations['K'] = ['d1']
        self.whiteLocations['Q'] = ['e1']

        self.blackLocations[''] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        self.blackLocations['r'] = ['a8', 'h8']
        self.blackLocations['n'] = ['b8', 'g8']
        self.blackLocations['b'] = ['c8', 'f8']
        self.blackLocations['k'] = ['d8']
        self.blackLocations['q'] = ['e8']

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
            elif x in "0123456789":
                final_string += str(x)+".0 "
            if count == 2:
                final_string += "-> "
        final_string+="\n"
        print(final_string)

    def aiMove(self):
        #TODO: IMPLEMENT AI AND HAVE IT TAKE A TURN
        pass

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

    def gameLoop(self):
        while(self.running):

            if (self.turn): #player turn
                move = input('Move: ')
                if move == "p":
                    self.printBoard()
                elif move == "m": #print legal moves
                    print(self.board.legal_moves)
                    for x in self.board.legal_moves:
                        print(x)
                elif move == "r": #fast reset of board
                    self.resetBoard()
                elif move == "cm": #a very easy checkmate, for endgame testing
                    self.movePiece("e4")
                    self.movePiece("e5")
                    self.movePiece("Qh5")
                    self.movePiece("Nc6")
                    self.movePiece("Bc4")
                    self.movePiece("Nf6")
                    self.movePiece("Qxf7")
                else:
                    self.movePiece(move)

                if self.checkGameOver(): #Check to see if the game is OVER
                    self.gameOver()
            else: #AI turn
                self.aiMove()
                if self.checkGameOver():
                    self.gameOver()

            self.turn = not self.turn
        print("Baiiiiiii")

if __name__ == "__main__":
    game = ChessGame()
