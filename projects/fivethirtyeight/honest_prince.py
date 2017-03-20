#!/usr/bin/env python
# coding=utf-8

"""
The Riddler, March 17, 2017
https://fivethirtyeight.com/features/can-you-find-the-honest-prince/

From Stephen Carrier, a puzzle about domestic boundaries:

Consider four square-shaped ranches, arranged in a two-by-two pattern,
as if part of a larger checkerboard. One family lives on each ranch, and
each family builds a small house independently at a random place within
the property. Later, as the families in adjacent quadrants become
acquainted, they construct straight-line paths between the houses that
go across the boundaries between the ranches, four in total. These paths
form a quadrilateral circuit path connecting all four houses. This
circuit path is also the boundary of the area where the families’
children are allowed to roam.

What is the probability that the children are able to travel in a
straight line from any allowed place to any other allowed place without
leaving the boundaries? (In other words, what is the probability that
the quadrilateral is convex?)

Results:
Of the 1000000 random samples, 91111 samples have a convex quadrilateral, or 9%.

"""

from __future__ import print_function

import argparse
import logging
import sys

from math import acos
from math import pi
from math import sqrt
from random import random


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "[{: 3.2f},{: 3.2f}]".format(self.x, self.y)

    def get_length(self, other_point):
        rise = other_point.y-self.y
        run = other_point.x-self.x

        return sqrt(rise**2 + run**2)

    def get_angle(self, top, bottom):
        """
        Return the angle, in degrees, between the two line segments,
        self-top, self-bottom.

        Using the Cosine Law:
        c2=a2+b2−2abcosθ.

        :param top: Point()
        :param bottom: Point()
        :return:
        """
        a = self.get_length(top)
        b = self.get_length(bottom)
        c = top.get_length(bottom)

        theta = acos((a**2 + b**2 - c**2)/(2*a*b))
        return theta * 180/pi

    # def get_angleX(self, top, bottom):
    #     """
    #     Return the angle, in degrees, between the two line segments,
    #     self-top, self-bottom.
    #
    #     :param top: Point()
    #     :param bottom: Point()
    #     :return:
    #     """
    #
    #     print(top, self, bottom)
    #     print((top.x-self.x), (top.y-self.y), atan(float(top.y-self.y)/(top.x-self.x)),
    #           atan(float(top.y - self.y) / (top.x - self.x)) * 180/pi)
    #     angle_to_top = atan(float(top.y-self.y)/(top.x-self.x)) * 180/pi
    #     # angle_to_bottom = atan((bottom.x-self.x)/(bottom.y-self.y)) * 180/pi
    #     angle_to_bottom = atan(float(self.y-bottom.y)/(self.x-bottom.x)) * 180/pi
    #
    #
    #     print(angle_to_top, angle_to_bottom)
    #
    #     angle = angle_to_top - angle_to_bottom
    #     print("{} - {} - {} has angle: {}"
    #           .format(top, self, bottom, angle))
    #
    #     print()
    #     return angle

    @staticmethod
    def random_float_no_zero(multiplier=1):
        x = 0
        while not x:
            x = random() * multiplier

        return x

    @staticmethod
    def create_random_point(quadrant, max_abs_value):
        x = Point.random_float_no_zero(max_abs_value)
        y = Point.random_float_no_zero(max_abs_value)

        if quadrant == 1:
            return Point(x, y)
        elif quadrant == 2:
            return Point(-x, y)
        elif quadrant == 3:
            return Point(-x, -y)
        elif quadrant == 4:
            return Point(x, -y)


class OuterSquare(object):
    def __init__(self, size):
        """
        Size is the size of each inner square.

        :param size:
        """
        self.size = size
        self.points = []
        self.convexity = False

    def reset(self):
        self.points = []
        self.convexity = False

    def populate_points(self):
        """
        Points a through d are in quadrants I through IV.  That is,
        point a is in +/+ quadrant, b is in -/+, c is in -/- and d is
        in +/-.
        :return:
        """
        a = Point.create_random_point(1, self.size)
        b = Point.create_random_point(2, self.size)
        c = Point.create_random_point(3, self.size)
        d = Point.create_random_point(4, self.size)

        self.points = [a, b, c, d]

    def test_convexity(self):
        a = self.points[0]
        b = self.points[1]
        c = self.points[2]
        d = self.points[3]
        total_angles = 0

        for tup in [(a, b, c), (b, c, d), (c, d, a), (d, a, b)]:
            angle = tup[1].get_angle(tup[0], tup[2])
            # print("{} {} {} gives us an angle of {}".format(tup[0], tup[1], tup[2], angle))
            total_angles += angle

        # print("TA: {:18f}".format(total_angles))

        # if total_angles != 360.0:
        # if -0.001 < (total_angles - 360.0) < 0.0001:
        if abs((total_angles - 360.0)) > 0.001:
        # if 0.001 < (total_angles - 360.0) or (total_angles - 360.0) < -0.001:
            print("CONVEX^^: 360 - {:9f} = {}".format(total_angles, 360-total_angles))
            # print("{}  ^^: {:18f}".format(self.convexity, (total_angles - 360.0)))
            self.convexity = True

    def to_string(self):
        s = ""
        for p in self.points:
            s += p.__str__() + ", "

        return s

    def pprint(self):
        print(self.to_string())


def set_logger(verbose_level):
    # Let there be debug.
    if verbose_level >= 2:
        logging_level = logging.DEBUG
    elif verbose_level == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR

    logging.basicConfig(level=logging_level,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description="This is a stub.")
    parser.add_argument("-i", "--important",
                        help="This is the important value that we really need.")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    square_size = 100
    # random_attempts = square_size * square_size
    random_attempts = 1000000

    convexity_ctr = 0
    os = OuterSquare(square_size)
    for i in range(1, random_attempts+1):
        os.reset()
        os.populate_points()
        # os.pprint()
        os.test_convexity()

        if os.convexity:
            # print("The children cannot walk in a straight line.")
            convexity_ctr += 1
            # print("convex counter: {}".format(convexity_ctr))

    print("\nOf the {} random samples, {} samples have a convex quadrilateral, or {}%."
          .format(random_attempts, convexity_ctr, 100*convexity_ctr/random_attempts))

if __name__ == "__main__":
    main()
    #
    # os = OuterSquare(100)
    # a = Point(1, 99)
    # b = Point(-99, 1)
    # c = Point(-1, -99)
    # d = Point(99, -1)
    # os.points = [a, b, c, d]
    # os.pprint()
    # print()
    # os.test_convexity()
    # print(os.convexity)
    #
    # a = Point(20, 20)
    # b = Point(0, 0)
    # c = Point(-20, 20)
    # print("-" * 20)
    # print(    b.get_angle(a, c))
    # print("-" * 20)
