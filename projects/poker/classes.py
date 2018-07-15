from random import randint
from random import shuffle

import logging
import sys
import time

"""
This appears to be the rules:
http://www.pokertda.com/poker-tda-rules/
"""


class Card(object):
    """
    Color and value

    Taking from MagicDraft.
    """

    def __init__(self, suit, numeric_rank):
        self.suit = suit  # C/S/D/H
        self.numeric_rank = numeric_rank  # 2..14 where an Ace is 14

        self.rank = ""
        if numeric_rank == 14:
            self.rank = "A"
        elif numeric_rank == 11:
            self.rank = "J"
        elif numeric_rank == 12:
            self.rank = "Q"
        elif numeric_rank == 13:
            self.rank = "K"
        else:
            self.rank = numeric_rank

    def __str__(self):
        return "%s%s" % (self.suit, self.rank)

    def is_suited(self, card):
        if self.suit == card.suit:
            return True
        else:
            return False

    def is_paired(self, card):
        if self.numeric_rank == card.numeric_rank:
            return True
        else:
            return False


class Hand(object):

    def __init__(self):
        self.cards = []

    def add(self, card):
        if not self.cards:
            self.cards.append(card)
            return

        # Order the cards for readability and stuff.
        # Assume hand will never be more than two cards.
        if self.cards[0].numeric_rank >= card.numeric_rank:
            self.cards.append(card)
        else:
            self.cards = [card] + self.cards

    def discard(self, card):
        self.cards.remove(card)

    def toss(self):
        self.cards = []

    def __str__(self):

        if not self.cards:
            return ""

        h = ""
        for card in self.cards:
            h = "{}{} ".format(h, card)

        h = "{}[{}]".format(h, self.slansky_malmuth_score())
        return h

    def slansky_malmuth_score(self):
        # From https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands#Sklansky_hand_groups

        # First look at paired cards.
        if self.cards[0].is_paired(self.cards[1]):
            if self.cards[0].numeric_rank >= 11:
                return 1
            elif self.cards[0].numeric_rank >= 10:
                return 2
            elif self.cards[0].numeric_rank >= 9:
                return 3
            elif self.cards[0].numeric_rank >= 8:
                return 4
            elif self.cards[0].numeric_rank >= 7:
                return 5
            elif self.cards[0].numeric_rank >= 5:
                return 6
            elif self.cards[0].numeric_rank >= 2:
                return 7

        # Then look at suited cards.
        if self.cards[0].is_suited(self.cards[1]):
            if self.cards[0].numeric_rank == 14:
                if self.cards[1].numeric_rank == 13:  # AK
                    return 1
                if self.cards[1].numeric_rank == 12 or self.cards[1].numeric_rank == 11:  # AQ AJ
                    return 2
                if self.cards[1].numeric_rank == 10:  # AT
                    return 3
                return 5
            elif self.cards[0].numeric_rank == 13:
                if self.cards[1].numeric_rank == 12:  # KQ
                    return 2
                if self.cards[1].numeric_rank == 11:  # KJ
                    return 3
                if self.cards[1].numeric_rank == 10:  # KT
                    return 4
                if self.cards[1].numeric_rank == 9:  # K9
                    return 6
                return 7
            elif self.cards[0].numeric_rank == 12:
                if self.cards[1].numeric_rank == 11:  # QJ
                    return 3
                if self.cards[1].numeric_rank == 10:  # QT
                    return 4
                if self.cards[1].numeric_rank == 9:   # Q9
                    return 5
                if self.cards[1].numeric_rank == 8:   # Q8
                    return 7
            elif self.cards[0].numeric_rank == 11:
                if self.cards[1].numeric_rank == 10:  # JT
                    return 3
                if self.cards[1].numeric_rank == 9:   # J9
                    return 4
                if self.cards[1].numeric_rank == 8:   # J8
                    return 6
                if self.cards[1].numeric_rank == 8:   # J7
                    return 8
            elif self.cards[0].numeric_rank == 10:
                if self.cards[1].numeric_rank == 9:   # T9
                    return 4
                if self.cards[1].numeric_rank == 8:   # T8
                    return 5
                if self.cards[1].numeric_rank == 7:   # T7
                    return 7
            elif self.cards[0].numeric_rank == 9:
                if self.cards[1].numeric_rank == 8:   # 98
                    return 4
                if self.cards[1].numeric_rank == 7:   # 97
                    return 5
                if self.cards[1].numeric_rank == 6:   # 96
                    return 8
            elif 8 >= self.cards[0].numeric_rank >= 7:
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 1:  # 87 76
                    return 4
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 2:  # 86 75
                    return 6
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 3:  # 85 74
                    return 8
            elif self.cards[0].numeric_rank == 6:
                if self.cards[1].numeric_rank == 5 or self.cards[1].numeric_rank == 4:  # 65 64
                    return 7
            elif self.cards[0].numeric_rank == 5:
                if self.cards[1].numeric_rank == 4:   # 54
                    return 6
                if self.cards[1].numeric_rank == 3:   # 53
                    return 7
            elif self.cards[0].numeric_rank == 4:
                if self.cards[1].numeric_rank == 3:   # 43
                    return 7
                if self.cards[1].numeric_rank == 2:   # 42
                    return 8
            elif self.cards[0].numeric_rank == 3:     # 32
                return 8

        # Finally look at non-suited cards.
        if self.cards[0].numeric_rank == 14:
            if self.cards[1].numeric_rank == 13:  # AK
                return 2
            if self.cards[1].numeric_rank == 12:  # AQ
                return 3
            if self.cards[1].numeric_rank == 11:  # AJ
                return 4
            if self.cards[1].numeric_rank == 10:  # AT
                return 6
            if self.cards[1].numeric_rank == 9:   # A9
                return 8
        elif self.cards[0].numeric_rank == 13:
            if self.cards[1].numeric_rank == 12:  # KQ
                return 4
            if self.cards[1].numeric_rank == 11:  # KJ
                return 5
            if self.cards[1].numeric_rank == 10:  # KT
                return 6
            if self.cards[1].numeric_rank == 9:   # K9
                return 8
        elif self.cards[0].numeric_rank == 12:
            if self.cards[1].numeric_rank == 11:  # QJ
                return 5
            if self.cards[1].numeric_rank == 10:  # QT
                return 6
            if self.cards[1].numeric_rank == 9:   # Q9
                return 8
        elif self.cards[0].numeric_rank == 11:
            if self.cards[1].numeric_rank == 10:  # JT
                return 5
            if self.cards[1].numeric_rank == 9:   # J9
                return 7
            if self.cards[1].numeric_rank == 8:   # J8
                return 8
        elif self.cards[0].numeric_rank == 10:
            if self.cards[1].numeric_rank == 9:   # T9
                return 7
            if self.cards[1].numeric_rank == 8:   # T8
                return 8
        elif self.cards[0].numeric_rank == 9 and self.cards[0].numeric_rank == 8:  # 98
            return 7
        elif self.cards[0].numeric_rank == 8 and self.cards[0].numeric_rank == 7:  # 87
            return 8
        elif self.cards[0].numeric_rank == 7 and self.cards[0].numeric_rank == 6:  # 76
            return 8
        elif self.cards[0].numeric_rank == 6 and self.cards[0].numeric_rank == 5:  # 65
            return 8
        elif self.cards[0].numeric_rank == 5 and self.cards[0].numeric_rank == 4:  # 54
            return 8

        return 20  # This is everything else


