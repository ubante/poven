import sys
import time


class Cache:
    def __init__(self, ttl=10):
        self.list = []
        self.single_value = None
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

    def reset_expiration_time(self):
        now = time.time()
        self.insertion_time = now
        self.expiration_time = now + self.ttl

    def set_list(self, a_list):
        self.list = a_list
        self.reset_expiration_time()
        # now = time.time()
        # self.insertion_time = now
        # self.expiration_time = now + self.ttl

    def set_single_value(self, value):
        self.single_value = value
        self.reset_expiration_time()

    def __str__(self):
        return "CACHE now:{} expiration:{} is_expired:{}".format(time.time(),
                                                                 self.expiration_time,
                                                                 self.is_expired())


class Flock:
    flock_travel_distance = None
    cache = Cache

    def __init__(self):
        print "Making a Flock object - should not happen"
        self.cache = Cache()

    @staticmethod
    def compute_flock_travel_distance():
        """This represents something we don't want to compute often."""
        if not Flock.flock_travel_distance:
            # Flock.flock_travel_distance = 22
            # Flock.flock_travel_distance = time.time() - 1467683200
            print "==== computing flock travel distance"
            Flock.flock_travel_distance = "{0:.2f}".format(time.time() - 1467683200)
            # Flock.cache.set_single_value(Flock.flock_travel_distance)

            c = Cache
            # c.set_single_value(8)
            c.set_single_value(Flock.flock_travel_distance)
            Flock.cache = c

        return Flock.flock_travel_distance


class Bird:
    cache = Cache()

    def __init__(self, name):
        self.travel_distance = None
        self.name = name

    def __str__(self):
        if self.travel_distance:
            return "{} has travelled {} kilomiles.".format(self.name, self.travel_distance)
        return self.name + " is a bird."

    # @staticmethod
    def compute_travel_distance(self):
        """This represents something we don't want to compute often."""
        distance = "{0:.2f}".format(time.time() - 1467683200)
        Bird.cache.set_single_value(distance)

    def get_flock_travel_distance(self):
        self.travel_distance = Flock.compute_flock_travel_distance()


class Numbre:
    def __init__(self, start=2, end=100):
        self.starting = start
        self.ending = end
        self.primes = []
        self.cache = Cache(ttl=3)
        print "Initializing the list in cache."
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
            print "The cache is expired.  Updating list in cache"
            self.find_primes()

        return len(self.primes)


class WhaleGangMember(object):
    def __init__(self):
        self.location = self.use_gps()
        self.name = None

    def __str__(self):
        return "This whale is named {} and is in {}.".format(self.name, self.location)

    def use_gps(self):
        """Assume that this is an expensive operation"""
        return "SF"


class Whale(WhaleGangMember):
    def __init__(self, name):
        super(Whale, self).__init__()
        self.name = name





