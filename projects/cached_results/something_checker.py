import time
from somethinglib import Numbre


"""
Check something
"""


def main():
    print "Here we go."

    num = Numbre()
    prime_count = num.get_count()
    print "The number of primes in the range of 2 to 100 is", prime_count

    sleepy_time = 2
    print "\nSleeping for {} seconds".format(sleepy_time)
    time.sleep(sleepy_time)
    num.cache.stat()
    prime_count = num.get_count()
    print "The number of primes in the range of 2 to 100 is", prime_count

    print "\nSleeping for {} seconds".format(sleepy_time)
    time.sleep(sleepy_time)
    num.cache.stat()
    prime_count = num.get_count()
    print "The number of primes in the range of 2 to 100 is", prime_count

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