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
    start_time = time.time()
    num_of_tournaments = 1  # just a random number but 50 seems significant
    # num_of_tournaments = 1000  # just a random number but 50 seems significant
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
        # time.sleep(1)

        winner = single_tournament()
        bracelets[winner.name] += 1

        print("...........................................................")
        print("...........................................................")
        print("Bracelets:")
        for player in bracelets:
            print("{:2} {}".format(bracelets[player], player))
        # print(bracelets)

    stop_time = time.time()
    elapsed_time = stop_time - start_time
    print("\n{:4d} tournaments took {:0.4f} seconds or {:0.4f}/tournament."
          .format(num_of_tournaments, elapsed_time, elapsed_time/num_of_tournaments))
    print("Start time was {}".format(start_time))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN,
    # logging.basicConfig(level=logging.INFO,
    # logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')

    main()

"""
...........................................................
Bracelets:
173 Dale
78 Pete
218 Quin
53 Bert
238 Trey
191 Adam
49 Cail

1000 tournaments took 1260.1020 seconds or 1.2601/tournament.

...........................................................
Current bracelets:
 8 Dale
 2 Bert
13 Quin
 7 Trey
16 Adam
 1 Pete
 3 Cail

50 tournaments took 62.5640001297 seconds or 1.25128000259/tournament.
...........................................................
Current bracelets:
 3 Dale
 3 Bert
18 Quin
 9 Trey
10 Adam
 5 Pete
 2 Cail

50 tournaments took 63.5380001068 seconds or 1.27076000214/tournament.
...........................................................
Current bracelets:
 7 Dale
 6 Pete
 2 Cail
 5 Bert
13 Trey
 8 Adam
 9 Quin
...........................................................
Current bracelets:
 9 Pete
 7 Dale
 4 Quin
 7 Bert
 7 Trey
13 Adam
 3 Cail

  50 tournaments took 54.8770 seconds or 1.0975/tournament.
...........................................................
Current bracelets:
 9 Dale
 6 Pete
15 Quin
 3 Bert
 6 Trey
 8 Adam
 3 Cail

  50 tournaments took 45.5020 seconds or 0.9100/tournament.
...........................................................
Current bracelets:
 5 Pete
 4 Bert
 2 Cail
10 Dale
10 Trey
 9 Adam
10 Quin

  50 tournaments took 65.3540 seconds or 1.3071/tournament.
...........................................................
Current bracelets:
40 Pete
95 Dale
25 Cail
21 Bert
110 Trey
100 Adam
109 Quin

 500 tournaments took 479.0790 seconds or 0.9582/tournament.
...........................................................
Current bracelets:
79 Dale
35 Pete
116 Quin
43 Bert
103 Trey
97 Adam
27 Cail

 500 tournaments took 500.2560 seconds or 1.0005/tournament.
...........................................................
Current bracelets:
42 Pete
93 Dale
26 Cail
32 Bert
106 Trey
83 Adam
118 Quin

 500 tournaments took 638.1550 seconds or 1.2763/tournament.
...........................................................
Current bracelets:
0 Fifi
42 Pete
93 Dale
26 Cail
32 Bert
106 Trey
83 Adam
118 Quin

 500 tournaments took 638.1550 seconds or 1.2763/tournament.


"""