#!/usr/bin/env python3

"""
This will do that thing to those things.
"""

from __future__ import print_function

import argparse
import logging
import sys


def set_logger(verbose_level):
    # Let there be debug.

    verbose_level = 0 if not verbose_level else verbose_level

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
    description = '''
The coupon collector is supposed to be O(n ln(n)) but I have a doubt.
This script will check.
'''
    epilog = '''
Examples:
    ./servicecatalogDAO.py --path ../../data/service_catalog.yaml --gsheet -vv
    ./servicecatalogDAO.py --path ../../data/service_catalog.yaml --list
'''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
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