class Deck(object):

    def __init__(self):
        self._deck = []
        self.create_fresh_deck()
        self.shuffle()

    def create_fresh_deck(self):
        self._deck = []
        for suit in "CSDH":
            for rank in range(2, 15):
                self._deck.append(Card(suit, rank))

    def shuffle(self):
        shuffle(self._deck)

    def dump(self):
        for card in self._deck:
            print(card)

    def get_card(self):
        return self._deck.pop()

    def __str__(self):
        return "The deck has {} cards remaining.".format(len(self._deck))


class Community(object):
    pass


class Pot(object):
    """
    There can be multiple pots.  The main pot is for everyone while side
    pots exclude all-in players with no equity.

    Note that bets do not enter a pot until all betting is complete.
    """
    def __init__(self):
        self.value = 0

    def add(self, v):
        self.value += v


class Player(object):

    def __init__(self, starting_stack, name):
        self.hand = Hand()
        self.stack = starting_stack
        self.name = name
        self.bet = 0
        self.next_player = None
        self.has_folded = False  # Or this could be self.in_the_hand = True
        self.is_all_in = False
        self.riskiness = 0  # A scale of 0..20 where 0 is most cautious.
        self.randomness = 1  # A TBD multiplier to riskiness.

    def __str__(self):
        if self.bet:
            return "{} {} ${} (${})".format(self.name, self.hand, self.stack, self.bet)
        else:
            return "{} {} ${} ".format(self.name, self.hand, self.stack)

    def pay_blind(self, blind_value):
        # Should check if stack is greater than value.

        self.stack -= blind_value
        self.bet = blind_value

        return True

    def get_player_by_name(self):
        pass  # this may be useful later when setting the button

    def fold(self):
        self.has_folded = True
        self.hand.toss()

        return -1

    def call(self, table_state):
        max_bet = table_state.get_max_bet()
        increase = max_bet - self.bet
        stack_before = self.stack
        bet_before = self.bet

        # Handle the times when calling puts the player all-in.
        if increase >= self.stack:
            self.all_in()
        else:
            self.bet = max_bet
            self.stack -= increase

        logging.debug("max bet: {}, increase: {}, bet before: {}, bet after: {}, stack before: {}, stack after: {}"
                      .format(max_bet, increase, bet_before, self.bet, stack_before, self.stack))

    def raise_(self, amount):
        """

        :param amount:
        :return:
        """
        self.bet += amount
        self.stack -= amount

        return amount  # is this necessary?

    def check(self, table_state):
        return 0  # is this function necessary?

    def all_in(self):
        all_in_amount = self.stack - self.bet
        self.bet += self.stack
        self.stack = 0
        self.is_all_in = True
        logging.info("{} has gone all-in.".format(self.name))

        return all_in_amount

    def choose_action_preflop(self, table_state):
        logging.debug("using the default preflop action of calling")
        self.call(table_state)  # default action

    def choose_action_flop(self, table_state):
        pass

    def choose_action_turn(self, table_state):
        pass

    def choose_action_river(self, table_state):
        pass

    def choose_action(self, table_state):
        # A player can choose an action unless they have folded or are
        # already all-in.
        #
        # Player can:
        #   1. fold - negative one
        #   2. check - return 0
        #   3. call - return the amount to call
        #   4. raise - return a valid raise value

        if self.has_folded:
            logging.debug("{} has folded so no action".format(self.name))
            return -2

        if self.is_all_in:
            logging.debug("{} is all-in so no action".format(self.name))
            return -3

        logging.debug("I am {} and my current bet is {}.".format(self.name, self.bet))

        if table_state.betting_round == "PREFLOP":
            self.choose_action_preflop(table_state)
        elif table_state.betting_round == "FLOP":
            self.choose_action_flop(table_state)
        elif table_state.betting_round == "TURN":
            self.choose_action_flop(table_state)
        elif table_state.betting_round == "RIVER":
            self.choose_action_flop(table_state)
        else:
            logging.fatal("you should never get here")
            sys.exit(1)

        return


