from __future__ import print_function

from random import randint
from random import shuffle

import logging
import sys
import time

"""
This appears to be the rules:
http://www.pokertda.com/poker-tda-rules/

Trying to stick to the definitions in https://www.pokernews.com/pokerterms/reraise.htm
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

    def fold(self):
        logging.debug("folding hand")
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

        logging.debug("calling - max bet: {}, increase: {}, bet before/after: {}/{}, stack before/after: {}/{}"
                      .format(max_bet, increase, bet_before, self.bet, stack_before, self.stack))

    def raise_(self, amount):
        """
        The amount is what we are betting.  If we have already bet
        something, than increment that bet to amount.

        The rules for raises are complicated:
        https://poker.stackexchange.com/questions/2729/what-is-the-min-raise-and-min-reraise-in-holdem-no-limit

        So for now make it be anything.
        :param amount:
        :return:
        """
        increase = amount - self.bet
        self.bet += increase
        self.stack -= increase
        logging.info("raising by {}".format(increase))
        return amount  # is this necessary?

    def reraise(self, amount):
        pass  # not sure if we need to distinguish this from raise()

    def check(self, table_state):
        return 0  # is this function necessary?

    def check_or_call(self, table_state):
        if table_state.get_max_bet == 0:
            return self.check(table_state)
        else:
            return self.call(table_state)

    def check_or_fold(self, table_state):
        if table_state.get_max_bet() == 0:
            return self.check(table_state)
        else:
            logging.debug("The current max bet is non zero ({}) so folding."
                          .format(table_state.get_max_bet()))
            return self.fold()

    def all_in(self):
        all_in_amount = self.stack - self.bet
        self.bet += self.stack
        self.stack = 0
        self.is_all_in = True
        logging.info("{} has gone all-in.".format(self.name))

        return all_in_amount

    def choose_action_preflop(self, table_state):
        logging.debug("using the default preflop action of check-calling")
        self.check_or_call(table_state)  # default action

    def choose_action_flop(self, table_state):
        logging.debug("using the default flop action of check-folding")
        self.check_or_fold(table_state)  # default action

    def choose_action_turn(self, table_state):
        logging.debug("using the default turn action of check-folding")
        self.check_or_fold(table_state)  # default action

    def choose_action_river(self, table_state):
        logging.debug("using the default river action of check-folding")
        self.check_or_fold(table_state)  # default action

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
    def get_user_input(valid_characters_iterable=None, valid_numbers=None):
        """
        Build a prompt from the given characters or numbers.  Ask the user
        for input and return that input.

        Do some validation.

        :param valid_characters_iterable:
        :param valid_numbers:
        :return:
        """
        # logging.debug("Prompting user for input.")

        if valid_numbers:
            valid_characters_iterable = [str(x) for x in valid_numbers]

        while True:
            user_input = raw_input("[{}]: "
                                   .format("/".join(valid_characters_iterable)))
            logging.debug("User entered '{}'.".format(user_input))

            # The first half of the below is because the user may hit
            # enter/return so we have to check for that.
            if user_input and user_input in valid_characters_iterable:
                logging.debug("User choose: '{}'.".format(user_input))
                return user_input

    def choose_interactive_action(self, table_state):
        print("@@@ Here are your stats:")
        print("@@@ {}".format(self))
        print("@@@ {}".format(table_state.get_community_string()))
        print("@@@ Your current bet: {}.  The current max bet: {}"
              .format(self.bet, table_state.get_max_bet()))
        print("@@@ ")
        acceptable = []
        print("@@@ You can:")
        print("@@@ 1: fold")
        acceptable.append(1)

        if table_state.get_max_bet() == 0:
            print("@@@ 2: check")
            acceptable.append(2)
        else:
            print("@@@ 3: call")
            acceptable.append(3)

        # If I didn't have a stack, I wouldn't have to choose an action
        # so we can assume we can raise.
        print("@@@ 4: raise")
        acceptable.append(4)
        print("@@@ 5: go all-in")
        acceptable.append(5)

        print("@@@ ")
        print("@@@ Choose an action: ", end="")
        user_action = self.get_user_input(valid_numbers=acceptable)

        if user_action == "1":
            self.fold()
        elif user_action == "2":
            self.check(table_state)
        elif user_action == "3":
            self.call(table_state)
        elif user_action == "4":
            pass
        elif user_action == "5":
            self.all_in()

    def choose_action_preflop(self, table_state):
        self.choose_interactive_action(table_state)

    def choose_action_flop(self, table_state):
        self.choose_interactive_action(table_state)

    def choose_action_turn(self, table_state):
        self.choose_interactive_action(table_state)

    def choose_action_river(self, table_state):
        self.choose_interactive_action(table_state)


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


class PreFlopTripleBbPlayer(Player):
    """
    This player wants action before the flop.  So will make sure no one
    gets to limp in.
    """

    def __init__(self, starting_stack, name):
        super(PreFlopTripleBbPlayer, self).__init__(starting_stack, name)
        self.has_raised = False

    def choose_action_preflop(self, table_state):
        if self.has_raised:
            logging.info("I have already raised so just chilling now")
            return self.check_or_call(table_state)

        # If there's already a bet I have to call, check if it is less
        # than what I want to raise.
        desired_raise = table_state.big_blind_value * 3
        to_bet = table_state.get_max_bet()

        if to_bet > desired_raise:
            logging.info("the table is sufficiently juiced.")
            return self.call(table_state)

        logging.info("this table needs less limpage")
        return self.raise_(desired_raise)


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

    def get_community_string(self):
        community_string = ""
        for card in self.community:
            community_string += card.__str__() + " "

        return "Community cards: {}".format(community_string)

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

        logging.info("Could not find a player named ({})".format(name))
        return None

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
            # TODO: use get_community_string() here
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

    def assign_button(self, name=None):
        if name:
            self.button = self.get_player_by_name(name)

        if name is None:
            position = randint(0, len(self.players) - 1)
            self.button = self.players[position]
            logging.debug("Randomly selected '{}' as the button player.".format(self.button.name))
        else:
            logging.debug("Assinging '{}' to be the button player.".format(name))

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

    def deal_turn(self):
        self.community.append(self.deck.get_card())

    def deal_river(self):
        self.community.append(self.deck.get_card())

    def print_status(self):
        print(self.__str__())

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
                logging.debug("  needs to take action.  Current bet is {} which is less than {}"
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
        self.get_player_action(better)
        better = better.next_player

        while not better == first_better:
            logging.debug("next better is {}".format(better.name))
            self.get_player_action(better)
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

            self.get_player_action(better)
            better = better.next_player

    def post_preflop_bet(self):
        """
        This is for the betting rounds for the flop, turn, and river.

        :return:
        """
        first_better = self.small_blind_player  # UTG player
        print("first bettor is {}".format(first_better.name))
        better = first_better
        self.get_player_action(better)
        better = better.next_player

        while not better == first_better:
            logging.debug("next better is {}".format(better.name))
            self.get_player_action(better)
            better = better.next_player

        while True:
            if self.count_all_in_players() + self.count_folded_players() == len(self.players):
                return

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

            self.get_player_action(better)
            better = better.next_player

    def find_winners(self):
        pass




class Game(object):
    pass


class Dealer(object):
    """
    Maybe move the mechanics out of Table into here....
    """
    pass











