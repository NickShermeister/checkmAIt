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
            # implementation = game.implementMove(command)
            implementation = game.testImplementMove(str(command))

            for m in implementation:
                steps = planner.make_command_list(m)  # type:List[Action]

                for step in steps:
                    controller.makeMove(step)

            response = ai.getMove(game.board)
            print(response)

            # implementation = game.implementMove(response)
            implementation = game.testImplementMove(str(response))

            for m in implementation:
                steps = planner.make_command_list(m)  # type:List[Action]

                for step in steps:
                    controller.makeMove(step)
        else:
            sleep(0.01)


if __name__ == '__main__':
    main()
