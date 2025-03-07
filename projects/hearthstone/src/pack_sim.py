#!/usr/bin/env python3

"""
This will simulate opening packs until I get all commons, rares, and epics.
"""
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


def run_sim():
    # me = Player()
    pass

    
def main():
    description = '''
This will simulate opening packs until I get all commons, rares, and epics.
'''
    epilog = '''
Examples:
    ./pack_sim.py
'''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    # In this, DEBUG is mostly for entering and exiting methods/functions.  Use the other debug
    # flags for more verbose output.
    args.verbose = 1
    set_logger(args.verbose)
    logging.debug("Here we go.")

    run_sim()


if __name__ == "__main__":
    main()