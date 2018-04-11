#!/usr/bin/env python3
from time import sleep
from typing import List

from ai import aiController
from speech import SpeechInput
from game import Game
from motionPlanner import MotionPlanner
from controller import Controller
from game import Game

from datatypes import *


def main():
    speech = SpeechInput()
    ai = aiController()
    planner = MotionPlanner()
    controller = Controller()

    game = Game()

    while True:
        command = speech.getCommand()
        if command:
            implementation = game.implementMove(str(command))

            for m in implementation:
                steps = planner.make_command_list(m)  # type:List[Action]

                for step in steps:
                    controller.makeMove(step)

            if len(implementation) > 0:
                response = ai.getMove(game.board)
                implementation = game.implementMove(str(response))

                for m in implementation:
                    steps = planner.make_command_list(m)  # type:List[Action]

                    for step in steps:
                        controller.makeMove(step)
        else:
            sleep(0.01)


if __name__ == '__main__':
    main()
