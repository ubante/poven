#!/usr/bin/env python

"""
https://en.wikipedia.org/wiki/Coupon_collector%27s_problem

Given an N sided die, how many rolls to roll each side?

50%, 99.5% ?
"""

from __future__ import print_function

import argparse
import logging
import math
import sys

from collections import defaultdict
from random import randint


def set_logger(verbose_level, logfilename=None):
    """
    Initialize the logger.  The verbose_level should be in [0, 1, 2].
    This won't return anything but will reconfigure the root logger.

    :param logfilename:
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
                        filename=logfilename,
                        format='%(levelname)s - %(message)s')


def main():
    description = '''
The coupon collector problem is supposed to be O(n ln(n)) but I have a doubt.
'''
    epilog = '''
Examples:
  ./decomm.py tilden-services7.sfp.sfdc.wavemarket.com --old-hv hv8.sfp.sfdc.wavemarket.com
  ./decomm.py sms4.afm.sfdc.wavemarket.com  # This will do that thing.
  ./decomm.py vci-scale3-history-api12.evdc.wavemarket.com
'''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", help="Number of sides of the die or number of distinct coupons", type=int)
    parser.add_argument("-p", "--percent", help="The percent we want", type=int, default=80)
    parser.add_argument("-i", "--iteration", help="How precise do you want to be?", type=int, default=100)
    parser.add_argument("-q", "--quiet", help="Suppress some output", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print info/debug", action="count")
    args = parser.parse_args()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    if not args.n:
        logging.fatal("Missing n.\n")
        parser.print_usage()
        parser.exit()

    logging.info("N: {}, I: {}, P: {}".format(args.n, args.iteration, args.percent))

    tally = defaultdict(int)
    # tallymax = 0
    bestroll = sys.maxint
    worstroll = 0
    for i in range(1, args.iteration+1):
        if not args.quiet:
            print("-- Iteration {}/{} --".format(i, args.iteration))

        found = defaultdict(bool)
        foundcount = 0
        rollcounter = 0
        while foundcount < args.n:
            rollcounter += 1
            roll = randint(1, args.n)
            logging.debug("rolled a {}".format(roll))
            if found[roll]:
                continue

            found[roll] = True
            foundcount += 1

        if not args.quiet:
            print("It took {} rolls to get all {} sides.".format(rollcounter, args.n))
        tally[rollcounter] += 1
        if rollcounter > worstroll:
            worstroll = rollcounter
        if rollcounter < bestroll:
            bestroll = rollcounter

    if not args.quiet:
        print("Tally:")
    mediansum = 0
    medianroll = 0
    percentsum = 0
    percentroll = 0
    for i in range(0, worstroll+1):
        if not args.quiet:
            print("{}: {}".format(i, tally[i]))
        mediansum += tally[i]
        if medianroll == 0:
            if mediansum > args.iteration/2:
                medianroll = i
        percentsum += tally[i]
        if percentroll == 0:
            if percentsum > args.iteration * args.percent / 100:
            # if percentsum > args.iteration / 2:
                percentroll = i

    print("The best rollset was {}, the median rollset was {}, the worst rollset was {}"
          .format(bestroll, medianroll, worstroll))
    # print("The median roll was {}".format(medianroll))
    print("n log(n) = {}".format(args.n * math.log(args.n)))
    print("{} percent of the {} rollsets were at or below {}".format(args.percent, args.iteration, percentroll))

    logging.info("{} {} {} {}".format(args.iteration, args.percent, args.iteration*100,
                                     args.iteration*100/args.percent))


if __name__ == "__main__":
    main()

"""
(poven) 1953-laptop:coupon_collector$ ./runner.py -n 42 -i 20000 -p99 -q
The best rollset was 73, the median rollset was 172, the worst rollset was 585
n log(n) = 156.982123968
99 percent of the 20000 rollsets were at or below 344
"""