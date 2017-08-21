#!/usr/bin/env python

"""
Check if a CSV file is rectangular.
"""

from __future__ import print_function

import argparse
import logging
import sys

from collections import defaultdict


def set_logger(verbose_level):
    """
    Initialize the logger.  The verbose_level should be in [0, 1, 2].
    This won't return anything but will reconfigure the root logger.
    
    :param verbose_level:
    :return:
    """
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
    parser.add_argument("-f", "--csvfilepath", help="CSV file path.")
    parser.add_argument("-s", "--simple", help="Just print the count as they happen.",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    if not args.csvfilepath:
        logging.fatal("Missing important thing.\n")
        parser.print_usage()
        parser.exit()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    # https://stackoverflow.com/questions/31126491/python-to-count-commas-in-a-text-file
    total = defaultdict(int)
    line_ctr = 0
    with open(args.csvfilepath) as f:
        for line in f:
            comma_count = line.count(",")
            line_ctr += 1
            total[comma_count] += 1

            if args.simple:
                print(comma_count)
                continue

    print("There are {} lines in the file.".format(line_ctr))

    most_frequent_count = None
    for k in total:

        if most_frequent_count is None:
            most_frequent_count = k
        else:
            if total[most_frequent_count] < total[k]:
                most_frequent_count = k

        print("{} occurences of {}".format(total[k], k))

    print("\nThe most frequent count is: {}".format(most_frequent_count))

    if args.simple:
        sys.exit()

    # Print the non-conforming lines.
    # I could have stored this in the total dictionary but re-reading
    # gets around memory limits.
    print("Below are the non-conforming lines:")
    with open(args.csvfilepath) as f:
        for line in f:
            comma_count = line.count(",")

            if comma_count != most_frequent_count:
                print("{}: {}".format(comma_count, line), end="")


if __name__ == "__main__":
    main()
