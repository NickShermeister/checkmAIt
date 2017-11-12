#!/usr/bin/env python2
"""
Requires: python-nxt
        pyserial
"""

import struct

import nxt
import numpy as np

import time

import serial


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
            return 0, 180 / self.el_gear

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


robot = Mechanism(16.0, 3.7, (3.5, 3.5))


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
        try:
            self.brick = nxt.find_one_brick()
            self.has_brick = True
            self.arduino = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600)
        except:
            self.brick = None
            self.has_brick = False
            print "NO BRICK CONNECTED"

        print "Initialized!"

    def send_target(self, pos):
        """
        :type pos: Position
        """
        self.send_target_raw(*pos.as_joints())

    def send_target_raw(self, shoulder, elbow):
        print "Sending target (s,e): ", (shoulder, elbow)
        if self.has_brick:
            self.brick.message_write(self.SHOULDER_BOX, struct.pack('f', shoulder))
            self.brick.message_write(self.ELBOW_BOX, struct.pack('f', elbow))
        else:
            print "NO BRICK CONNECTED"

        time.sleep(2)

    def send_mag_up(self):
        if self.has_brick:
            s = 'U\n'
            self.arduino.write(s)
            self.brick.play_tone_and_wait(1415, 100)
        else:
            print "NO BRICK CONNECTED: Mag up"

        time.sleep(1)

    def send_mag_down(self):
        if self.has_brick:
            s = 'D\n'
            self.arduino.write(s)
            self.brick.play_tone_and_wait(1415, 100)
        else:
            print "NO BRICK CONNECTED: Mag down"

    def run_test(self):
        if self.has_brick:
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
        if self.has_brick:
            for box in range(5, 10):
                self.brick.message_write(box, 'message test %d' % box)
            for box in range(5, 10):
                local_box, message = self.brick.message_read(box, box, True)
                print local_box, message

        # self.send_target_raw(0, 0)

        self.send_mag_down()

        while True:
            # s = raw_input('Input: "x y" or "u" or "d": ')
            try:
                s = raw_input()
            except EOFError:
                time.sleep(0.01)
                continue
                
            s = s.strip()
            if s.lower() == 'u':
                self.send_mag_up()
                continue
            if s.lower() == 'd':
                self.send_mag_down()
                continue

            l = s.split(' ')
            pos = Position(float(l[0]), float(l[1]))

            self.send_target(pos)


if __name__ == '__main__':
    Connection().key_control()
