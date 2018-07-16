#!/usr/bin/env python

from __future__ import print_function

ctr = 5
user_choice = "-1"
# while user_choice not in ["0", "1", "2", "3", "4", "5"]:
while user_choice not in map(str, range(0, ctr+1)):
    print("Choose your own adventure [0-{}]: ".format(ctr), end="")
    # user_choice = 0
    user_choice = raw_input()

    # If the user wants to set their own FQDN.
    if user_choice == "1":
        print("You want to replace {}; enter a FQDN: "
              .format("somestring"), end="")
        user_fqdn = raw_input()
        print("Confirm that you want to use {}: ".format(user_fqdn), end="")
        y_n = raw_input("(y/n) ")

        # If confirmed, then what???
        if y_n == 'y':
            continue

        # Otherwise, prompt again.
        user_choice = -1

print("\nYou chose: {}".format(user_choice))
