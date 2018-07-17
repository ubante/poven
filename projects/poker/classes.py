from __future__ import print_function

from collections import defaultdict
from random import randint
from random import shuffle

import itertools
import logging
import sys
import time

"""
This appears to be the rules:
http://www.pokertda.com/poker-tda-rules/

Trying to stick to the definitions in https://www.pokernews.com/pokerterms/reraise.htm

In addtion to those definitions:
  - hand: the five cards a player constructs
  - round: a betting stage; there are four per game: preflop/flop/turn/river
  - game: what happens between the shuffling of the deck
  - tournament: from the first game until there's only one player left
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
        elif numeric_rank == 10:
            self.rank = "T"
        else:
            self.rank = numeric_rank

    def __str__(self):
        # return "{}{:<2}".format(self.suit, self.rank)  # use this if we want 10 instead of T
        return "{}{}".format(self.suit, self.rank)

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


class Evaluation(object):
    """
    This represents the evaluation of five cards.
    """

    def __init__(self, cardset):
        self.cardset = cardset
        self.cards = self.cardset.cards
        self.human_eval = "No eval yet"

        # Primary ranks are:
        # 9: Straight flush
        # 8: Four of a kind
        # 7: Full house
        # 6: Flush
        # 5: Straight
        # 4: Three of a kind
        # 3: Two pair
        # 2: One pair
        # 1: High card
        self.primary_rank = 0

        # Secondary ranks vary with the primary rank.  For example,  for
        # a straight, the secondary rank will be the highest card.  For
        # a full house, the secondary rank will be the numeric value of
        # the three of a kind.
        self.secondary_rank = 0

        # Tertiary rank also vary's with the primary rank.  For a flush,
        # this would be the second highest card.  For a full house, this
        # would be the numeric value of the pair.
        self.tertiary_rank = 0

        # This just goes on and on.  For a flush and high card, it is
        # possible to have a rank for each of the five cards.  For the
        # other types of hands, these will remain at zero.
        self.quaternary_rank = 0
        self.quinary_rank = 0
        self.senary_rank = 0

        self.all_ranks = []
        self.set_all_ranks()

        if self.cardset.length() != 5:
            logging.warn("invalid length: {}".format(self.cardset.length()))
            self.human_eval = "invalid length: {}".format(self.cardset.length())
            return

        self._evaluate()

    def __str__(self):
        return "{}: {} with ranks: {}".format(self.cardset, self.human_eval, self.all_ranks)

    def compare(self, another_eval):
        """
        This will return 1 if this eval is greater and will return 2 if
        the other eval is greater.  If they are even, then this will
        return 0.
        
        Greater values in rank means betterness.

        :param another_eval:
        :return:
        """
        
        if self.primary_rank > another_eval.primary_rank:
            return 1
        elif self.primary_rank < another_eval.primary_rank:
            return 2
        elif self.secondary_rank > another_eval.secondary_rank:
            return 1
        elif self.secondary_rank < another_eval.secondary_rank:
            return 2
        elif self.tertiary_rank > another_eval.tertiary_rank:
            return 1
        elif self.tertiary_rank < another_eval.tertiary_rank:
            return 2
        elif self.quaternary_rank > another_eval.quaternary_rank:
            return 1
        elif self.quaternary_rank < another_eval.quaternary_rank:
            return 2
        elif self.quinary_rank > another_eval.quinary_rank:
            return 1
        elif self.quinary_rank < another_eval.quinary_rank:
            return 2
        elif self.senary_rank > another_eval.senary_rank:
            return 1
        elif self.senary_rank < another_eval.senary_rank:
            return 2
        else:
            return 0
        
    def set_all_ranks(self):
        # There must be a way to make a list of objects where if the
        # objects change, the elements of that list do too.
        self.all_ranks = [self.primary_rank, self.secondary_rank, self.tertiary_rank,
                          self.quaternary_rank, self.quinary_rank, self.senary_rank]

    def is_flush(self):
        suit = None
        for card in self.cards:
            if suit:
                if card.suit != suit:
                    return False
            else:
                suit = card.suit

        return True

    def is_straight(self):
        ranks = self.cardset.get_reverse_ordered_numeric_ranks()
        previous = None
        for rank in ranks:
            # print("rank {}".format(rank))
            if previous:
                if previous - rank != 1:
                    return False
                previous = rank
            else:
                previous = rank

        return True

    def has_matches(self, num_of_matches, look_for_two_pairs=False):
        match = defaultdict(int)
        for card in self.cards:
            match[card.numeric_rank] += 1

        if look_for_two_pairs:
            pairs = []
            other = None
            for rank in match:
                if match[rank] == 2:
                    pairs.append(rank)
                else:
                    other = rank

            if len(pairs) == 2:
                return sorted(pairs, reverse=True), other
            else:
                return False

        other_cards = []
        found_match = None
        for rank in match:
            if match[rank] == num_of_matches:
                found_match = rank
            else:
                other_cards.append(rank)
        if found_match:
            return found_match, sorted(other_cards, reverse=True)
        else:
            return False

    def _evaluate(self):
        if self.is_straight() and self.is_flush():
            self.human_eval = "straight flush"
            self.primary_rank = 9
            self.secondary_rank = self.cardset.get_reverse_ordered_numeric_ranks()[0]
            self.set_all_ranks()
            return

        quads = self.has_matches(4)
        if quads:
            self.human_eval = "four of a kind"
            self.primary_rank = 8
            self.secondary_rank = quads[0]
            self.tertiary_rank = quads[1][0]
            self.set_all_ranks()
            return

        trips = self.has_matches(3)
        pair = self.has_matches(2)
        if trips and pair:
            self.human_eval = "full house"
            self.primary_rank = 7
            self.secondary_rank = trips[0]
            self.tertiary_rank = pair[0]
            self.set_all_ranks()
            return

        if self.is_flush():
            self.human_eval = "flush"
            self.primary_rank = 6
            (self.secondary_rank, self.tertiary_rank, self.quaternary_rank, self.quinary_rank, self.senary_rank) = \
                self.cardset.get_reverse_ordered_numeric_ranks()
            self.set_all_ranks()
            return

        if self.is_straight():
            self.human_eval = "straight"
            self.primary_rank = 5
            self.secondary_rank = self.cardset.get_reverse_ordered_numeric_ranks()[0]
            self.set_all_ranks()
            return

        if trips:
            self.human_eval = "three of a kind"
            self.primary_rank = 4
            self.secondary_rank = trips[0]
            self.tertiary_rank = trips[1][0]
            self.quaternary_rank = trips[1][1]
            self.set_all_ranks()
            return

        pairs = self.has_matches(2, look_for_two_pairs=True)
        if pairs:
            self.human_eval = "two pairs"
            self.primary_rank = 3
            self.secondary_rank = pairs[0][0]
            self.tertiary_rank = pairs[0][1]
            self.quaternary_rank = pairs[1]
            self.set_all_ranks()
            return

        if pair:
            self.human_eval = "one pair"
            self.primary_rank = 2
            self.secondary_rank = pair[0]
            self.tertiary_rank = pair[1][0]
            self.quaternary_rank = pair[1][1]
            self.quinary_rank = pair[1][2]
            self.set_all_ranks()
            return

        # The measly high card.
        self.human_eval = "high card"
        self.primary_rank = 1
        (self.secondary_rank, self.tertiary_rank, self.quaternary_rank, self.quinary_rank, self.senary_rank) = \
            self.cardset.get_reverse_ordered_numeric_ranks()
        self.set_all_ranks()
        return


class CardSet(object):
    """
    This represents a set of Cards.

    One disadvantage of using set() is it does a union which won't be a
    problem until we use a deck that contains duplicates.  That doesn't
    really happen in poker but does in blackjack.
    """

    def __init__(self, cards=None):
        """
        We can instantiate this object with a set() of Card().

        :param cards:
        """
        if cards:
            self.cards = cards
        else:
            self.cards = set()
        self.possible_hands = []  # list of CardSet()
        # self.evaluation = None
        self.best_hand = None

    def __str__(self):
        values = [c.__str__() for c in self.get_ordered_cards()]
        return " ".join(values)

    def length(self):
        return len(self.cards)

    def add(self, card):
        self.cards.add(card)

    def combine(self, another_cardset):
        """
        This will take copy the set() of Card() in another CardSet() and
        add it to this object's self.cards
        :param another_cardset:
        :return:
        """
        self.cards.update(another_cardset.cards)

    def is_better_than(self, another_cardset):
        eval_this = Evaluation(self)  # should we make this a member?
        eval_that = Evaluation(another_cardset)

        comparision = eval_this.compare(eval_that)
        if comparision == 1:
            return True

        return False

    def set_possible_hands(self):
        set_of_subsets = set(itertools.combinations(self.cards, 5))
        for possible_hand in set_of_subsets:
            self.possible_hands.append(CardSet(cards=possible_hand))

    def find_best_hand(self):
        self.set_possible_hands()
        best_hand = None
        for possible in self.possible_hands:
            evaled = Evaluation(possible)
            # print(evaled)

            if best_hand is None:
                best_hand = possible
                # print("^ setting initial hand")
                continue

            if best_hand.is_better_than(possible):
                pass
                # print("^^ keeping")
            else:
                best_hand = possible
                # print("^ new best hand")

        self.best_hand = best_hand  # Just stick to the object's field?

    def get_ordered_cards(self):
        """
        This will return a list of the cards ordered by numeric value.

        :return:
        """
        return sorted(self.cards, key=lambda x: x.numeric_rank, reverse=True)

    def get_reverse_ordered_numeric_ranks(self):
        ordered_ranks = []
        for card in self.cards:
            ordered_ranks.append(card.numeric_rank)

        return sorted(ordered_ranks, reverse=True)


class HoleCards(object):

    def __init__(self):
        self.cards = []  # Phasing this out for self.cardset
        self.cardset = CardSet()

    def add(self, card):
        self.cardset.add(card)

        if not self.cards:
            self.cards.append(card)
            return

        # Order the cards for readability and stuff.  Assume hole cards
        # will never be more than two cards.  If we do Omaha, this will
        # change.
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
                if self.cards[1].numeric_rank == 9:  # Q9
                    return 5
                if self.cards[1].numeric_rank == 8:  # Q8
                    return 7
            elif self.cards[0].numeric_rank == 11:
                if self.cards[1].numeric_rank == 10:  # JT
                    return 3
                if self.cards[1].numeric_rank == 9:  # J9
                    return 4
                if self.cards[1].numeric_rank == 8:  # J8
                    return 6
                if self.cards[1].numeric_rank == 8:  # J7
                    return 8
            elif self.cards[0].numeric_rank == 10:
                if self.cards[1].numeric_rank == 9:  # T9
                    return 4
                if self.cards[1].numeric_rank == 8:  # T8
                    return 5
                if self.cards[1].numeric_rank == 7:  # T7
                    return 7
            elif self.cards[0].numeric_rank == 9:
                if self.cards[1].numeric_rank == 8:  # 98
                    return 4
                if self.cards[1].numeric_rank == 7:  # 97
                    return 5
                if self.cards[1].numeric_rank == 6:  # 96
                    return 8
            elif 8 >= self.cards[0].numeric_rank >= 7:
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 1:  # 87 76
                    return 5
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 2:  # 86 75
                    return 6
                if (self.cards[0].numeric_rank - self.cards[1].numeric_rank) == 3:  # 85 74
                    return 8
            elif self.cards[0].numeric_rank == 6:
                if self.cards[1].numeric_rank == 5 or self.cards[1].numeric_rank == 4:  # 65 64
                    return 7
            elif self.cards[0].numeric_rank == 5:
                if self.cards[1].numeric_rank == 4:  # 54
                    return 6
                if self.cards[1].numeric_rank == 3:  # 53
                    return 7
            elif self.cards[0].numeric_rank == 4:
                if self.cards[1].numeric_rank == 3:  # 43
                    return 7
                if self.cards[1].numeric_rank == 2:  # 42
                    return 8
            elif self.cards[0].numeric_rank == 3:  # 32
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
            if self.cards[1].numeric_rank == 9:  # A9
                return 8
        elif self.cards[0].numeric_rank == 13:
            if self.cards[1].numeric_rank == 12:  # KQ
                return 4
            if self.cards[1].numeric_rank == 11:  # KJ
                return 5
            if self.cards[1].numeric_rank == 10:  # KT
                return 6
            if self.cards[1].numeric_rank == 9:  # K9
                return 8
        elif self.cards[0].numeric_rank == 12:
            if self.cards[1].numeric_rank == 11:  # QJ
                return 5
            if self.cards[1].numeric_rank == 10:  # QT
                return 6
            if self.cards[1].numeric_rank == 9:  # Q9
                return 8
        elif self.cards[0].numeric_rank == 11:
            if self.cards[1].numeric_rank == 10:  # JT
                return 5
            if self.cards[1].numeric_rank == 9:  # J9
                return 7
            if self.cards[1].numeric_rank == 8:  # J8
                return 8
        elif self.cards[0].numeric_rank == 10:
            if self.cards[1].numeric_rank == 9:  # T9
                return 7
            if self.cards[1].numeric_rank == 8:  # T8
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
    In live poker, there can be multiple pots when someone goes in but
    there's still action on the table.

    Here, we will have one pot, the main pot.  But we'll keep track of
    each players equity.  Once the game is complete, we'll segment the
    pot.  Using the equity, we know how much of the pot is split across
    all players.  This is the first segment.  And how much of the pot is
    split across all-1 players.  This is the second segment.  This will
    continue until all equity is accounted for.

    For each segment, we'll find take the involved players and find who
    has the best hand and that player will get that segment of the pot.
    Folded players will have dead hands so their equity remains in the
    pot but their hand cannot win.

    If all players have equal equity, then there will be one segment
    and the player with the best hand gets the whole pot.

    For example, if one player goes all in and everyone else calls
    without going all in themselves, and there is no further betting,
    then each player has equal equity and we still have one segment.

    For another example, if PlayerA goes all on the flop and everyone
    folds except PlayerB and PlayerC.  Those two players call.  Then
    on the turn, they check-check.  Then on the river, they raise-call,
    then we have two segments.  The first segment are for exactly the
    three remaining players.  The second segment is just for PlayerB
    and PlayerC.

    Note that bets do not enter a pot until all betting is complete for
    the round.

    TODO: this needs to track equity because Fifi is beating Gary which
          should be an extreme rarity.
    """

    def __init__(self):
        self.value = 0
        self.equity = defaultdict(int)

    def reset(self):
        self.value = 0

    def add_equity(self, amount, player):  # I might be misusing "equity"
        self.equity[player.name] += amount
        self.value += amount

    def get_segments(self):
        segments = []  # list of tuples (segment_total, player_list)

        return segments

    def split(self, num_players):
        return self.value / num_players