class CallingStationPlayer(Player):
    """
    This player will always check or call.
    """

    def choose_action(self, table_state):
        max_bet = table_state.get_max_bet()

        if max_bet > self.bet:
            logging.debug("I am {}; max bet is {} and my current bet is {} so betting the difference."
                          .format(self.name, max_bet, self.bet))
            self.call(table_state)
            logging.debug("  - my bet is now {}".format(self.bet))
        else:
            logging.debug("I am {}; max bet is {} and my current bet is {} so just checking."
                          .format(self.name, max_bet, self.bet))
            self.check(table_state)

        return self.bet


class InteractivePlayer(Player):
    """
    This is you.
    """

    pass


class FoldingPlayer(Player):
    """
    I once saw a disconnected or AFK player make the top 3 in a
    tournament of 9 players.  Epic.
    """
    def choose_action(self, table_state):
        max_bet = table_state.get_max_bet()

        if max_bet > self.bet:
            self.fold()
            logging.debug("I am {} and I'm folding.".format(self.name))
            return -1
        else:
            logging.debug("I am {} and I'm still in it.".format(self.name))
            return 0


class AllInPlayer(Player):
    """
    When raising, this player goes all in.  The needed logic is to
    decide when to raise.

    When not raising or calling, this player will fold.
    """
    pass


class GonzoPlayer(Player):
    """
    This player always goes all in.  Always.
    """
    def choose_action(self, table_state):
        max_bet = table_state.get_max_bet()
        logging.debug("{} is gonzo.  Going all in.  Current: {}, max bet: {}, stack: {}"
                      .format(self.name, self.bet, max_bet, self.stack))
        raise_value = self.all_in()

        return raise_value


