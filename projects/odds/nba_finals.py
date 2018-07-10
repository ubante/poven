from __future__ import print_function

import random

from collections import defaultdict

iterations = 999
odds_game_for_t1 = 0.90
win_count = defaultdict(int)

for i in range(1, iterations+1):

    print("Iteration #{0:2}: ".format(i), end="")
    t1_wins = 0
    t2_wins = 0
    scores = ""

    game_number = 1
    while t1_wins < 4 and t2_wins < 4:
        # if random.randomdom < 0.5
        # if random.randint(0,9) < 5:
        # if random.randint(0, 1) < 0.5:
        # score = random.randint(0, 1)
        score = random.uniform(0, 1)
        scores = "{} {}".format(scores, score)
        if score < odds_game_for_t1:
            # print("1 ", end="")
            # print("Team 1 wins game #{}".format(game_number))
            t1_wins += 1
        else:
            # print("2 ", end="")
            # print("Team 2 wins game #{}".format(game_number))
            t2_wins += 1
        game_number += 1
    # print("")

    if t1_wins == 4:
        win_count["t1"] += 1
        print("Team 1 wins the series {} to {} ({}/{})  {}."
              .format(t1_wins, t2_wins, win_count["t1"], win_count["t2"], scores))
    if t2_wins == 4:
        win_count["t2"] += 1
        # print("Team 2 wins the series {} to {}.".format(t2_wins, t1_wins))
        print("Team 2 wins the series {} to {} ({}/{})  {}."
              .format(t2_wins, t1_wins, win_count["t1"], win_count["t2"], scores))

print("\n\nAfter {} iterations with Team 1 winning each game with the odds of {}, the final results are {}/{}:"
      .format(iterations, odds_game_for_t1, win_count["t1"], win_count["t2"]))
