#!/usr/bin/env python2
import struct

import nxt
import numpy as np

import time


class Mechanism(object):
    def __init__(self, arm_length, gridsize, center):
        """All units in cm"""
        self.gridsize = gridsize
        self.arm_length = arm_length
        self.center = np.array(center)

        self.sh_gear = -12.0 / 36  # joint moves ** times what motor does
        self.el_gear = -12.0 / 36

    def inverseKinemetics(self, pos):
        """

        :type pos: Position in grid coordinates
        :returns: tuple of (shoulder angle, elbow angle) in degrees
        """
        dpos = (pos.to_vector() - self.center) * self.gridsize  # In cm

        if (dpos == np.array([0, 0])).all():
            return 0, 180/self.el_gear

        radius = np.linalg.norm(dpos)

        print pos.to_vector(), dpos, radius

        # a1 is angle between the lower arm (arm1) and the position vector
        a1 = np.rad2deg(np.arccos((radius) / (2 * self.arm_length)))
        # a2 is the angle between the two arms
        a2 = 180 - 2 * a1
        # a3 is the angle between vertical and position vector
        a3 = np.rad2deg(np.arctan2(-dpos[0], dpos[1]))

        sh_angle = a3 + a1  # shoulder angle
        el_angle = 180 - a2  # elbow angle

        print "World angles (s,e): ", sh_angle, el_angle
        return sh_angle / self.sh_gear, el_angle / self.el_gear


robot = Mechanism(16.0, 3.7, (0, 0))


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
        print "Sending target (s,e): ", (shoulder, elbow)
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
            angle = (t % 10) * 50
            self.send_target_raw(angle, -angle)
            # self.send_mag_up()
            time.sleep(.1)
            # self.send_mag_down()
            # time.sleep(1.5)

    def key_control(self):
        for box in range(5, 10):
            self.brick.message_write(box, 'message test %d' % box)
        for box in range(5, 10):
            local_box, message = self.brick.message_read(box, box, True)
            print local_box, message

        self.send_target_raw(0, 0)

        while True:
            s = raw_input('Input: "x y"')
            l = s.split(' ')
            pos = Position(float(l[0]), float(l[1]))

            self.send_target(pos)


if __name__ == '__main__':
    Connection().key_control()
