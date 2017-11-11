#!/usr/bin/env python2

import nxt
import numpy as np

import time


class Mechanism(object):
    def __init__(self, arm1, arm2, gridsize, center):
        """All units in cm"""
        self.gridsize = gridsize
        self.arm2 = arm2
        self.arm1 = arm1
        self.center = np.array(center)

    def inverseKinemetics(self, pos):
        """

        :type pos: Position
        :returns: tuple of (shoulder angle, elbow angle) in degrees
        """
        dpos = pos.as_vector() - self.center

        radius = np.linalg.norm(dpos)

        # TODO: This is a placeholder, USE SOMETHING REAL
        return np.rad2deg(radius / self.arm1), np.rad2deg(np.arctan2(*dpos))


robot = Mechanism(20.0, 20.0, 4.0, (3.5, 3.5))

class Position(object):
    def __init__(self, x, y):
        self.y = y
        self.x = x


    def as_joints_str(self, bot=robot):
        return "{} {}".format(*bot.inverseKinemetics(self))

    def as_vector(self):
        return np.array([self.x, self.y])


class Connection(object):
    def __init__(self):
        self.brick = nxt.find_one_brick()

    def send_target(self, pos):

        """
        :type pos: Position
        """
        s = 'M ' + pos.as_joints_str()
        self.brick.something(())

    def run_test(self):
        while True:
            self.brick.play_tone_and_wait(np.random.randint(1000, 2000), 500)
            time.sleep(1.5)

if __name__ == '__main__':
    Connection().run_test()
