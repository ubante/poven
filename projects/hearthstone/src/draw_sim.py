#!/usr/bin/env python3

"""
How likely are you to get a given card in your opening hand?
"""
import argparse
import logging
import sys
from collections import defaultdict

from projects.hearthstone.src.common import Card, Rarity, Deck, CardSet


# These are global so unless the variable is reassigned, we can manipulate the referenced
# object.
# board = Board()
# moi = Player("Moi")
# debug_runs = False
# debug_groups = False
# debug_do_prompt_moi = True
# debug_one_run = False
# debug_find_sum_of_melds = 0  # 2 is max level
# correct_responses = 0
# wrong_responses = 0


def set_logger(verbose_level):
    # Let there be debug.

    verbose_level = 0 if not verbose_level else verbose_level

    if verbose_level >= 2:
        logging_level = logging.DEBUG
    elif verbose_level == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR

    logging.basicConfig(level=logging_level,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')


def run_one_simulation() -> int:
    """
    This will create a new deck with filler cards and the card we are looking for.
    Then will mulligan if we don't have the card.  If we have the card during the
    opening hand, we'll return 0.  If not, we'll draw until we get the card, or we
    reach the nth round where n is the mana cost of the card.  If we don't have
    the card by the nth round, we'll return 99 otherwise we'll return the round
    number.

    :return:
    """
    is_legendary = False
    mana_cost = 4
    is_playing_first = True

    # https://hsreplay.net/cards/110091/arkonite-defense-crystal
    deck = Deck()
    card1 = Card("Arkonite Defense Crystal", 110091, Rarity.RARE)
    deck.add(card1)
    if is_legendary:
        logging.debug("Only adding one copy of card to deck since it is legendary.")
    else:
        card2 = Card("Arkonite Defense Crystal", 110091, Rarity.RARE)
        deck.add(card2)

    # Fill the deck with other cards
    while deck.size() < 30:
        deck.add(Card("Grizzly Bears", 1337, Rarity.COMMON))
    deck.shuffle()

    # Start with your opening hand.  This could be its own class....
    hand = CardSet()
    initial_hand_size = 4
    if is_playing_first:
        initial_hand_size = 3

    for i in range(0, initial_hand_size):
        hand.add(deck.get())

    # Check if card is in hand.  If it is, exit.
    if hand.contains(card1.index):
        return 0

    # If it isn't, mulligan everything.
    logging.debug("Mulliganning everything.")
    while hand.size() > 0:
        deck.add(hand.get())
    deck.shuffle()
    for i in range(0, initial_hand_size):
        hand.add(deck.get())

    # Check again.
    if hand.contains(card1.index):
        return 0

    # Draw for the card.
    for i in range(1, mana_cost + 1):
        hand.add(deck.get())
        if hand.contains(card1.index):
            return i

    # We didn't get it.
    return 99


def main():
    description = '''
How likely are you to get a given card in your opening hand?  Or to draw it
when you can cast it?

For example, if there's a 5 mana non-legendary card, how likely can you cast
it when you have 5 mana?
'''
    epilog = '''
Examples:
    ./draw_sim.py
'''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    # In this, DEBUG is mostly for entering and exiting methods/functions.  Use the other debug
    # flags for more verbose output.
    args.verbose = 1
    set_logger(args.verbose)
    logging.debug("Here we go.")

    num_sim = 100000
    results = defaultdict(int)
    for i in range(0, num_sim):
        turn = run_one_simulation()
        # print(f"Got the card in round #{turn}.")
        results[turn] += 1

    print(f"Ran the simulation {num_sim} times.")
    print(f"You failed to get the card {round(results[99]/num_sim*100)}% of the time.")
    print(f"You got the card in your opening hand {round(results[0]/num_sim*100)}% of the time.")
    for i in range(1, 99):
        if i in results:
            print(f"You got the card in round #{i} {round(results[i]/num_sim*100)}% of the time.")

    print("So if you mulligan hard, you can get the card in time to cast\nit as early as "
          f"possible {100-(round(results[99]/num_sim*100))}% of the time.")

if __name__ == "__main__":
    main()

"""
Ran the simulation 100000 times.
You failed to get the card 47% of the time.
You got the card in your opening hand 35% of the time.
You got the card in round #1 5% of the time.
You got the card in round #2 5% of the time.
You got the card in round #3 4% of the time.
You got the card in round #4 4% of the time.
So if you mulligan hard, you can get the card in time to cast
it as early as possible 53% of the time.
"""