"""
This will run many tournaments to see which Player is the most
successful.
"""

import logging
import sys
import time

from collections import defaultdict

from runner import main as single_tournament


def main():
    num_of_tournaments = 50  # just a random number but 50 seems significant
    bracelets = defaultdict(int)
    for i in range(1, num_of_tournaments+1):
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("...........................................................")
        print("Running tournament #{}/{}:".format(i, num_of_tournaments))
        print("...........................................................")
        print("...........................................................")
        time.sleep(1)

        winner = single_tournament()
        bracelets[winner.name] += 1

        print("...........................................................")
        print("...........................................................")
        print("Current bracelets:")
        for player in bracelets:
            print("{:2} {}".format(bracelets[player], player))
        # print(bracelets)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')

    main()

"""
2018/07/17:
Current bracelets:
 3 Pete
 7 Bert
14 Cail
17 Adam
 9 Dale


"""