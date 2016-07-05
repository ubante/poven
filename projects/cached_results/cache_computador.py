import time
import sys
from somethinglib import Numbre, Whale, Bird
"""
Check something
"""


def main():
    # This shows how "b" learns its travelled distance
    b = Bird("b")
    print b.__str__()
    b.compute_travel_distance()
    print b.__str__()

    # This shows how "k" picks up b's cache
    print
    sleepy_time = 1
    time.sleep(sleepy_time)
    k = Bird("k")
    print k.__str__()
    k.compute_travel_distance()

    # This should have mostly cache hits
    for interval in range(0, 13):
        time.sleep(sleepy_time)
        k.compute_travel_distance()
        print k.__str__()

    # Now b picks up on the shared cache
    print
    b.compute_travel_distance()
    print b.__str__()
    sys.exit()


if __name__ == "__main__":
    main()

"""
b is a bird.
b has travelled 1143.86 kilomiles.

k is a bird.
k has travelled 1143.86 kilomiles.
k has travelled 1143.86 kilomiles.
k has travelled 1143.86 kilomiles.
k has travelled 1148.86 kilomiles.
k has travelled 1148.86 kilomiles.
k has travelled 1148.86 kilomiles.
k has travelled 1148.86 kilomiles.
k has travelled 1148.86 kilomiles.
k has travelled 1153.86 kilomiles.
k has travelled 1153.86 kilomiles.
k has travelled 1153.86 kilomiles.
k has travelled 1153.86 kilomiles.
k has travelled 1153.86 kilomiles.

b has travelled 1153.86 kilomiles.
"""