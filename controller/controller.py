#!/usr/bin/env python2
import struct

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
        dpos = pos.to_vector() - self.center

        radius = np.linalg.norm(dpos)

        # TODO: This is a placeholder, USE SOMETHING REAL
        return np.rad2deg(radius / self.arm1), np.rad2deg(np.arctan2(*dpos))


robot = Mechanism(20.0, 20.0, 4.0, (3.5, 3.5))


class Position(object):
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def as_joints(self, bot=robot):
        return bot.inverseKinemetics(self)

    def to_vector(self):
        return np.array([self.x, self.y])

    @staticmethod
    def from_vector(vec):
        return Position(*vec)


class Connection(object):
    SHOULDER_BOX = 0
    ELBOW_BOX = 1
    MAG_BOX = 2

    def __init__(self):
        self.brick = nxt.find_one_brick()
        print "Initialized!"

    def send_target(self, pos):
        """
        :type pos: Position
        """
        self.send_target_raw(*pos.as_joints())

    def send_target_raw(self, shoulder, elbow):
        self.brick.message_write(self.SHOULDER_BOX, struct.pack('f', shoulder))
        self.brick.message_write(self.ELBOW_BOX, struct.pack('f', elbow))

    def send_mag_up(self):
        s = 'U'
        # self.brick.message_write(self.MAG_BOX, s)
        self.brick.play_tone_and_wait(2000, 500)

    def send_mag_down(self):
        s = 'D'
        # self.brick.message_write(self.MAG_BOX, s)
        self.brick.play_tone_and_wait(1000, 500)

    def run_test(self):
        for box in range(5, 10):
            self.brick.message_write(box, 'message test %d' % box)
        for box in range(5, 10):
            local_box, message = self.brick.message_read(box, box, True)
            print local_box, message

        while True:
            t = time.time()
            angle = (t % 10)*50
            self.send_target_raw(angle, -angle)
            # self.send_mag_up()
            time.sleep(.1)
            # self.send_mag_down()
            # time.sleep(1.5)


if __name__ == '__main__':
    Connection().run_test()
