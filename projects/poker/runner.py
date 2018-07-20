from projects.poker.classes import Player, CallingStationPlayer, InteractivePlayer, FoldingPlayer, GonzoPlayer, \
    AllInPreFlopPlayer
from projects.poker.classes import Pot
from projects.poker.classes import PreFlopTripleBbPlayer
from projects.poker.classes import Table

import argparse
import logging
import sys


def set_logger(verbose_level, logfilename=None):
    """
    Initialize the logger.  The verbose_level should be in [0, 1, 2].
    This won't return anything but will reconfigure the root logger.

    :param logfilename:
    :param verbose_level:
    :return:
    """
    if verbose_level >= 2:
        logging_level = logging.DEBUG
    elif verbose_level == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR

    logging.basicConfig(level=logging_level,
                        stream=sys.stdout,
                        filename=logfilename,
                        format='%(levelname)s - %(message)s')


def main():
    description = '''
    Run the thing.
    '''
    epilog = '''
    Examples:
      ./decomm.py llll --old-hv llll
      ./decomm.py llll  # This will do that thing.
      ./decomm.py llll
    '''
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--important",
                        help="This is the important value that we really need.")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    # For IDE work, set logging level here:
    # args.verbose = 2  # This is DEBUG level.
    # args.verbose = 1  # This is INFO level.

    # INFO is for interesting things.
    # DEBUG is what happens to interesting things after I lose interest.
    set_logger(args.verbose)
    # logging.debug("Here we go.")
    # logging.info("Here we go informationally.")
    # logging.warning("This is a fake warning to test logging level.")

    # Business logic below.
    table = Table()

    initial_stack = 1000
    table.add_player(AllInPreFlopPlayer(initial_stack, "Adam", 5))  # All in at 5
    table.add_player(Player(initial_stack, "Bert"))
    table.add_player(CallingStationPlayer(initial_stack, "Cail"))
    table.add_player(AllInPreFlopPlayer(initial_stack, "Dale", 2))  # deuce
    # player5 = InteractivePlayer(initial_stack, "Eyor")
    table.add_player(FoldingPlayer(initial_stack, "Fifi"))
    # table.add_player(GonzoPlayer(initial_stack, "Gary"))
    table.add_player(PreFlopTripleBbPlayer(initial_stack, "Pete"))
    table.add_player(AllInPreFlopPlayer(initial_stack, "Quin", 4))  # quads
    table.add_player(AllInPreFlopPlayer(initial_stack, "Sven", 7))  # seven
    table.add_player(AllInPreFlopPlayer(initial_stack, "Trey", 3))  # treys

    table.print_status()

    # Start a tournament.
    table.assign_button()
    # table.assign_button("Dale")
    table.define_blinds(25)

    while True:
        table.betting_round = "PREFLOP"
        table.post_blinds()
        table.deal_hole_cards()
        print("-- Hole cards dealt.")
        table.print_status()

        # Bet preflop
        # print("-- This is the preflop bet.")
        table.preflop_bet()
        # print("-- After the preflop bet.")
        # table.print_status()
        print("-- After moving the bets into the main pot.")
        table.move_bets_to_pot()
        table.print_status()

        # Deal the flop
        table.deal_flop()
        table.betting_round = "FLOP"
        print("-- After dealing the flop.")
        table.print_status()

        # Bet the flop
        print("\n-- This is the flop bet.")
        table.post_preflop_bet()
        print("-- This is after the flop round.")
        table.print_status()

        # Deal the turn
        table.deal_turn()
        table.betting_round = "TURN"
        # print("-- After dealing the turn.")
        # table.print_status()

        # Bet the turn
        print("\n-- This is the turn bet.")
        table.post_preflop_bet()
        print("-- This is after the turn round.")
        table.print_status()

        # Deal the river
        table.deal_river()
        table.betting_round = "RIVER"
        # print("-- After dealing the river.")
        # table.print_status()

        # Bet the river
        print("\n-- This is the river bet.")
        table.post_preflop_bet()
        print("-- This is after the river round.")
        table.print_status()

        # For all the different pots, find and pay winners
        print("\n-- Finding and paying the winners.")
        table.pay_winners()
        # sys.exit()

        # # Find the winners
        # print("\n-- Finding the winner.")
        # table.find_winners()
        # # Payout
        # table.payout()
        # print("\n-- Before clearing out the busted players.")
        # table.print_status()

        # Remove busted players
        table.remove_busted_players()
        print("\n-- The table after removing busted players.")
        table.print_status()

        # Check for tournament winner.
        winner = table.check_tournament_winner()
        if winner:
            break

        # Reset the table
        table.reset()
        print("\n-- After resetting the table.")
        table.print_status()

    print("       '{}' is the tournament winner".format(winner.name))
    # print("The tournament winner is: {}".format(winner.name))
    return winner


