from projects.poker.classes import Player, CallingStationPlayer, InteractivePlayer, FoldingPlayer, GonzoPlayer
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
    args.verbose = 2  # This is DEBUG level.
    # args.verbose = 1  # This is INFO level.

    # INFO is for interesting things.
    # DEBUG is what happens to interesting things after I lose interest.
    set_logger(args.verbose)
    logging.debug("Here we go.")
    logging.info("Here we go informationally.")
    # logging.warning("This is a fake warning to test logging level.")

    # Business logic below.
    table = Table()

    player1 = Player(1000, "Adam")
    table.add_player(player1)
    player2 = Player(1000, "Bert")
    table.add_player(player2)
    player3 = CallingStationPlayer(1000, "Cail")
    table.add_player(player3)
    player4 = Player(1000, "Dale")
    table.add_player(player4)
    player5 = InteractivePlayer(1000, "Eyor")
    table.add_player(player5)
    player7 = FoldingPlayer(1000, "Fifi")
    table.add_player(player7)
    player8 = GonzoPlayer(1000, "Gary")
    table.add_player(player8)

    table.print_status()

    # Start a game.
    table.betting_round = "PREFLOP"
    table.assign_button()
    table.define_blinds(25)
    table.post_blinds()
    table.deal_hole_cards()
    print("-- Hole cards dealt.")
    table.print_status()

    # Bet preflop
    print("-- This is the preflop bet.")
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
    table.flop_bet()


if __name__ == "__main__":
    main()

