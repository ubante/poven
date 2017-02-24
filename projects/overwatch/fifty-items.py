"""
How many boxes to get the 50 item achievement?  Ignore special edition stuff.

Results:
Over 100 runs, the average number of boxes was 509.

"""

from __future__ import print_function

import logging
import sys

from collections import defaultdict
from random import randint


class Item(object):
    def __init__(self):
        self.char_num = None
        self.type = None
        self.rarity = None
        self.index = None

    def to_string(self):
        return("Char num: {}, type: {}, rarity: {}, index: {}"
               .format(self.char_num, self.type, self.rarity, self.index))

    def serialize(self):
        return "{}{}{}{}".format(self.char_num, self.type, self.rarity, self.index)

    @staticmethod
    def generate_random(char_num):
        """
        From https://www.pcgamesn.com/overwatch/overwatch-loot-legendary-skin-chance

        129 commons, 43.6%
        117 rares, 39.5%
        36 epics, 12.2%
        14 legendaries, 4.8%

        Types are:
            k -> skin
            e -> emote
            p -> victory pose
            l -> voice line
            s -> spray
            h -> highlight intro
        :return:
        """
        rarity_roll = randint(0, 100)

        item = Item()
        if rarity_roll < 44:
            item.rarity = 'C'
        elif rarity_roll < 44+40:
            item.rarity = 'R'
        elif rarity_roll < 44+40+12:
            item.rarity = 'E'
        else:
            item.rarity = 'L'

        item.char_num = randint(1, char_num+1)

        # types = ['k', 'e', 'p', 'l', 's', 'h']
        # item.type = types[randint(0, 5)]

        # To calculate the index number, we have to take into account
        # the type and rarity.  This is approximate because to be
        # accurate, we should also take into account the char_num.
        if item.rarity == 'C':
            types = ['l', 's']
            item.type = types[randint(0, 1)]
            if item.type == 'l':
                item.index = randint(1, 14)
            else:
                item.index = randint(1, 31)
        elif item.rarity == 'R':
            types = ['k', 'p']
            item.type = types[randint(0, 1)]
            if item.type == 'k':
                item.index = randint(1, 4)
            else:
                item.index = randint(1, 5)
        elif item.rarity == 'E':
            types = ['k', 'e', 'h']
            item.type = types[randint(0, 2)]
            if item.type == 'k':
                item.index = randint(1, 2)
            elif item.type == 'e':
                item.index = randint(1, 6)
            else:
                item.index = randint(1, 3)
        else:
            item.type = 's'
            item.index = randint(1, 6)

        return item


class Counter(object):
    def __init__(self, char_num):
        self.box_counter = 0
        self.char_num = char_num
        self.unique_count = 0
        self.max_count = 0
        self.repeat_count = 0
        self.char_list = range(1, self.char_num+1)
        self.giant_hash = defaultdict(list)
        logging.debug("Initialized counter with {} chars.".format(self.char_num))

    def achieved(self):
        max_by_char = 0
        max_char = None

        for char in self.giant_hash:
            char_items_len = len(self.giant_hash[char])
            if char_items_len > max_by_char:
                max_by_char = char_items_len
                max_char = char

        logging.debug("Unique count at {}; max length at {}."
                      .format(self.unique_count, max_by_char))

        if max_by_char >= 50:
            return max_char
        else:
            return None

    def get_winning_char(self):
        return self.achieved()

    def open_box(self):
        self.box_counter += 1
        for opened_item in range(1, 5):
            item = Item.generate_random(self.char_num)
            logging.debug(item.to_string())

            if item.serialize() in self.giant_hash[item.char_num]:
                self.repeat_count += 1
                logging.debug("Repeat count at {}.".format(self.repeat_count))
            else:
                self.giant_hash[item.char_num].append(item.serialize())
                self.unique_count += 1
                if len(self.giant_hash[item.char_num]) > self.max_count:
                    self.max_count = len(self.giant_hash[item.char_num])

        logging.debug("Box counter at {}, unique count a {}, max count at {}."
                      .format(self.box_counter, self.unique_count, self.max_count))
        logging.info(", {}, {}, {}"
                     .format(self.box_counter, self.unique_count, self.max_count))


def simulation(num_chars):
    counters = Counter(num_chars)

    while True:
        if counters.achieved():
            break

        counters.open_box()

    return counters


def main():
    # counters = Counter(23)
    #
    # while True:
    #     if counters.achieved():
    #         break
    #
    #     counters.open_box()
    counters = simulation(23)

    print("It took {} boxes to get the achievement.".format(counters.box_counter))
    winner = counters.achieved()
    print("\nThe winning char is {}: {}".format(winner, counters.giant_hash[winner]))
    # print("\nIt took {} commons, {} rares, {} epics and {} legendaries to get to 50."
    #       .format([1,2,3,4]))
    print("\nThere were {} repeats and {} uniques."
          .format(counters.repeat_count, counters.unique_count))


def lite(num_simulations):
    sum = 0

    for _ in range(0, num_simulations):
        counters = simulation(23)
        print(counters.box_counter)
        sum += counters.box_counter

    print("Over {} runs, the average number of boxes was {}."
          .format(num_simulations, sum/num_simulations))

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')

    lite(100)
    # main()
