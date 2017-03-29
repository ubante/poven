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
Of the 1000000 random samples, 91111 samples have a convex
quadrilateral, or 9%.

Which means the probability that the children can travel without leaving
the quadrilateral is 91%.

"""

from __future__ import print_function

import argparse
import logging
import matplotlib.pyplot as plt
import sys

from math import acos
from math import pi
from math import sqrt
from random import random
from time import sleep


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

    def draw_points(self, blue_points, axis_ctr):
        """
        One day, use the axis_ctr as a title or label to show progress.

        :param blue_points:
        :param axis_ctr:
        :return:
        """
        x_axis = []
        y_axis = []
        for point in self.points:
            x_axis.append(point.x)
            y_axis.append(point.y)

        x_axis.append(self.points[0].x)
        y_axis.append(self.points[0].y)

        # plt.clf()
        # axis = plt.figure().gca()
        plt.plot(x_axis, y_axis, 'ro-')
        plt.plot([blue_points[0].x, blue_points[1].x], [blue_points[0].y, blue_points[1].y])
        # plt.draw()
        # plt.show(block=False)

        # I would like for the figure window to open.  And every time we
        # find a convex quadrilateral, we clear the figure and draw the
        # new quadrilateral.  But alas, I have to settle with this
        # blocking call.
        plt.show()

    def test_convexity(self):
        a = self.points[0]
        b = self.points[1]
        c = self.points[2]
        d = self.points[3]
        total_angles = 0

        largest_angle = 0
        largest_angle_points = []
        for tup in [(a, b, c), (b, c, d), (c, d, a), (d, a, b)]:
            angle = tup[1].get_angle(tup[0], tup[2])
            total_angles += angle

            if angle > largest_angle:
                largest_angle_points = [tup[0], tup[2]]
                largest_angle = angle

        if abs((total_angles - 360.0)) > 0.001:
            print("{}: 360 - {:9f} = {}".format(self.to_string(), total_angles, 360-total_angles))
            print("Biggest angle ({}) endpoints: {} & {}"
                  .format(largest_angle, largest_angle_points[0], largest_angle_points[1]))
            # self.draw_points(largest_angle_points)
            self.convexity = True

        return largest_angle_points

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
    random_attempts = 100

    convexity_ctr = 0
    os = OuterSquare(square_size)
    plt.plot([-50, 50], [50, 50])
    plt.show(block=False)
    plt.clf()

    for i in range(1, random_attempts+1):
        os.reset()
        os.populate_points()
        # os.pprint()
        largest_angle_points = os.test_convexity()

        if os.convexity:
            convexity_ctr += 1
            os.draw_points(largest_angle_points, convexity_ctr)

    plt.show()

    print("\nOf the {} random samples, {} samples have a convex quadrilateral, or {}%."
          .format(random_attempts, convexity_ctr, 100*convexity_ctr/random_attempts))

if __name__ == "__main__":
    main()

    # fig = plt.figure()
    # ax = fig.gca()
    # fig.show()
    #
    # for i in range(10):
    #     ax.plot(i, i, 'ko')
    #     fig.canvas.draw()
    #     raw_input('pause : press any key ...')
    # fig.close()

    #
    # plt.plot([1,2.5,3,4])
    # plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    # plt.plot([1, 2, 3, 2, 1], [1, 2, 1, 0, 1])
    # plt.ylabel('asdf')
    # plt.show()