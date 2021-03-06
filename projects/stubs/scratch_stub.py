#!/usr/bin/env python

"""
This will do that thing to those things.
"""

from __future__ import print_function

import argparse
import logging
import sys


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

    if not args.important:
        logging.fatal("Missing important thing.\n")
        parser.print_usage()
        parser.exit()

    set_logger(args.verbose)
    logging.debug("Here we go.")

if __name__ == "__main__":
    main()
