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


        self.gameLoop()

    def movePiece(self, command):
        stripped_command = ''.join(l for l in command if not l.isupper())
        try:
            hi = self.board.push_san(command)
        except:
            print(stripped_command)
            hi = "Invalid command."
        print(hi)
        self.convertToLocation(stripped_command)

    def printBoard(self):
        print(self.board)

    def resetBoard(self):
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