def main3():
    from classes import Card, CardSet, Evaluation

    cs1 = CardSet()
    cs1.add(Card("C", 5))
    cs1.add(Card("C", 8))
    cs1.add(Card("C", 2))
    cs1.add(Card("C", 11))
    cs1.add(Card("C", 7))
    eval1 = Evaluation(cs1)
    print(eval1)

    cs2 = CardSet()
    cs2.add(Card("H", 11))
    cs2.add(Card("C", 12))
    cs2.add(Card("S", 9))
    cs2.add(Card("D", 10))
    cs2.add(Card("H", 8))
    eval2 = Evaluation(cs2)
    print(eval2)

    cs3 = CardSet()
    cs3.add(Card("C", 11))
    cs3.add(Card("C", 7))
    cs3.add(Card("C", 9))
    cs3.add(Card("C", 10))
    cs3.add(Card("C", 8))
    eval3 = Evaluation(cs3)
    print(eval3)

    cs4 = CardSet()
    cs4.add(Card("C", 11))
    cs4.add(Card("C", 7))
    cs4.add(Card("S", 7))
    cs4.add(Card("D", 7))
    cs4.add(Card("H", 7))
    eval4 = Evaluation(cs4)
    print(eval4)

    cs5 = CardSet()
    cs5.add(Card("C", 3))
    cs5.add(Card("C", 6))
    cs5.add(Card("S", 6))
    cs5.add(Card("D", 6))
    cs5.add(Card("H", 3))
    eval5 = Evaluation(cs5)
    print(eval5)

    cs6 = CardSet()
    cs6.add(Card("C", 3))
    cs6.add(Card("C", 6))
    cs6.add(Card("S", 6))
    cs6.add(Card("D", 6))
    cs6.add(Card("H", 7))
    eval6 = Evaluation(cs6)
    print(eval6)

    cs7 = CardSet()
    cs7.add(Card("C", 3))
    cs7.add(Card("C", 13))
    cs7.add(Card("S", 13))
    cs7.add(Card("D", 11))
    cs7.add(Card("H", 11))
    eval7 = Evaluation(cs7)
    print(eval7)

    cs8 = CardSet()
    cs8.add(Card("C", 3))
    cs8.add(Card("C", 4))
    cs8.add(Card("S", 7))
    cs8.add(Card("D", 7))
    cs8.add(Card("H", 12))
    eval8 = Evaluation(cs8)
    print(eval8)

    cs9 = CardSet()
    cs9.add(Card("C", 3))
    cs9.add(Card("C", 4))
    cs9.add(Card("S", 7))
    cs9.add(Card("D", 11))
    cs9.add(Card("H", 2))
    eval9 = Evaluation(cs9)
    print(eval9)


def print_cardlist(cards):
    values = []
    for card in cards:
        values.append("{}{}".format(card.suit, card.numeric_rank))

    print (" ".join(values))


def main2():
    from classes import Deck
    import itertools

    deck = Deck()
    cardlist = []
    for i in range(0, 7):
        cardlist.append(deck.get_card())

    print_cardlist(cardlist)
    print("length = {}\n".format(len(cardlist)))

    for subset in [c for c in list(itertools.combinations(set(cardlist), 5))]:
        # print(type(list(subset)))
        print_cardlist(list(subset))


def main4():
    p1 = Player(1000, "p1")
    p2 = Player(1000, "p2")
    p3 = Player(1000, "p3")
    p4 = Player(1000, "p4")
    p5 = Player(1000, "p5")

    pot = Pot()
    pot.add_equity(40, p1)
    pot.add_equity(40, p2)
    pot.add_equity(40, p3)
    pot.add_equity(40, p4)
    pot.add_equity(40, p5)

    pot.add_equity(30, p2)
    pot.add_equity(30, p3)
    pot.add_equity(30, p4)
    pot.add_equity(30, p5)

    pot.add_equity(100, p4)
    pot.add_equity(100, p5)

    print(pot)

    segments = pot.get_segments()
    for segment in segments:
        print("{} split by {}".format(segment[0], segment[1]))


def main5():
    print("apple {:2d} {:0.4f}".format(1, 62.5640001297))
    res = ['Irene Adler', 35, 24.798]
    print('{0[0]:{1}s} {0[1]:{2}d} {0[2]:{3}f}'.format(res, 10, 5, .2))
    # Irene Adler    35 24.80
    print('{0[0]:10s} {0[1]:5d} {0[2]:.2f}'.format(res))
    print('{:{}s} {:{}d} {:{}f}'.format(res[0], 10, res[1], 5, res[2], .2))

    print('{:{}s} {:{}d} {:{}f}'.format("Linda", 10, 25, 5, 12.734, .2))
    print('{:{}s} {:5d} {:{}f}'.format("Linda", 10, 25, 12.734, .2))
    print('{:10s} {:5d} {:0.2f}'.format("Linda", 25, 12.734))
    print('{:10s} {:5d} {:0.2f}'.format("apple", 1, 62.5640001297))
    print('apple {:5d} {:0.2f}'.format(1, 62.5640001297))
    print('apple {:2d} {:0.4f}'.format(1, 62.5640001297))
    print("apple {:2d} {:0.4f}".format(1, 62.5640001297))

    num_of_tournaments = 5
    elapsed_time = 62.5640001297
    print("\n{:4d} tournaments took {:0.4f} seconds or {:0.4f}/tournament."
          .format(num_of_tournaments, elapsed_time,
                  elapsed_time/num_of_tournaments))


if __name__ == "__main__":
    # main()
    main5()
    # main4()
    # main3()
    # main2()

