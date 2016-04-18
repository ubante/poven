'''
This is from https://wiki.python.org/moin/SimplePrograms
'''

print("Hello, world!")

print
import os
import sys

print(os.path.dirname(sys.executable))

# name = raw_input("What is your name?\n")
print
name = "tired of inputting"
print "Hi, %s." % name

# list?
print
friends = ["john", "patrick", "gar", "mikey"]
for i, name in enumerate(friends):
    print "iteration {iteration} is {name}".format(iteration=i, name=name)

# tuple
print
parents, babies = (1, 1)
while babies < 100:
    print "This generation has {0} babies and {0} parents".format(babies, parents)
    parents, babies = (babies, parents + babies)

# functions
print


def greet(name):
    print "Hello", name


greet("Jack")
greet("Jill")
greet("Bob")

# regex
print
import re

for test_string in ["555-1212", "123-456", "123-45678", "123-4567 ", "ILL-EGAL"]:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        print test_string, 'is a valid US number'
    else:
        print test_string, 'rejected'

# dictionaries, generator expressions
print
prices = {"apple": 0.40, "banana": 0.50}
my_purchase = {
    'apple': 1,
    'banana': 6
}
grocery_bill = sum(prices[fruit] * my_purchase[fruit] for fruit in my_purchase)
print "I owe $%.2f" % grocery_bill

# command line args, "exception handling"
# adds up any integer arguments when this is invoked
try:
    total = sum(int(arg) for arg in sys.argv[1:])
    print "sum = ", total
except ValueError:
    print "Gimme integer arg, Hodor"

# opening files
# this will look for all .py files in the working directory and will output them concatenated
# with labels and indents
import glob

print
python_files = glob.glob("*.py")
for file_name in sorted(python_files):
    print "         --------" + file_name

    # with open(file_name) as f:
    #     for line in f:
    #         print "    " + line.rstrip()
    #
    # print

# time, conditionals
from time import localtime

print
activities = {8: "Sleeping",
              9: "Commuting",
              17: "Working",
              18: "Commuting",
              20: "Easting",
              22: "Resting",
              23: "Working more",
              # 24: "Raising",
              25: "Waiting for the future"
              }
time_now = localtime()
hour = time_now.tm_hour

print "The hour is now %d" % hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print activities[activity_time]
        break
else:
    print "Unknown, AFK or sleeping"

# triple quotes, while loop
# print
REFRAIN = '''
%d bottles of beer on the wall,
%d bottles of beer
take one down, pass it around,
%d bottles of beer on the wall!'''
bottles_of_beer = 5
while bottles_of_beer > 1:
    print REFRAIN % (bottles_of_beer, bottles_of_beer, bottles_of_beer - 1)
    bottles_of_beer -= 1

# classes
print


class BankAccount(object):
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def overdrawn(self):
        return self.balance < 0


my_account = BankAccount(15)
my_account.withdraw(5)
print "Balance is $%s" % my_account.balance

# unittest
print
print "unit test:"
import unittest


def median(pool):
    copy = sorted(pool)
    size = len(copy)
    if size % 2 == 1:
        return copy[(size - 1) / 2]
    else:
        return (copy[size / 2 - 1] + copy[size / 2]) / 2


class TestMedian(unittest.TestCase):
    def testMedian(self):
        self.failUnlessEqual(median([2, 9, 9, 7, 9, 2, 4, 5, 8]), 7)


# the below will cause program to exit
# if __name__ == "__main__":
#     unittest.main()

# doctest
print
print "doctest:"


def median(pool):
    """
    Statistical median to demonstrate doctest.
    >>> median([2, 9, 9, 7, 9, 2, 4, 5, 8])
    7
    """
    copy = sorted(pool)
    size = len(copy)
    if size % 2 == 1:
        return copy[(size - 1) / 2]
    else:
        return (copy[size / 2 - 1] + copy[size / 2]) / 2


if __name__ == "__main__":
    import doctest

    print "why doesn't this work??"
    doctest.testmod()

# itertools
# will respect paragraphs but not other newlines
print
from itertools import groupby

lines = '''
This is
the
first
paragraph.

This is the second.
'''.splitlines()

for has_chars, frags in groupby(lines, bool):
    if has_chars:
        print ' '.join(frags)

# tuple unpacking
print
import csv

writer = csv.writer(open("stocks.csv", "wb", buffering=0))
writer.writerows([
    ('GOOG', 'Google, Inc.', 505.24, 0.47, 0.09),
    ('YHOO', 'Yahoo! Inc.', 27.38, 0.33, 1.22),
    ('CNET', 'CNET Networks, Inc.', 8.62, -0.13, -1.49)
])

stocks = csv.reader(open("stocks.csv", "rb"))
status_labels = {-1: "down",
                 0: "changed",
                 1: "up"}
for ticker, name, price, change, pct in stocks:
    status = status_labels[cmp(float(change), 0.0)]
    print "%s is %s (%s%%)" % (name, status, pct)

# 8-queens recursion problem
print
BOARD_SIZE = 8


def under_attack(col, queens):
    left = right = col
    for r, c in reversed(queens):
        left, right = left-1, right+1

        if c in (left, col, right):
            return True
    return False

def solve(n):
    if n == 0:
        return [[]]

    smaller_solutions = solve(n-1)

    return [solution+[(n, i+1)]
        for i in xrange(BOARD_SIZE)
            for solution in smaller_solutions
                if not under_attack(i+1, solution)]

for answer in solve(BOARD_SIZE):
                    print answer





































