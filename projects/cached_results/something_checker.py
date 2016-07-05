import time
import sys
from somethinglib import Numbre, Whale, Bird
"""
Check something
"""


def main():
    print "Here we go."

    b = Bird("b")
    print b.__str__()
    # b.get_flock_travel_distance()
    b.compute_travel_distance()
    print b.__str__()
    # b.get_flock_travel_distance()
    # b.compute_travel_distance()
    # print b.__str__()
    # b.stat_cache()

    print
    sleepy_time = 1
    time.sleep(sleepy_time)
    k = Bird("k")
    print k.__str__()
    k.compute_travel_distance()
    # k.stat_cache()

    for interval in range(0, 13):
        # k.get_flock_travel_distance()
        time.sleep(sleepy_time)
        k.compute_travel_distance()
        print k.__str__()
    # k.stat_cache()
    # b.stat_cache()
    print
    b.compute_travel_distance()
    print b.__str__()
    sys.exit()

    print "\n\nPRIME TIME\n"
    num = Numbre()
    # prime_count = num.get_count()
    # print "The number of primes in the range of 2 to 100 is", prime_count
    #
    # print "\nSleeping for {} seconds".format(sleepy_time)
    # time.sleep(sleepy_time)
    # num.cache.stat()
    # prime_count = num.get_count()
    # print "The number of primes in the range of 2 to 100 is", prime_count

    for interval in range(0, 7):
        prime_count = num.get_count()
        print "The number of primes in the range of 2 to 100 is", prime_count

        print "\nSleeping for {} seconds".format(sleepy_time)
        time.sleep(sleepy_time)
        # num.cache.stat()
        print num.cache
        # print num.cache.__str__()

    #
    # print "\nSleeping for {} seconds".format(sleepy_time)
    # time.sleep(sleepy_time)
    # num.cache.stat()
    # prime_count = num.get_count()
    # print "The number of primes in the range of 2 to 100 is", prime_count

    sys.exit()

    print "This above has the Cache object be a member of the Numbre object so each object will " \
          "have its own cache.  This makes sense if you reuse an object.  But if you don't....\n"

    aWhale = Whale("Alfred")
    bWhale = Whale("Barnie")
    whales = [aWhale, bWhale]
    for whale in whales:
        print whale.__str__()


if __name__ == "__main__":
    main()

"""
Here we go.
Setting list in cache
The number of primes in the range of 2 to 100 is 25

Sleeping for 2 seconds
CACHE now:1467509590.64 expiration:1467509591.64 state:False
The number of primes in the range of 2 to 100 is 25

Sleeping for 2 seconds
CACHE now:1467509592.64 expiration:1467509591.64 state:True
the cache is expired
Setting list in cache
The number of primes in the range of 2 to 100 is 25
"""