"""
https://medium.com/@jacobgreenleaf/why-data-structures-are-irrelevant-to-software-engineering-interviews-and-what-can-be-done-about-it-bd9b7a9a0bb8#.3wa0wxt6i

Numbers are randomly generated and stored into an (expanding) array. How
would you keep track of the median?
"""

from __future__ import print_function

import random

from heaps import (MinHeap, MaxHeap)


def get_random_int(min, max):
    return random.randint(min, max)


class Median(object):
    def __init__(self):
        self.median = None
        self.element_counter = 0

        # The root of a minHeap has the lowest value in that tree.  We
        # will use min_heap to represent the larger half of the data
        # stream.  The name seems misleading at first.  But it is easier
        # to use the heaps like this so the two roots are close to each
        # other.
        self.larger_half = MinHeap()
        self.smaller_half = MaxHeap()

    def get_median(self):
        if self.element_counter < 2:
            return None

        # If there are an odd number of elements, then one heap will
        # have more elements than the other.  Because of how we
        # rebalance the heaps in add(), the root of the larger heap
        # will be the median.
        if self.element_counter % 2 == 1:
            if self.larger_half.counter > self.smaller_half:
                median = self.larger_half.get_root_value()
            else:
                median = self.smaller_half.get_root_value()
            return float(median)

        # If there are an even number of elements, then the median
        # is the average of two numbers.  Again, since we rebalance
        # the trees, those two numbers are the two roots.
        else:
            return float(self.larger_half.get_root_value() + self.smaller_half.get_root_value()) / 2

    def initialize(self, input_int):
        """
        Just to break this out of add().
        :param input_int:
        :return:
        """
        # If this is the first input, then just put it in the heap for
        # the larger numbers.
        if self.element_counter == 1:
            self.larger_half.add(input_int)

            return

        # If the second input is smaller than the first input, easy.
        if input_int <= self.larger_half.get_root_value():
            self.smaller_half.add(input_int)
        else:
            # Otherwise, still easy.
            self.smaller_half.add(self.larger_half.get_root_value())
            self.larger_half.remove_smallest()
            self.larger_half.add(input_int)

        self.median = float(self.larger_half.get_root_value() + self.smaller_half.get_root_value()) / 2

    def rebalance(self):
        """
        The two heaps should be the same size, give or take 1.

        It is possible for a heap to be larger than the other heap by 2.
        This happens when the larger heap gets another element.  This
        function, in those cases, will take the root from the larger
        heap and add it to the smaller heap.  It is expected that the
        moved root will become the new root in its destination heap.
        :return:
        """
        if abs(self.larger_half.counter - self.smaller_half.counter) <= 1:
            return

        if self.larger_half.counter > self.smaller_half.counter:
            number_to_migrate = self.larger_half.remove_smallest()
            self.smaller_half.add(number_to_migrate)
        else:
            self.larger_half.add(self.smaller_half.remove_largest())

    def add(self, input_int):
        self.element_counter += 1
        if self.element_counter <= 2:
            self.initialize(input_int)
            return

        # Once we get past the first two inputs, we have to compare
        # this input with the roots of the two trees.
        if input_int < self.larger_half.get_root_value():
            # print("input is greater than min_heap")
            self.smaller_half.add(input_int)
        else:
            # print("input is lesser than min_heap")
            self.larger_half.add(input_int)

        self.rebalance()

    def display_heaps(self):
        print("Smaller values:")
        self.smaller_half.display()
        print("Larger values:")
        self.larger_half.display()


def main():
    median = Median()
    # random.seed("just_to_make_testing_easier")

    for i in range(1, 100):
        random_int = get_random_int(0, 100)
        # print("---- ({:2}) ".format(random_int), end="")
        median.add(random_int)
        # print("{:3}: Median is {:1} ----".format(i, median.get_median()))

        # This is for visualizing the heaps because dumping the
        # underlying list isn't useful.
        # median.display_heaps()

        # In case I want just the median for graphing purposes, comment
        # out the above prints.
        # print(median.get_median())

        print("{},{}".format(random_int, median.get_median()))

        #TODO: I see the median converge but would like to see how the mean converges.

if __name__ == "__main__":
    main()
