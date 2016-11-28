#!/usr/bin/env python

from __future__ import print_function

import sqlite3
import time

from random import randint


"""
Can you find the cube root of a number?
"""


class Scores(object):

    def __init__(self, score, e_time):
        self.score = score
        self.e_time = e_time
        self.name = "didnotplace"
        self.conn = sqlite3.connect("top10.db")
        self.cursor = self.conn.cursor()
        self.num_of_rows_that_matter = 10
        # self.position = self.num_of_rows_that_matter+1

        # Make the table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Scores(Score INT, Time REAL, Name TEXT)")

        # Find the position of the score
        self.position = self.find_position()

    def find_position(self):
        self.cursor.execute("SELECT Score, Time FROM Scores "
                            "ORDER By Score DESC, Time ASC "
                            "LIMIT {}".format(self.num_of_rows_that_matter))

        for position, (score, e_time) in enumerate(self.cursor.fetchall(), start=1):
            if self.score > score:
                return position
            elif (self.score == score) and (self.e_time < e_time):
                return position

        # If we get to this point, then the score did not crack the top
        # scores.
        return self.num_of_rows_that_matter+1

    def is_top_score(self):
        return self.position == 1

    def is_high_score(self):
        return self.position <= self.num_of_rows_that_matter

    def add_name(self, name):
        self.name = name

    def commit_score(self):
        self.cursor.execute("INSERT INTO Scores VALUES({}, {}, '{}')"
                            .format(self.score, self.e_time, self.name))

        # This is needed to commit the transaction.
        self.cursor.execute('PRAGMA schema_version')

    def display_high_scores(self):
        self.cursor.execute("SELECT * FROM Scores "
                            "ORDER BY Score DESC, Time ASC "
                            "LIMIT {}".format(self.num_of_rows_that_matter))
        rows = self.cursor.fetchall()

        print("\n  === HIGH SCORES ===")
        print("{:4}  {:5}  {:4}  {:10}".format("Rank", "Score", "Time", "Name"))
        print("{:4}  {:5}  {:4}  {:10}".format("-"*4, "-"*5, "-"*4, "-"*10))
        for rank, row in enumerate(rows, start=1):
            print("{:4}  {:5}  {:4.1f}  {}".format(rank, row[0], float(row[1]), row[2]))


def get_ordinal(number):
    # This will do.
    # http://stackoverflow.com/questions/739241/date-ordinal-output
    if 4 <= number <= 20 or 24 <= number <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][number % 10 - 1]

    return "{}{}".format(number, suffix)


def main():
    score = 0
    start_time = time.time()

    # Give cheatsheet.
    print("   1  1  1")
    print("   8  2  8")
    print("  27  3  7")
    print("  64  4  4")
    print(" 125  5  5")
    print(" 216  6  6")
    print(" 343  7  3")
    print(" 512  8  2")
    print(" 729  9  9")
    print("1000 10  0")
    print("")

    for i in range(1, 11):
        # Find a random counting number below 100.
        n = randint(0, 99)

        # Get its cube.
        cube = n * n * n

        # Ask user.
        print("What is the cube root of {:,} ?: ".format(cube), end="")
        answer = raw_input()

        # Give results.
        if answer.isdigit() and int(answer) == n:
            print("Very good.")
            score += 1
        else:
            print("The correct answer is {}.".format(n))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("You scored {} out of 10 and took {} seconds.".format(score, elapsed_time))

    score = Scores(score, elapsed_time)
    if score.is_high_score():
        if score.is_top_score():
            print("Congratulations, you are #1 across the nation!")
        else:
            # print("Congratulations, you are {}th place.".format(8))
            print("Congratulations, you are {} place."
                  .format(get_ordinal(score.position)))

        print("What is your name? ", end="")
        score.add_name(raw_input())

    score.commit_score()
    score.display_high_scores()

if __name__ == "__main__":
    main()


"""
   1  1  1
   8  2  8
  27  3  7
  64  4  4
 125  5  5
 216  6  6
 343  7  3
 512  8  2
 729  9  9
1000 10  0

What is the cube root of 59,319 ?: 39
Very good.
What is the cube root of 157,464 ?: 54
Very good.
What is the cube root of 474,552 ?:
The correct answer is 78.
What is the cube root of 21,952 ?:
The correct answer is 28.
What is the cube root of 314,432 ?:
The correct answer is 68.
What is the cube root of 4,096 ?:
The correct answer is 16.
What is the cube root of 21,952 ?:
The correct answer is 28.
What is the cube root of 2,744 ?:
The correct answer is 14.
What is the cube root of 804,357 ?:
The correct answer is 93.
What is the cube root of 8,000 ?:
The correct answer is 20.
You scored 2 out of 10 and took 13.5098359585 seconds.
Congratulations, you are 7th place.
What is your name? CND

  === HIGH SCORES ===
Rank  Score  Time  Name
----  -----  ----  ----------
   1     10  39.7  CND
   2     10  44.0  CND
   3     10  55.5  CND
   4      9  42.4  CND
   5      2  10.3  didnotplace
   6      2  12.6  pac
   7      2  13.5  CND
   8      2  16.3  haha
   9      2  17.0  Tang
  10      2  21.9  hehaw
"""