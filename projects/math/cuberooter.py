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

        # Make the table if it doesn't exist
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS Scores(Score INT, Time REAL, Name TEXT)")

    def is_top_score(self):
        return True

    def is_high_score(self):
        return True

    def add_name(self, name):
        self.name = name

    def commit_score(self):
        self.cursor.execute("INSERT INTO Scores VALUES({}, {}, '{}')"
                            .format(self.score, self.e_time, self.name))
        # This is needed to commit the transaction.
        self.cursor.execute('PRAGMA table_info(Scores)')

    def display_high_scores(self):
        self.cursor.execute("SELECT * FROM Scores")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

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

    for i in range(1,11):
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
            print("Congratulations, you are {}th place.".format(score.position))
        print("What is your name? ", end="")
        score.add_name(raw_input())

    score.commit_score()
    score.display_high_scores()

if __name__ == "__main__":
    main()