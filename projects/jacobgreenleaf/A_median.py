"""
https://medium.com/@jacobgreenleaf/why-data-structures-are-irrelevant-to-software-engineering-interviews-and-what-can-be-done-about-it-bd9b7a9a0bb8#.3wa0wxt6i

Numbers are randomly generated and stored into an (expanding) array. How
would you keep track of the median?
"""

from __future__ import print_function

import random
import numpy

from heapq import heappush, heappop

def get_random_number():
    return random.random()*2000-1000


def find_median(a_list):
    return numpy.median(a_list)


def get_random_list(list_length):
    # list_length = 10  # yeah, I know
    return [get_random_number() for i in range(0,list_length)]


def main():
    length = 10
    array = get_random_list(length)
    median = find_median(array)
    print("The list of {} numbers:".format(length))
    print(*array, sep='\n')
    print("\nThe median is {}\n\n".format(median))

    for i in range(0, 100):
        random_number = get_random_number()
        array.append(random_number)

        # What to do about median?

        print("After adding {} to the list, the new median is {}"
              .format(random_number, median))


def get_random_int(min, max):
    return random.randint(min, max)


class Median(object):
    def __init__(self):
        self.median = None
        self.element_counter = 0


    def print_median(self):
        if self.median:
            print("The median: {}".format(self.median))
        else:
            print("We have no data yet.")

    def add(self, input_int):
        self.element_counter += 1


def try2():
    median = Median()

    for i in range(1, 11):
        print("{:3}: ".format(i), end="")
        median.add(get_random_int(0,50))
        median.print_median()


def so_sample():
    """
    From http://stackoverflow.com/questions/12749622/creating-a-heap-in-python
    :return:
    """
    heap = []
    data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    for item in data:
        heappush(heap, item)
    print("Heap:", heap)

    ordered = []
    while heap:
        ordered.append(heappop(heap))

    print("Ordered:", ordered)

if __name__ == "__main__":
    # main()
    try2()
    print("")
    so_sample()