class Table(object):

    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.community = []  # maybe a list is enough
        self.main_pot = Pot()
        self.button = None  # should this be self.button_player ?
        self.small_blind_player = None
        self.big_blind_player = None
        self.small_blind_value = 0
        self.big_blind_value = 0
        self.betting_round = None

    def add_player(self, player):
        """
        The seating will eventually be randomized.

        :param player:
        :return:
        """

        # For the first player
        if not self.players:
            self.players.append(player)
            return

        self.players[-1].next_player = player
        player.next_player = self.players[0]
        self.players.append(player)

    def __str__(self):
        s = "{} players / {} folded / {} all-in \n"\
            .format(len(self.players), self.count_folded_players(), self.count_all_in_players())
        for player in self.players:
            s = "{}{}\n".format(s, player)
        s = "{}{}\n".format(s, self.deck)
        s = "{}Pot is ${}.\n".format(s, self.main_pot.value)

        if self.button:
            s = "{}Button is {}.\n".format(s, self.button.name)
            s = "{}Small blind is {}.\n".format(s, self.small_blind_player.name)
            s = "{}Big blind is {}.\n".format(s, self.big_blind_player.name)

        if self.small_blind_value:
            s = "{}Blinds are ${}/${}.\n".format(s, self.small_blind_value, self.big_blind_value)

        if self.community:
            community_string = ""
            for card in self.community:
                community_string += card.__str__() + " "

            s = "{}Community cards: {}".format(s, community_string)

        return s

    def count_folded_players(self):
        count = 0
        for player in self.players:
            if player.has_folded:
                count += 1

        return count

    def count_all_in_players(self):
        count = 0
        for player in self.players:
            if player.is_all_in:
                count += 1

        return count

    def assign_button(self):
        position = randint(0, len(self.players) - 1)
        self.button = self.players[position]
        self.small_blind_player = self.button.next_player
        self.big_blind_player = self.small_blind_player.next_player

    def define_blinds(self, sb):
        """
        Right now, runner.py sets this.  Later, the game will set this
        and the value will increase over the duration of the game.

        :param sb:
        :return:
        """
        self.small_blind_value = sb
        self.big_blind_value = sb * 2

    def post_blinds(self):
        self.small_blind_player.pay_blind(self.small_blind_value)
        self.big_blind_player.pay_blind(self.big_blind_value)

    def get_max_bet(self):
        """
        It might be slightly faster if we keep a running tally.

        :return:
        """
        max_bet = 0
        for player in self.players:
            if player.bet > max_bet:
                max_bet = player.bet

        return max_bet

    def deal_hole_cards(self):
        for _ in [1, 2]:  # Players start a hand with two hole cards.
            for player in self.players:
                player.hand.add(self.deck.get_card())

    def deal_flop(self):
        for _ in range(0, 3):
            self.community.append(self.deck.get_card())

    def print_status(self):
        print self.__str__()

    def check_for_one_player(self):
        if len(self.players) - self.count_folded_players() != 1:
            return False

        logging.info("We are down to one player in the hand.")
        return True

    def check_bet_parity(self):
        """
        Return False unless:
          - all non folded players either have the same bet or are
            all-in

        :return:
        """

        bet = self.get_max_bet()
        for player in self.players:
            logging.debug("checking parity for {}: ".format(player.name))
            if player.has_folded:
                logging.debug("  has folded")
                continue

            if player.is_all_in:
                logging.debug("  is all-in")
                continue

            if player.bet != bet:
                logging.debug("  needs has to take action.  Current bet is {} which is less than {}"
                              .format(player.bet, bet))
                return False

        return True

    def move_bets_to_pot(self):
        round_bet = 0
        for player in self.players:
            round_bet += player.bet
            player.bet = 0

        self.main_pot.add(round_bet)

    def get_player_action(self, player):
        """
        We will eventually import Player classes so there are some
        functions we do not want them to overwrite.  So the Table will
        deal with them.

        :param player:
        :return:
        """
        if player.has_folded:
            logging.debug("{} has folded so no action".format(player.name))
            return -2

        if player.is_all_in:
            logging.debug("{} is all-in so no action".format(player.name))
            return -3

        return player.choose_action(self)

    def preflop_bet(self):
        first_better = self.big_blind_player.next_player  # UTG player
        logging.debug("first bettor is {}".format(first_better.name))
        better = first_better
        better.choose_action(self)
        better = better.next_player

        while not better == first_better:
            logging.debug("next better is {}".format(better.name))
            better.choose_action(self)
            better = better.next_player

        # We can do this preflop because of blinds.  Will need something
        # better in the other betting rounds.
        print("\n- After going around the table once, we now have:")
        self.print_status()

        # Check if there is only player in the hand.
        if self.check_for_one_player():
            logging.debug("There is only one player left.")
            return

        # Continue the bets until:
        #  - every player still in has the same bet
        #  - except for all-in players
        while True:
            # print("There are {} folded players".format(self.count_folded_players()))
            # print("There are {} all-in players".format(self.count_all_in_players()))
            # print("There are {} total players ".format(len(self.players)))

            # Check if everyone is already all in.
            if self.count_all_in_players() + self.count_folded_players() == len(self.players):
                logging.info("Everyone is either all-in or folded.")
                return

            logging.info("Checking on {}".format(better.name))
            # time.sleep(1)

            if better.has_folded:
                better = better.next_player
                continue

            if better.is_all_in:
                better = better.next_player
                continue

            logging.info("{} to bet".format(better.name))
            if self.check_bet_parity():
                logging.info("we are done with betting")
                break

            better.choose_action(self)
            better = better.next_player

    def flop_bet(self):
        first_better = self.small_blind_player  # UTG player
        print("first bettor is {}".format(first_better.name))
        better = first_better
        # better.choose_action(self)
        self.get_player_action(better)


class Game(object):
    pass


class Dealer(object):
    """
    Maybe move the mechanics out of Table into here....
    """
    pass











