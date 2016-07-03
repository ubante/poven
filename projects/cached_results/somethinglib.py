import sys
import time


class Cache:
    def __init__(self, ttl=10):
        self.list = []
        self.insertion_time = None
        self.expiration_time = None
        self.ttl = ttl

    def is_expired(self):
        if not self.expiration_time:
            return True

        now = time.time()
        if self.expiration_time < now:
            # print "cache expired"
            # print "now: {}, expiration: {}".format(now, self.expiration_time)
            return True

        return False

    def set_list(self, a_list):
        print "Setting list in cache"
        self.list = a_list
        now = time.time()
        self.insertion_time = now
        self.expiration_time = now + self.ttl
        # print "Setting expiration time to", self.expiration_time

    def stat(self):
        now = time.time()
        print "CACHE now:{} expiration:{} state:{}".format(now,
                                                           self.expiration_time,
                                                           self.is_expired())


class Numbre:
    def __init__(self, start=2, end=100):
        self.starting = start
        self.ending = end
        self.primes = []
        self.cache = Cache(ttl=3)
        self.find_primes()

    def find_primes(self):
        self.primes = []
        for dividend in range(self.starting, self.ending + 1):

            is_prime = True
            for divisor in range(2, dividend):
                if (dividend % divisor) == 0:
                    # print "dividend: {}, divisor: {}".format(dividend, divisor)
                    is_prime = False
                    break

            if is_prime:
                self.primes.append(dividend)

        self.cache.set_list(self.primes)

    def get_count(self):
        if self.cache.is_expired():
            print "the cache is expired"
            # sys.exit()
            self.find_primes()

        return len(self.primes)
