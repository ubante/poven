"""
I commonly put common things here.
"""
from collections import defaultdict
from enum import Enum

from projects.hearthstone.src.constants import PITY_EPIC, PITY_LEGENDARY, GUARANTEED_LEGENDARY, RAPTOR1_COUNT_COMMON, \
    RAPTOR1_COUNT_LEGENDARY, RAPTOR1_COUNT_RARE, RAPTOR1_COUNT_EPIC


class Rarity(Enum):
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
    You know, cards.
    """
    def __init__(self, name: str, index: int, rarity: Rarity):
        self.name: str = name
        self.index: int = index
        self.rarity: Rarity = rarity
        self.dust_value: int = 0

    @staticmethod
    def random():  # strange that I can't use Card as a hint
        """
        This should be a random card irrespective of the player's collection.
        :return:
        """
        random_card = Card("name33", 33, Rarity.COMMON)
        return random_card


class Player(object):
    """
    Me

    Here, I'm assuming there is only one set.  In Collection(), I'm making space for multiple
    sets.  This is okay for now.
    """
    
    def __init__(self, name):
        self.name = name
        self.collection = Collection()
        self.pack_count: int = 0
        self.pity_timer = {Rarity.EPIC: 0,
                           Rarity.LEGENDARY:0}

    def get_pack(self):
        pass


class Collection(object):
    """
    Inspired by https://hsreplay.net/collection/mine/
    """
    def __init__(self):
        self.raptor1 = {Rarity.COMMON: defaultdict(int),
                        Rarity.RARE: defaultdict(int),
                        Rarity.EPIC: defaultdict(int),
                        Rarity.LEGENDARY: defaultdict(int)}
        Collection.initialize(self.raptor1,
                              RAPTOR1_COUNT_COMMON,
                              RAPTOR1_COUNT_RARE,
                              RAPTOR1_COUNT_EPIC,
                              RAPTOR1_COUNT_LEGENDARY)

    @staticmethod
    def initialize(hs_set: dict, common: int, rare: int,
                   epic: int, legendary: int):
        """
        I'm tempted to make a set class.
        :param hs_set:
        :param common:
        :param rare:
        :param epic:
        :param legendary:
        :return:
        """
        for i in range(1, common + 1):
            hs_set[Rarity.COMMON][i] = 0
        for i in range(1, rare + 1):
            hs_set[Rarity.RARE][i] = 0
        for i in range(1, epic + 1):
            hs_set[Rarity.EPIC][i] = 0
        for i in range(1, legendary + 1):
            hs_set[Rarity.LEGENDARY][i] = 0

    def add(self, card: Card):
        self.raptor1[card.rarity][card.index] += 1

    def is_solid(self) -> bool:
        """
        Returns true if player has a pair of each common, rare and epic.
        :return:
        """
        for r in Rarity:
            for index in self.raptor1[r]:
                if self.raptor1[r][index] < 2:
                    return False

        return True

    def contains_legendary(self) -> bool:
        for ind in self.raptor1[Rarity.LEGENDARY]:
            if self.raptor1[Rarity.LEGENDARY][ind] > 0:
                return True

        return False

    def display(self):
        print("\n-----------------------------------------------\n"
              "Year of the Raptor.  Set 1 is 'Into the Emerald Dream'")

        for r,d in self.raptor1.items():
            print(f"{r}:")
            for index in d:
                print(f"{index:>3}:{d[index]:>2}", end=" ")
                if not index % 10 and index != len(d):
                    print()
            print()

    def compact_display(self):
        self.compact_display_line(Rarity.COMMON)
        self.compact_display_line(Rarity.RARE)
        self.compact_display_line(Rarity.EPIC)
        self.compact_display_line(Rarity.LEGENDARY)

    def compact_display_line(self, rarity):
        print(f"{rarity:>16}:", end="")
        for ind in self.raptor1[rarity]:
            match self.raptor1[rarity][ind]:
                case 0:
                    print(".", end="")
                case 1:
                    print("_", end="")
                case _:
                    print("-", end="")
        print()

class Store(object):
    @staticmethod
    def buy_pack(player: Player) -> Pack:
        pack = Pack()

        # Check if player has hit 10 pack guarantee.
        if player.pack_count == (GUARANTEED_LEGENDARY - 1) and not player.collection.contains_legendary():
            # Add a random legendary to pack
            pass

        # Check if the player has hit any pity timer.
        if player.pity_timer[Rarity.EPIC] == (PITY_EPIC - 1):
            # Add an epic to pack

            player.pity_timer[Rarity.EPIC] = 0

        if player.pity_timer[Rarity.LEGENDARY] == (PITY_LEGENDARY - 1):
            # Add an epic to pack

            player.pity_timer[Rarity.LEGENDARY] = 0

        # For the remaining cards, use the drop rates.

        # For the final card, if the previous four cards were uncommon, then
        # remove common cards from the random pool.

        return pack

    @staticmethod
    def get_random_card(col: Collection, rarity: Rarity) -> Card:
        pass



