#!/usr/bin/env python

"""
https://en.wikipedia.org/wiki/Coupon_collector%27s_problem

Given an N sided die, how many rolls to roll each side?

50%, 99.5% ?
"""

from __future__ import print_function

import argparse
import csv
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


def dict_to_list(rollcount):
    newlist = []
    # print(rollcount)
    # print(rollcount[1])
    for i in range(0, len(rollcount)):
        # print("loop {}".format(i))
        newlist.append(rollcount[i+1])

    return newlist


def main():
    description = '''
The coupon collector problem is supposed to be O(n ln(n)) but I have a doubt.

This extends the problem by requiring each possible random value to happen F times.
When f=1, that is the classic coupon collector problem.
'''
    epilog = '''
Examples:
  ./fillmode.py -n 42 -i 20000 -p99 -q -f1
  ./fillmode.py -n 6 -i 20 -p90 -f1
'''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", help="Number of sides of the die or number of distinct coupons", type=int)
    parser.add_argument("-f", help="How many hits do you want for each possible value", type=int)
    parser.add_argument("-p", "--percent", help="The percent we want", type=float, default=80)
    parser.add_argument("-i", "--iteration", help="How precise do you want to be?", type=int, default=100)
    parser.add_argument("-c", "--csv", help="Write the rolls out to a csv file")
    parser.add_argument("-q", "--quiet", help="Suppress some output", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print info/debug", action="count")
    args = parser.parse_args()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    if not args.n:
        logging.fatal("Missing n.\n")
        parser.print_usage()
        parser.exit()

    if not args.f:
        logging.fatal("Missing f.\n")
        parser.print_usage()
        parser.exit()

    logging.info("N: {}, I: {}, P: {}".format(args.n, args.iteration, args.percent))

    tally = defaultdict(int)
    bestroll = sys.maxint
    worstroll = 0
    csvdata = []
    for i in range(1, args.iteration+1):
        if not args.quiet:
            print("-- Iteration {}/{} --".format(i, args.iteration))

        found = defaultdict(int)
        foundcount = 0
        rollcounter = 0
        while foundcount < args.n:
            rollcounter += 1
            roll = randint(1, args.n)
            logging.debug("rolled a {}".format(roll))
            if found[roll] > args.f:
                continue

            found[roll] += 1
            if found[roll] == args.f:
                foundcount += 1

        if not args.quiet:
            print("It took {} rolls to get all {} sides {} times.".format(rollcounter, args.n, args.f))
        logging.info(found)
        csvdata.append(dict_to_list(found))
        # csvdata.append([1,3,5,4])
        tally[rollcounter] += 1
        if rollcounter > worstroll:
            worstroll = rollcounter
        if rollcounter < bestroll:
            bestroll = rollcounter

    if args.csv:
        with open(args.csv, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csvdata)



    sys.exit(3)

    if not args.quiet:
        print("Tally:")
    mediansum = 0
    medianroll = 0
    percentsum = 0
    percentroll = 0
    for i in range(0, worstroll+1):
        if tally[i] == 0:
            continue
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

    print("To hit each possibility {} times, the best rollset was {}, the median was {}, the worst was {}"
          .format(args.f, bestroll, medianroll, worstroll))
    # print("n log(n) = {}".format(args.n * math.log(args.n)))
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

(poven) 2141-laptop:coupon_collector$ time ./runner.py -n 42 -i 100000 -p99.99 -q
The best rollset was 72, the median rollset was 173, the worst rollset was 635
n log(n) = 156.982123968
99.99 percent of the 100000 rollsets were at or below 518

real	0m38.594s
user	0m38.472s
sys	0m0.071s

(poven) 2147-laptop:coupon_collector$ ./runner.py -n 6 -i 20 -p90
-- Iteration 1/20 --
It took 9 rolls to get all 6 sides.
-- Iteration 2/20 --
It took 13 rolls to get all 6 sides.
-- Iteration 3/20 --
It took 13 rolls to get all 6 sides.
-- Iteration 4/20 --
It took 16 rolls to get all 6 sides.
-- Iteration 5/20 --
It took 12 rolls to get all 6 sides.
-- Iteration 6/20 --
It took 10 rolls to get all 6 sides.
-- Iteration 7/20 --
It took 12 rolls to get all 6 sides.
-- Iteration 8/20 --
It took 15 rolls to get all 6 sides.
-- Iteration 9/20 --
It took 16 rolls to get all 6 sides.
-- Iteration 10/20 --
It took 17 rolls to get all 6 sides.
-- Iteration 11/20 --
It took 13 rolls to get all 6 sides.
-- Iteration 12/20 --
It took 8 rolls to get all 6 sides.
-- Iteration 13/20 --
It took 12 rolls to get all 6 sides.
-- Iteration 14/20 --
It took 18 rolls to get all 6 sides.
-- Iteration 15/20 --
It took 12 rolls to get all 6 sides.
-- Iteration 16/20 --
It took 12 rolls to get all 6 sides.
-- Iteration 17/20 --
It took 20 rolls to get all 6 sides.
-- Iteration 18/20 --
It took 27 rolls to get all 6 sides.
-- Iteration 19/20 --
It took 13 rolls to get all 6 sides.
-- Iteration 20/20 --
It took 30 rolls to get all 6 sides.
Tally:
0: 0
1: 0
2: 0
3: 0
4: 0
5: 0
6: 0
7: 0
8: 1
9: 1
10: 1
11: 0
12: 5
13: 4
14: 0
15: 1
16: 2
17: 1
18: 1
19: 0
20: 1
21: 0
22: 0
23: 0
24: 0
25: 0
26: 0
27: 1
28: 0
29: 0
30: 1
The best rollset was 8, the median rollset was 13, the worst rollset was 30
n log(n) = 10.7505568154
90.0 percent of the 20 rollsets were at or below 27

"""