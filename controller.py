#!/usr/bin/env python3

import time

from datatypes import *


class RobotPosition(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Controller(object):
    def __init__(self, simulation=True, square_size=3.0, center=(30.0, 20.0)):
        self.square_size = square_size
        self.center = center

        self.simulation = simulation

    def makeMove(self, step: Action):
        if step.up:
            self.mag_up()

        elif step.down:
            self.mag_down()

        elif step.coord:
            self.goto_coord(step.coord)

    def mag_up(self):
        if self.simulation:
            print("Lifting the magnet!")
        else:
            raise NotImplementedError()

    def mag_down(self):
        if self.simulation:
            print("Lowering the magnet!")
        else:
            raise NotImplementedError()

    def goto_coord(self, coord:PieceCoord):
        self.goto_raw_coord(self._convert_coord(coord))

    def goto_raw_coord(self, pos: RobotPosition):
        if self.simulation:
            print("Moving to coordinates {}".format(pos))
        else:
            raise NotImplementedError()

    def _convert_coord(self, coord: PieceCoord):
        x = (coord.x - 6.5) * self.square_size + self.center[0]
        y = (coord.y - 3.5) * self.square_size + self.center[1]
        return RobotPosition(x, y)

def key_control():
    c = Controller()

    c.mag_down()

    print('Input: "x y" or "u" or "d": ')

    while True:
        try:
            s = input()
        except EOFError:
            time.sleep(0.01)
            continue

        s = s.strip()
        if s.lower() == 'u':
            c.mag_up()
            continue
        if s.lower() == 'd':
            c.mag_down()
            continue

        try:
            l = s.split(' ')
            pos = PieceCoord(float(l[0]), float(l[1]))

            c.goto_coord(pos)

        except Exception:
            print('Input two numbers separated by a space')

if __name__ == '__main__':
    key_control()