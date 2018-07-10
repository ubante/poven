import sys
from random import randint

"""
How should I signal in an 8 person draft?

There are eight players.  Each player starts with a 15 card deck.  The "cards" have a color from (
red, blue, green, yellow, purple) and an integer from [1:40].  The cards can repeat in a deck and
the cards are random.  Each player also has a hand.  At the start of the draft, the player looks at
his deck and chooses the "best" card to put in his hand and passes the rest of the deck to the
player to the left.  In the second turn of the draft, the player accepts the deck from the
player to his right and evaluates if he should choose the best card of the same color of his
hand or
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
    """
    Color and value
    """

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
        for i in range(0, set_size):
            self.cards.append(Card(colors, max_value))
        self.color_strength = {}
        for color in colors:
            self.color_strength[color] = 0
        self.power_history = []

    def get_list(self):
        return self.cards

    def print_list(self):
        print "Card set:",
        for card in self.cards:
            print "%3s" % card.get_description(),
        print ""

    def remove(self, card):
        self.cards.remove(card)

    def append(self, card):
        self.cards.append(card)

    def get_power(self):

        # First find the strongest color
        color_power = {}
        for color in self.color_strength.keys():
            color_power[color] = 0

        strongest_color = None
        for card in self.cards:
            color_power[card.color] += card.value
            if not strongest_color:
                strongest_color = card.color
                continue
            if color_power[card.color] > color_power[strongest_color]:
                strongest_color = card.color

        # Then score the CardSet
        cardset_power = 0
        for card in self.cards:
            if card.color == strongest_color:
                cardset_power += 4 * card.value
            else:
                cardset_power += card.value

        return cardset_power

    def record_power(self):
        power = self.get_power()
        self.power_history.append(power)


class Player:
    """
    I play

    TODO: maybe Player should track its own name instead of Table doing it???
    """

    def __init__(self, initial_deck_size, card_colors, card_max_value):
        self.deck = CardSet(initial_deck_size, card_colors, card_max_value)
        self.hand = CardSet(0, card_colors, card_max_value)
        # This could be moved to CardSet but since it only matters for hand, I'll leave it in
        # Player.
        self.color_strength = {}
        for color in card_colors:
            self.color_strength[color] = 0
        self.strongest_color = card_colors[0]  # placeholder

    def get_deck(self):
        return self.deck

    def set_deck(self, deck):
        self.deck = deck


    def get_deck_string(self):
        return_string = "Deck: "
        for card in self.deck.get_list():
            return_string += "%4s" % card.get_description()
        return return_string

    def print_deck(self):
        print self.get_deck_string()

    def get_hand_string(self):
        return_string = "Hand: "
        for card in self.hand.get_list():
            return_string += "%4s" % card.get_description()
        return return_string

    def print_hand(self):
        print self.get_hand_string()

    def pick(self):
        """
        We're looking for the card that enhances the color_strength of the hand the most.
        """

        strongest_color_value = self.color_strength[self.strongest_color]
        pick_candidate = None

        for card in self.deck.get_list():
            if card.value + self.color_strength[card.color] > strongest_color_value:
                pick_candidate = card
                strongest_color_value = card.value + self.color_strength[card.color]
                # print "Found a good card: %s" % card.get_description()

        """
        It's possible that we do not find a card that increases our strongest color.  In this case,
        choose a card that has the greatest value.
        """
        if pick_candidate:
            self.deck.remove(pick_candidate)
            self.hand.append(pick_candidate)
            self.strongest_color = pick_candidate.color
            self.color_strength[pick_candidate.color] += pick_candidate.value
        else:
            best_offcolor_card = None
            for card in self.deck.get_list():
                if not best_offcolor_card:
                    best_offcolor_card = card
                    # print "Found an initial off color card: %s" % card.get_description()
                    continue
                if card.value > best_offcolor_card.value:
                    best_offcolor_card = card
                    # print "Found a better off color card: %s" % card.get_description()
            self.deck.remove(best_offcolor_card)
            self.hand.append(best_offcolor_card)
            self.color_strength[best_offcolor_card.color] += best_offcolor_card.value

    def score_hand(self):
        self.hand.record_power()

    def print_power_csv_line(self):
        # print ", ".join(self.hand.power_history)
        print str(self.hand.power_history).strip('[]')


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
        # print "Here's the table of %d players:" % self.player_count
        for i in range(0, self.player_count):
            print "PLAYER #%d  ><  %s  ><  %s" % (i, self.players[i].get_deck_string(),
                                                  self.players[i].get_hand_string())

    def display_with_power(self):
        # print "Here's the table of %d players:" % self.player_count
        for i in range(0, self.player_count):
            print "PLAYER #%d  ><  %s  ><  %s (%d)" % (i, self.players[i].get_deck_string(),
                                                       self.players[i].get_hand_string(),
                                                       self.players[i].hand.get_power())

    def do_turn(self):

        for turn in range (1, self.deck_size+1):

            for player in self.players:
                player.pick()
                player.score_hand()
            print "\nAfter %d turn of picks:" % turn
            self.display_with_power()
            # self.display()

            # Pass the deck
            placeholder_deck = self.players[0].get_deck()
            for i in range (0, self.player_count-1):
                self.players[i].set_deck(self.players[i+1].get_deck())
            self.players[self.player_count-1].set_deck(placeholder_deck)

    def print_power_csv(self):
        print "\nHere are the power histories for graphing:"
        for i in range(0, self.player_count):
            print "Player %d, " % i,
            player = self.players[i]
            player.print_power_csv_line()

def main(argv):
    """
    Let's do it
    """
    player_count = 8
    round_count = 1
    card_max_value = 40
    deck_size = 15
    card_colors = 'RBGYP'

    print "\nHere's the start:"
    aTable = Table(player_count, round_count, card_max_value, deck_size, card_colors)
    aTable.initialize()
    aTable.display()
    print

    aTable.do_turn()
    aTable.print_power_csv()

if __name__ == "__main__":
    main(sys.argv[1:])


















