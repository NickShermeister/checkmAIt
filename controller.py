#!/usr/bin/env python3

import time

import numpy as np
from datatypes import *
import serial


class RobotPosition(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Controller(object):
    UP_POS = 46
    DOWN_POS = 70
    CALIB = 'M92 Y50 Z50'

    def __init__(self, simulation=False, square_size=2.54, center=(18.0, 10.0), speed=500):
        self.speed = speed  # In mm/sec
        self.square_size = square_size
        self.center = center

        self.simulation = simulation

        self.lastpos = RobotPosition(0, 0)

        if not simulation:
            try:
                self.serial = serial.serial_for_url('/dev/ttyACM0', baudrate=115200)
            except serial.serialutil.SerialException:
                print("Unable to initialize serial! Falling back to simulation mode!")
                self.simulation = True

    def makeMove(self, step: Action):
        if step.up:
            self.mag_up()

        elif step.down:
            self.mag_down()

        elif step.coord:
            self.goto_coord(step.coord)

    def write_serial(self, data: str):
        self.serial.write((data+'\n').encode())
        print("Sent command: '{}'".format(data))
        # TODO: remove this once we trust the system
        if True:
            time.sleep(1)
            response = self.serial.read_all().decode().strip()
            print("Got response: '{}'".format(response))

    def mag_up(self):
        if self.simulation:
            print("Lifting the magnet!")
        else:
            command = 'M280 P0 S{}'.format(self.UP_POS)
            self.write_serial(command)

    def mag_down(self):
        if self.simulation:
            print("Lowering the magnet!")
        else:
            command = 'M280 P0 S{}'.format(self.DOWN_POS)
            self.write_serial(command)

    def goto_coord(self, coord: PieceCoord):
        self.goto_raw_coord(self._convert_coord(coord))

    def goto_raw_coord(self, pos: RobotPosition):
        if self.simulation:
            print("Moving to coordinates {}".format(pos))
        else:
            dist = np.sqrt((pos.x - self.lastpos.x)**2 + (pos.y - self.lastpos.y)**2)
            command = 'G0 Y{y} Z{z} E{e} F{f}'.format(y=pos.y, z=pos.x, e=dist, f=self.speed)
            self.write_serial(self.CALIB)
            self.write_serial(command)
            self.lastpos = pos

    def _convert_coord(self, coord: PieceCoord):
        x = (coord.x - 6.5) * self.square_size + self.center[0]
        y = (coord.y - 3.5) * self.square_size + self.center[1]
        return RobotPosition(x, y)

    def run_test(self):
        self.mag_down()
        for x in range(0, 10, 0.1):
            self.goto_raw_coord(RobotPosition(x, 0))
            time.sleep(.1)


def key_control():
    c = Controller(simulation=False)

    print('Input: "x y" or "r x y" or "u" or "d": ')

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

        if s and s.lower()[0] == 'r':
            try:
                l = s[1:].strip().split(' ')
                pos = RobotPosition(float(l[0]), float(l[1]))

                c.goto_raw_coord(pos)

            except Exception as e:
                print('Input two numbers separated by a space', e)
            continue

        try:
            l = s.split(' ')
            pos = PieceCoord(float(l[0]), float(l[1]))

            c.goto_coord(pos)

        except Exception as e:
            print('Input two numbers separated by a space')


if __name__ == '__main__':
    key_control()
