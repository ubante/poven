#!/usr/bin/env python

"""
This will do that thing to those things.
"""

from __future__ import print_function

import argparse
import json
import logging
import sys


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
    parser.add_argument("-j", "--json-file",
                        help="This is the important value that we really need.")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    args.json_file = "sample_menu.json"

    if not args.json_file:
        logging.fatal("Missing important thing.\n")
        parser.print_usage()
        parser.exit()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    # Read the json file.
    with open(args.json_file) as json_data:
        j = json.load(json_data)
        json_data.close()

    print(j["menu"]["popup"]["menuitem"])

    # http://www.softqe.com/read-json-file-using-python/
    for value in j["menu"]["popup"]["menuitem"]:
        print("Value -> '{}'".format(value))

        for k in value.keys():
            print("      '{}' -> '{}'"
                  # .format(k, k))
                  .format(k, value[k]))

if __name__ == "__main__":
    main()
