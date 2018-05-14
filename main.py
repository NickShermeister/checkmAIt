#!/usr/bin/env python3
from time import sleep
from typing import List

import chess
import sys

from ai import aiController
from speech import SpeechInput
from game import Game
from motionPlanner import MotionPlanner
from controller import Controller
from game import Game


from datatypes import *


def main():
    debugFlag = False
    debugMoves = 0
    speech = SpeechInput()
    ai = aiController()
    planner = MotionPlanner()
    controller = Controller()
    attempt = 0

    game = Game()
    try:
        hi = sys.argv[1]
    except:
        hi = input("What debug mode? 0 = 2 players, 1 = 1 ai, 2 = 2 ai:  ")
    if(hi == "1"):
        print("Player vs. AI")
        while True:
            if game.board.turn == chess.WHITE and not debugFlag:
                print(game.board)
                command = speech.getCommand()
                try:
                    debugMoves = int(command)
                    debugFlag = True
                    aiMove = True
                    command = ai.getMove(game.board)
                except:
                    aiMove = False
            else:
                command = ai.getMove(game.board, attempt)
                aiMove = True
                if debugFlag:
                    debugMoves -= 1
                    if debugMoves == 0:
                        debugFlag = False

            if command == 'show':
                print(game.board)
            elif command:
                implementation = game.implementMove(str(command))

                if aiMove and not implementation:
                    print(game.board)
                    print("The AI did a goof. Sorry.")
                    attempt += 2
                    aiMove = False
                    # raise Exception("The AI tried to make the move {}, which is apparently illegal.".format(command))

                attempt = 0
                if aiMove:
                    for m in implementation:
                        steps = planner.make_command_list(m)  # type:List[Action]

                        for step in steps:
                            controller.makeMove(step)

            else:
                sleep(0.01)
    elif hi == "2":   #AI game
        print("AI duel")

        while(True):
            print(game.board)
            try:
                aiMove = True
                command = ai.getMove(game.board)
            except:
                aiMove = False

            if command:
                implementation = game.implementMove(str(command))

                if aiMove and not implementation:
                    print(game.board)
                    print("The AI did a goof. Sorry.")
                    attempt += 2
                    aiMove = False
                attempt = 0
                if aiMove:
                    for m in implementation:
                        print(m)
                        steps = planner.make_command_list(m)  # type:List[Action]

                        for step in steps:
                            controller.makeMove(step)

            else:
                sleep(1)

    else:
        print("Player v. Player")
        while True:
            print(game.board)
            command = speech.getCommand()

            if command == 'show':
                print(game.board)
            elif command:
                implementation = game.implementMove(str(command))
                attempt = 0

            else:
                sleep(0.01)


if __name__ == '__main__':
    main()
