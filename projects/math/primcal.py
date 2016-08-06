"""
From http://www.murderousmaths.co.uk/games/primcal.htm
"""

def prime_number_trick():
    # The first 25 primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
              83, 89, 97]

    print "The columns are (prime, squared, plus 17, modulo 12)"
    for prime in primes:
        if prime < 5:
            continue # these don't count

        sq = prime * prime
        plus = sq + 17
        mod = plus % 12

        print "%5d %5d %5d %3d" % (prime, sq, plus, mod)

    # p mod 6 is 1 or 5 when p is not 2 or 3.
    print "The magic is the remainder is always 6.  Wot?"

prime_number_trick()