class Player(object):

    def __init__(self, starting_stack, name):
        self.stack = starting_stack
        self.name = name
        self.next_player = None
        self.previous_player = None
        self.riskiness = 0  # A scale of 0..20 where 0 is most cautious.
        self.randomness = 1  # A TBD multiplier to riskiness.

        # The below get reset after each game.
        self.holecards = HoleCards()
        self.best_hand = None
        self.best_hand_evaluation = None
        self.bet = 0
        self.has_folded = False  # Or this could be self.in_the_hand = True
        self.is_all_in = False

    def __str__(self):
        if self.bet:
            return "{} {} ${} (${})".format(self.name, self.holecards, self.stack, self.bet)
        else:
            return "{} {} ${} ".format(self.name, self.holecards, self.stack)

    def reset(self):
        self.holecards = HoleCards()
        self.best_hand = None
        self.best_hand_evaluation = None
        self.bet = 0
        self.has_folded = False  # Or this could be self.in_the_hand = True
        self.is_all_in = False

    def state_without_cards(self):
        if self.bet:
            return "{} xx xx ${} (${})".format(self.name, self.stack, self.bet)
        else:
            return "{} xx xx ${} ".format(self.name, self.stack)

    def pay_blind(self, blind_value):
        if self.stack > blind_value:
            self.stack -= blind_value
            self.bet = blind_value
        else:
            self.all_in()

    def fold(self):
        logging.debug("folding hand")
        self.has_folded = True
        self.holecards.toss()

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
        # Check that player can make this raise.
        if amount > self.stack:
            logging.error("{} is trying to raise (${}) more than their stack (${})."
                          .format(self.name, amount, self.stack))
            sys.exit(1)

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

    def get_user_input_range(self, minimum, maximum):
        while True:
            user_input = input("[{} .. {}]: ".format(minimum, maximum))
            logging.debug("User entered '{}'.".format(user_input))

            if minimum <= user_input <= maximum:
                return user_input
            else:
                logging.info("That is not between {} and {}, inclusive.".format(minimum, maximum))

    def choose_interactive_action(self, table_state):
        print("@@@ ")
        print("@@@ ")
        print("@@@ Here's the table state:")
        print(table_state.state_without_cards())
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
            min_bet = table_state.get_max_bet() - self.bet + table_state.big_blind_value
            print("Enter a value between {} and {}, inclusive:".format(min_bet, self.stack))
            user_input = self.get_user_input_range(min_bet, self.stack)

            # We have to increment what the user added by their current
            # bet because raise_() will decrement what we send it by
            # their current bet.  I'm not crazy about that.
            self.raise_(user_input + self.bet)
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
        if desired_raise > self.stack:
            desired_raise = self.stack
            logging.info("{} has no fear.".format(self.name))

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
        self.button = None  # should this be self.button_player ?
        self.small_blind_value = 0
        self.big_blind_value = 0
        self.game_ctr = 1
        self.bust_log = defaultdict(list)

        # The below values always get reset after each game.
        self.deck = Deck()
        self.community = []  # maybe a list is enough - nope
        self.communityset = CardSet()
        self.main_pot = Pot()
        self.small_blind_player = None
        self.big_blind_player = None
        self.betting_round = None
        self.winners = []

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
        player.previous_player = self.players[-1]
        player.next_player = self.players[0]
        self.players[0].previous_player = player

        self.players.append(player)

    def remove_player(self, player):
        if self.button == player:
            self.button = player.next_player

        player.previous_player.next_player = player.next_player
        player.next_player.previous_player = player.previous_player
        self.players.remove(player)

    def get_cardlist_string(self, cards):
        # Try to move these to CardSet().__str__()
        values = []
        for card in cards:
            values.append("{}{}".format(card.suit, card.numeric_rank))

        return " ".join(values)

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
        s = "{} players / {} folded / {} all-in / game #{}\n" \
            .format(len(self.players), self.count_folded_players(), self.count_all_in_players(), self.game_ctr)
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

    def state_without_cards(self):
        s = "{} players / {} folded / {} all-in / game #{}\n" \
            .format(len(self.players), self.count_folded_players(), self.count_all_in_players(), self.game_ctr)
        #
        # s = "{} players / {} folded / {} all-in \n" \
        #     .format(len(self.players), self.count_folded_players(), self.count_all_in_players())
        for player in self.players:
            s = "{}{}\n".format(s, player.state_without_cards())
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

    def assign_blind_players(self):
        self.small_blind_player = self.button.next_player
        self.big_blind_player = self.small_blind_player.next_player

    def assign_button(self, name=None):
        if name:
            self.button = self.get_player_by_name(name)

        if name is None:
            position = randint(0, len(self.players) - 1)
            self.button = self.players[position]
            logging.debug("Randomly selected '{}' as the button player.".format(self.button.name))
        else:
            logging.debug("Assinging '{}' to be the button player.".format(name))

        self.assign_blind_players()
        # self.small_blind_player = self.button.next_player
        # self.big_blind_player = self.small_blind_player.next_player

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
                player.holecards.add(self.deck.get_card())

    def deal_flop(self):
        for _ in range(0, 3):
            card = self.deck.get_card()
            self.community.append(card)
            # self.community.append(self.deck.get_card())
            self.communityset.add(card)

    def deal_turn(self):
        card = self.deck.get_card()
        self.community.append(card)
        self.communityset.add(card)
        # self.community.append(self.deck.get_card())

    def deal_river(self):
        card = self.deck.get_card()
        self.community.append(card)
        self.communityset.add(card)
        # self.community.append(self.deck.get_card())

    def print_status(self):
        print(self.__str__())

    def check_for_one_player(self):
        remaining_player_count = len(self.players) - self.count_folded_players()
        if remaining_player_count >= 1:
            return False
        elif remaining_player_count == 1:
            logging.info("We are down to one player in the hand.")
            return True
        else:
            logging.error("We should never have less than one player remaining.")
            sys.exit(3)

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
        for player in self.players:
            self.main_pot.add_equity(player.bet, player)
            player.bet = 0

        # round_bet = 0
        # for player in self.players:
        #     round_bet += player.bet
        #     player.bet = 0
        #
        # self.main_pot.add(round_bet)

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
        # TODO: this needs to happen more often
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
        logging.debug("first bettor is {}".format(first_better.name))
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
        active_players = [p for p in self.players if not p.has_folded]

        print("These players are still active:")
        winners = []
        for ap in active_players:
            print("- {}".format(ap))
            combined_cardset = CardSet()
            combined_cardset.combine(ap.holecards.cardset)
            combined_cardset.combine(self.communityset)
            print("  {}".format(combined_cardset))
            combined_cardset.find_best_hand()
            evaled = Evaluation(combined_cardset.best_hand)
            print("  {}".format(evaled))

            if not winners:
                winners = [(ap, combined_cardset, evaled)]
                continue

            comparision = evaled.compare(winners[0][2])
            if comparision == 0:
                print("^tie")
                winners.append((ap, combined_cardset, evaled))
            elif comparision == 1:
                print("^new best deck")
                winners = [(ap, combined_cardset, evaled)]

        print("\nThe winners are:")
        for winner in winners:
            print("{:<65} {}".format(winner[2], winner[0].name))
            self.winners.append(winner[0])

    def payout(self):
        num_winners = len(self.winners)

        # TODO: sidepots
        payout_per_player = self.main_pot.split(num_winners)
        for winner in self.winners:
            print("Paying out {}".format(winner.name))
            print("  current stack: {} + payout: {} = ".format(winner.stack, payout_per_player))
            winner.stack += payout_per_player
            print("  stack after payout: {}".format(winner.stack))

    def remove_busted_players(self):
        busted_players = [p for p in self.players if p.stack == 0]
        for busted_player in busted_players:
            # print(type(busted_player))
            print("busted out: {}".format(busted_player.name))
            self.bust_log[self.game_ctr].append(busted_player.name)
            self.remove_player(busted_player)

        # Checking for negative stacks.
        for player in self.players:
            if player.stack < 0:
                logging.fatal("WE HAVE BUGS.")
                sys.exit(1)

    def check_tournament_winner(self):
        if len(self.players) == 1:
            print("=============================================================")
            print("=============================================================")
            print("=============================================================")
            print("")
            print("After {} games, we have a winner!!!!".format(self.game_ctr))
            print(self.players[0])
            print("")
            print("")
            print("Here's the bust log:")
            for round in sorted(self.bust_log):
                print("{:5} {}".format(round, self.bust_log[round]))

            sys.exit()

    def reset(self):
        for player in self.players:
            player.reset()

        self.assign_blind_players()
        self.deck = Deck()
        self.main_pot.reset()
        self.community = []  # maybe a list is enough - nope
        self.communityset = CardSet()
        self.betting_round = None
        self.winners = []
        self.game_ctr += 1
        # time.sleep(10)  # even players need to rest


class Game(object):
    pass


class Dealer(object):
    """
    Maybe move the mechanics out of Table into here....
    """
    pass
