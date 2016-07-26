import os
import sys
import logging


def methods_outside_classes_are_not_weird():
    logging.info('Not weird at all.')


class Nutleton:

    class_int = 3
    class_str = "this is peanuts"

    def __init__(self):
        self.instance_str = "your own pecans"

    def get_instance_nuts(self):
        return self.instance_str


class VerbosePrint:
    """
    I need something that print line Java's System.out.println() but we can set verbosity.

    So this needs to
    """
    verbosity_level = 0

    @staticmethod
    def print0(*args):
        for arg in args:
            print arg,
        print

    @staticmethod
    def print1(*args):
        if VerbosePrint.verbosity_level >= 1:
            for arg in args:
                print arg,
            print

    @staticmethod
    def print2(*args):
        if VerbosePrint.verbosity_level >= 2:
            for arg in args:
                print arg,
            print

    @staticmethod
    def print3(*args):
        if VerbosePrint.verbosity_level >= 3:
            for arg in args:
                print arg,
            print




