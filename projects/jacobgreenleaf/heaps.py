"""
I can't find a heap.  Maybe it's some type of queue somewhere.
"""
from __future__ import print_function

import math

from heapq import heappush, heappop


class Heap(object):

    def __init__(self):
        self.elements = []
        self.counter = 0

    def add(self, number):
        heappush(self.elements, number)
        self.counter += 1

    def display(self, negation=False):
        if self.counter == 0:
            print("Heap is empty.")
            return

        print("Heap has {} elements:".format(self.counter))

        # If there's just one element, we need to handle this separately
        # because the following loop would be too ungainly if we didn't.
        if self.counter == 1:
            value = self.elements[0]
            if negation:
                value = -value
            print("{}{}\n".format(" "*5, value))
            return

        num_layers = int(math.ceil(math.log(self.counter, 2)))
        for layer in range(1, num_layers+1):
            layer_start = 2**(layer-1)-1
            layer_end = 2**layer-1

            if layer == num_layers:
                layer_end = self.counter
            for index in range(layer_start, layer_end):
                # The leading spaces should be half the size.
                print("{}".format(" " * (2 ** (num_layers-layer+1))), end="")

                value = self.elements[index]
                if negation:
                    value = -value
                print("{}{}".format(value, " " * (2 ** (num_layers-layer+1))), end="")
                # print("{}{}".format(self.elements[index], " " * (2 ** (num_layers-layer+1))),
                #       end="")
            print("")
        print("")

    def get_root_value(self):
        return self.elements[0]

    def reset(self):
        self.__init__()


class MinHeap(Heap):
    def remove_smallest(self):
        self.counter -= 1
        return heappop(self.elements)


class MaxHeap(Heap):
    """
    This has the largest node at the root.

    We do some kludgey stuff.
    """
    def add(self, number):
        heappush(self.elements, -number)
        self.counter += 1

    def remove_largest(self):
        self.counter -= 1
        smallest = heappop(self.elements)

        return -smallest

    def display(self):
        super(MaxHeap, self).display(negation=True)

    def get_root_value(self):
        return -self.elements[0]


def populate_heap(heap):
    data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    for item in data:
        heap.add(item)


def demo():
    # heap = MaxHeap()
    heap = MinHeap()
    data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    for item in data:
        heap.add(item)
    heap.display()

    heap.add(12)
    heap.display()

    heap.add(18)
    heap.display()

    heap.add(10)
    heap.display()

    smallest = heap.remove_smallest()
    heap.display()

    heap.add(28)
    heap.display()

    # heap.reset()
    heap.add(1)
    heap.display()

    heap.add(-3)
    heap.display()

    heap.add(-18)
    heap.display()

    heap.add(13)
    heap.display()


if __name__ == "__main__":
    demo()
