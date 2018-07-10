from random import randint
from random import shuffle


class Card(object):
    """
    Color and value

    Taking from MagicDraft.
    """

    def __init__(self, suit, numeric_rank):
        self.suit = suit  # C/S/D/H
        self.numeric_rank = numeric_rank  # 1..13

        self.rank = ""
        if numeric_rank == 1:
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


class Hand(object):

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def discard(self, card):
        self.cards.remove(card)

    def __str__(self):
        h = ""
        for card in self.cards:
            h = "{}{} ".format(h, card)

        return h


class Deck(object):

    def __init__(self):
        self._deck = []
        self.create_fresh_deck()
        self.shuffle()

    def create_fresh_deck(self):
        self._deck = []
        for suit in "CSDH":
            for rank in range(1, 14):
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
        # Should exit if there is only a single player.

        position = randint(0, len(self.players)-1)
        # print("position = {} with max of {}".format(position, len(self.players)))
        self.dealer = self.players[position]

        # This could be much better.
        position += 1
        if position == len(self.players):
            position -= len(self.players)
        self.small_blind_player = self.players[position]
        position += 1
        if position == len(self.players):
            position -= len(self.players)
        self.big_blind_player = self.players[position]

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


class Game(object):
    pass












