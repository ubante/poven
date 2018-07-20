"""
This will run many tournaments to see which Player is the most
successful.
"""

from datetime import datetime

import logging
import sys
import time

from collections import defaultdict

from runner import main as single_tournament


def main():
    start_time = time.time()
    # num_of_tournaments = 2
    num_of_tournaments = 1000  # just a random number but 1000 seems significant
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
    print("End time is {}".format(str(datetime.now())))


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
160 Dale
55 Pete
42 Cail
51 Bert
201 Trey
120 Sven
164 Adam
207 Quin

1000 tournaments took 1156.4080 seconds or 1.1564/tournament.
End time is 2018-07-19 00:47:00.490000

...........................................................
Bracelets:
167 Dale
30 Bert
178 Quin
201 Trey
151 Sven
169 Adam
76 Pete
28 Cail

1000 tournaments took 1147.7600 seconds or 1.1478/tournament.
End time is 2018-07-18 23:17:29.408000

...........................................................
Bracelets:
152 Dale
91 Pete
39 Cail
44 Bert
196 Trey
135 Sven
159 Adam
184 Quin

1000 tournaments took 1134.0650 seconds or 1.1341/tournament.
End time is 2018-07-18 22:05:36.357000

...........................................................
Bracelets:
92 Pete
58 Bert
230 Quin
152 Dale
233 Trey
186 Adam
49 Cail

1000 tournaments took 1179.3810 seconds or 1.1794/tournament.
End time is 2018-07-18 21:44:54.624000
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