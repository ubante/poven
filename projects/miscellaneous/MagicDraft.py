import sys
from random import randint

"""
How should I signal in an 8 person draft?

There are eight players.  Each player starts with a 15 card deck.  The "cards" have a color from (
red, blue, green, yellow, purple) and an integer from [1:40].  The cards can repeat in a deck and
the cards are random.  Each player also has a hand.  At the start of the draft, the player looks at
his deck and chooses the "best" card to put in his hand and passes the rest of the deck to the
player to the right.  In the second pick of the draft, the player accepts the deck from the
player to his left and evaluates if he should choose the best card of the same color of his hand or
abandon the color and choose another color card to put into his hand.  He then passes the deck.
This continues until the there are no more cards in the deck.

At what point do players stop changing colors?
Do the players that change colors have better decks?

In the next version, there will be three rounds where each round is as described above.
However, in the second round, the passing switches direction.  After three rounds, each player
will have a deck of 45 cards.

If I commandeer one of the players, can I influence the other players to choose worse decks?
"""


class Card:
    'Color and value'

    def __init__(self, color_letters, max_value):
        self.color_letters = color_letters
        self.max_value = max_value
        self.value = randint(1, self.max_value)
        self.color = self.color_letters[randint(1, len(self.color_letters)) - 1]

    def get_description(self):
        return "%s%d" % (self.color, self.value)


class CardSet:
    """
    Can be used for Deck or Hand
    """

    def __init__(self, set_size, colors, max_value):
        self.cards = []
        for i in range(1, set_size):
            self.cards.append(Card(colors, max_value))

    def get_list(self):
        return self.cards

    def print_list(self):
        print "Card set:",
        for card in self.cards:
            print "%3s" % card.get_description(),
        print ""


class Player:
    """
    I play
    """

    def __init__(self, initial_deck_size, card_colors, card_max_value):
        self.deck = CardSet(initial_deck_size, card_colors, card_max_value)
        self.hand = CardSet(0, card_colors, card_max_value)

    def print_deck(self):
        print "Deck:",
        for card in self.deck.get_list():
            print "%3s" % card.get_description(),
        print ""

    def print_hand(self):
        print "Hand:",
        for card in self.hand.get_list():
            print "%3s" % card.get_description(),
        print ""


class DoubleList(object):
    """
    Thank you, Mr. Parker.
    http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/
    """
    head = None
    tail = None

    def append(self, data):
        new_node = Chair(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.nexxt = None
            self.tail.nexxt = new_node
            self.tail = new_node

    def remove(self, node_value):
        current_node = self.head

        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.nexxt = current_node.nexxt
                    current_node.nexxt.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.nexxt
                    current_node.nexxt.prev = None

            current_node = current_node.nexxt

    def show(self):
        print "Show list data:"
        current_node = self.head
        while current_node is not None:
            print current_node.prev.data if hasattr(current_node.prev, "data") else None,
            print current_node.data,
            print current_node.nexxt.data if hasattr(current_node.nexxt, "data") else None

            current_node = current_node.nexxt
        print "*"*50


class Chair(object):
    """
    Maybe we should just use Player and give it prev and next fields.
    """

    def __init__(self, data, prev, nexxt):
        self.data = data
        self.prev = prev
        self.nexxt = nexxt


class Table:
    """
    Thing the players sit at
    """

    def __init__(self, player_count, round_count, card_max_value, deck_size, card_colors):
        self.player_count = player_count
        self.round_count = round_count
        self.card_max_value = card_max_value
        self.deck_size = deck_size
        self.card_colors = card_colors
        self.players = []

    def initialize(self):
        for i in range(self.player_count):
            self.players.append(Player(self.deck_size, self.card_colors, self.card_max_value))

    def display(self):
        print "Here's the table of %d players:" % self.player_count
        for i in range(0, self.player_count):
            print "Player #%d:" % i
            self.players[i].print_deck()
            self.players[i].print_hand()



def main(argv):
    """
    Let's do it
    """
    player_count = 8
    round_count = 1
    card_max_value = 40
    deck_size = 15
    card_colors = 'RBGYP'

    '''
    debug prints, yeah
    '''
    aCard = Card(card_colors, card_max_value)
    print aCard.get_description()

    aDeck = CardSet(deck_size, card_colors, card_max_value)
    aDeck.print_list()

    print "\nPlayer stuff:"
    aPlayer = Player(deck_size, card_colors, card_max_value)
    aPlayer.print_deck()
    aPlayer.print_hand()

    print
    aTable = Table(player_count, round_count, card_max_value, deck_size, card_colors)
    aTable.initialize()
    aTable.display()


if __name__ == "__main__":
    main(sys.argv[1:])
