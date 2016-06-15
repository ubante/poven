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
    'Can be used for Deck or Hand'

    def __init__(self, set_size, colors, max_value):
        self.cards = []
        for i in range(1, set_size):
            self.cards.append(Card(colors, max_value))



class Player:
    'I Play'

    def __init__(self, initial_deck_size, card_colors, card_max_value):
        deck = CardSet(initial_deck_size, card_colors, card_max_value)
        hand = CardSet(0, card_colors, card_max_value)

'''
Let's do it
'''
def main(argv):
    player_count = 8
    round_count = 1
    card_max_value = 40
    deck_size = 15
    card_colors = 'RBGYP'

    aCard = Card(card_colors, card_max_value)
    print aCard.get_description()

    aPlayer = Player(deck_size, card_colors, card_max_value)




if __name__ == "__main__":
    main(sys.argv[1:])