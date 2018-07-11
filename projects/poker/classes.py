from random import randint
from random import shuffle


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
        self.all_in = False
        self.next_player = None
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

    def choose_action(self, table_state):
        # This is where the logic will be.
        #
        # Player can:
        #   1. fold
        #   2. call/check
        #   3. raise

        return


class Table(object):

    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.pot = Pot()
        self.button_player = None
        self.dealer = None
        self.small_blind_player = None
        self.big_blind_player = None
        self.small_blind_value = 0
        self.big_blind_value = 0

    def add_player(self, player):
        # For the first player
        if not self.players:
            self.players.append(player)
            return

        self.players[-1].next_player = player
        player.next_player = self.players[0]
        self.players.append(player)

    def __str__(self):
        s = "{} players\n".format(len(self.players))
        for player in self.players:
            s = "{}{}\n".format(s, player)
        s = "{}{}\n".format(s, self.deck)
        s = "{}Pot is ${}.\n".format(s, self.pot.value)

        if self.dealer:
            s = "{}Dealer is {}.\n".format(s, self.dealer.name)
            s = "{}Small blind is {}.\n".format(s, self.small_blind_player.name)
            s = "{}Big blind is {}.\n".format(s, self.big_blind_player.name)

        if self.small_blind_value:
            s = "{}Blinds are ${}/${}.\n".format(s, self.small_blind_value, self.big_blind_value)

        return s

    def assign_dealer(self):
        position = randint(0, len(self.players) - 1)
        self.dealer = self.players[position]
        self.small_blind_player = self.dealer.next_player
        self.big_blind_player = self.small_blind_player.next_player
    #
    # def assign_dealer2(self):
    #     # Should exit if there is only a single player.
    #
    #     position = randint(0, len(self.players)-1)
    #     # print("position = {} with max of {}".format(position, len(self.players)))
    #     self.dealer = self.players[position]
    #
    #     # This could be much better.
    #     position += 1
    #     if position == len(self.players):
    #         position -= len(self.players)
    #     self.small_blind_player = self.players[position]
    #     position += 1
    #     if position == len(self.players):
    #         position -= len(self.players)
    #     self.big_blind_player = self.players[position]

    def set_small_blind(self, sb):
        self.small_blind_value = sb
        self.big_blind_value = sb * 2

    def set_blinds(self):
        self.small_blind_player.pay_blind(self.small_blind_value)
        self.big_blind_player.pay_blind(self.big_blind_value)

    def deal_hole_cards(self):
        for _ in [1, 2]:  # Players start a hand with two hole cards.
            for player in self.players:
                player.hand.add(self.deck.get_card())

    def print_status(self):
        print self.__str__()

    def move_bets_to_pot(self):
        round_bet = 0
        for player in self.players:
            round_bet += player.bet
            player.bet = 0

        self.pot.add(round_bet)

    def preflop_bet(self):
        first_better = self.big_blind_player.next_player
        # print("first bettor is {}".format(first_better.name))
        better = first_better
        better.choose_action(self)
        better = better.next_player

        while not better == first_better:
            # print("next better is {}".format(better.name))
            better = better.next_player
            better.choose_action(self)

        self.move_bets_to_pot()


class Game(object):
    pass












