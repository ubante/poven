"""
I commonly put common things here.
"""
from enum import Enum


class Rarity(Enum):
    NONE = 0
    COMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4


class Pack(object):
    """
    These are the things you earn via rewards or buy via dollars.  The contents
    depend on player collection.  That is, packs will not contain a third copy
    of a card until the player has a complete set of that card's rarity.
    
    I'll have to make some assumptions since the logic isn't public.
    """

    def __init__(self):
        self.cards: list[Card] = []


class Card(object):
    """
    Here are the number of cards in the first expansion of the last three years:

                 total  common  rare  epic  legendary
             WW:  265    106     78    54       27
            FoL:  263    106     76    54       27
            VSC:  245    100     70    50       25

    According to https://hearthstone.fandom.com/wiki/Card_pack_statistics, the
    relevant drop rates are:

    * On average, 5.0% chance to get a Normal Legendary card and guaranteed to
      get one within 40 packs from the previous Normal Legendary card drop.
    * On average, 21.0% chance to get a Normal Epic card and guaranteed to get
      one within 10 packs from the previous Normal Epic card drop.
    * One Legendary card is guaranteed within the first 10 packs of a new
      card expansion.
    * Pity timer for normal legendary: 40 packs
    * Pity timer for normal epic: 10 packs
    """
    
    def __init__(self):
        self.name: str = ""
        self.index: int = 0
        self.rarity: Rarity = Rarity.NONE
        self.dust_value: int = 0
        
class Player(object):
    """
    Me
    """
    
    def __init__(self):
        self.collection = Collection()
        self.pack_count: int = 0

    def is_complete(self, rarity: Rarity):
        pass

class Collection(object):
    def __init__(self):
        pass