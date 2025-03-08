"""
I commonly put common things here.
"""
import logging
import random
from collections import defaultdict
from enum import Enum

from projects.hearthstone.src.constants import PITY_EPIC, PITY_LEGENDARY, GUARANTEED_LEGENDARY, RAPTOR1_COUNT_COMMON, \
    RAPTOR1_COUNT_LEGENDARY, RAPTOR1_COUNT_RARE, RAPTOR1_COUNT_EPIC, PACK_SIZE, CARD_DROP_RATE_LEGENDARY, \
    CARD_DROP_RATE_EPIC, CARD_DROP_RATE_RARE


class Rarity(Enum):
    COMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4


class Dust(object):
    """
    Ref: https://hearthstone.fandom.com/wiki/Crafting
    """
    @staticmethod
    def get_disenchant_values() -> dict[Rarity, dict]:
        return {Rarity.LEGENDARY: {True: 1600, False: 400},
                Rarity.EPIC: {True: 400, False: 100},
                Rarity.RARE: {True: 100, False: 20},
                Rarity.COMMON: {True: 50, False: 5}}

    @staticmethod
    def get_craft_values() -> dict[Rarity, dict]:
        return {Rarity.LEGENDARY: {True: 3200, False: 1600},
                Rarity.EPIC: {True: 1600, False: 400},
                Rarity.RARE: {True: 800, False: 100},
                Rarity.COMMON: {True: 400, False: 40}}

class Card(object):
    """
    You know, cards.
    """
    def __init__(self, name: str, index: int, rarity: Rarity):
        self.name: str = name
        self.index: int = index
        self.rarity: Rarity = rarity
        self.golden: bool = False
        self.diamond: bool = False
        self.signature: bool = False

    def __str__(self):
        return f"{self.name}, {self.index}, {self.rarity}"

    def dust_value(self):
        dust = Dust.get_disenchant_values()

        return dust[self.rarity][self.golden]


class Pack(object):
    """
    These are the things you earn via rewards or buy via dollars.  The contents
    depend on player collection.  That is, packs will not contain a third copy
    of a card until the player has a complete set of that card's rarity.

    I'll have to make some assumptions since the logic isn't public.
    """

    def __init__(self):
        self.cards: list[Card] = []

    def add(self, card: Card):
        self.cards.append(card)

    def size(self) -> int:
        return len(self.cards)

    def open(self) -> list[Card]:
        return self.cards

    def contains(self, rarity: Rarity) -> bool:
        for card in self.cards:
            if card.rarity == rarity:
                return True

        return False

    def contains_only_commons(self):
        for card in self.cards:
            if card.rarity != Rarity.COMMON:
                return False

        return True

    def get_rarities(self):
        rarities = ""
        for card in self.cards:
            rarities += str(card.rarity.name)
            rarities += " "

        return rarities


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

    def open_pack(self):
        # It would be interesting to record the last pack opened to see if it contained a legendary
        # when we get a fully complete collection.  LATER
        pack = Store.buy_pack(self)
        self.pack_count += 1
        logging.debug(f"{pack.get_rarities()}")
        for card in pack.open():
            self.collection.add(card)


class Collection(object):
    """
    Inspired by https://hsreplay.net/collection/mine/
    """
    def __init__(self):
        self.raptor1 = {Rarity.COMMON: defaultdict(int),
                        Rarity.RARE: defaultdict(int),
                        Rarity.EPIC: defaultdict(int),
                        Rarity.LEGENDARY: defaultdict(int)}
        self.extra_dust_value = 0
        self.can_craft_missing_cards = False

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

        # Update the dust potential of extras.
        if (card.rarity == Rarity.LEGENDARY and self.raptor1[card.rarity][card.index] > 1) or \
                self.raptor1[card.rarity][card.index] > 2:
            self.extra_dust_value += card.dust_value()

            # The below is expensive but more readable than having another dictionary to track
            # missing cards.
            if self.extra_dust_value >= self.find_missing_cards_cost():
                self.can_craft_missing_cards = True
            return

    def is_rarity_complete(self, rarity: Rarity) -> bool:
        """
        Returns true if the collection contains at least a pair of each card
        at the given rarity.

        :param rarity:
        :return:
        """
        for index in self.raptor1[rarity]:
            complete_count = 2
            if rarity == Rarity.LEGENDARY:
                complete_count = 1

            if self.raptor1[rarity][index] < complete_count:
                return False

        return True

    def is_fully_complete(self) -> bool:
        """
        Returns True if the collection has at least one card for each legendary
        and a pair of every other card.

        :return:
        """
        for r in Rarity:
            if not self.is_rarity_complete(r):
                return False

        return True

    def is_solid(self) -> bool:
        """
        Returns true if player has a pair of each common, rare and epic.
        :return:
        """
        for r in [Rarity.COMMON, Rarity.RARE, Rarity.EPIC]:
            for index in self.raptor1[r]:
                if self.raptor1[r][index] < 2:
                    return False

        return True

    def contains_legendary(self) -> bool:
        """
        Returns true if the collection has at least one legendary.

        :return:
        """
        for ind in self.raptor1[Rarity.LEGENDARY]:
            if self.raptor1[Rarity.LEGENDARY][ind] > 0:
                return True

        return False

    def display(self):
        print("\n"
              "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
              "Year of the Raptor.  Set 1 is 'Into the Emerald Dream'")

        for rarity, d in self.raptor1.items():
            print(f"{rarity.name}:")
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
        print(f"{rarity.name:>9}:", end="")
        for ind in self.raptor1[rarity]:
            match self.raptor1[rarity][ind]:
                case 0:
                    print(".", end="")
                case 1:
                    print("_", end="")
                case _:
                    print("-", end="")
        print()

    def print_stats(self):
        all_count = 0
        for rarity in Rarity:
            rarity_count = 0
            total_rarity_count = 0
            rarity_slice = self.raptor1[rarity]
            for index in rarity_slice.keys():
                all_count += rarity_slice[index]
                total_rarity_count += rarity_slice[index]
                if rarity == Rarity.LEGENDARY:
                    if rarity_slice[index]:
                        rarity_count += 1
                        continue
                else:
                    if rarity_slice[index] >= 2:
                        rarity_count += 2
                        continue
                rarity_count += rarity_slice[index]

            out_of = 0
            match rarity:
                case Rarity.COMMON:
                    out_of = RAPTOR1_COUNT_COMMON * 2
                case Rarity.RARE:
                    out_of = RAPTOR1_COUNT_RARE * 2
                case Rarity.EPIC:
                    out_of = RAPTOR1_COUNT_EPIC * 2
                case Rarity.LEGENDARY:
                    out_of = RAPTOR1_COUNT_LEGENDARY

            percentage = int(rarity_count / out_of * 100)

            print(f"{rarity.name:>12}: {rarity_count:>3}/{out_of:<3} "
                  f"{percentage}% {total_rarity_count} cards")
        print(f"Collection has {all_count} cards.")
        print(f"The dust value of extra cards: {self.extra_dust_value}")
        print(f"The dust cost to craft missing cards: {self.find_missing_cards_cost()}")

    def find_missing_cards_by_rarity(self) -> defaultdict[Rarity, int]:
        """
        It might be more efficient to use counters but this is easier to
        understand.
        :return:
        """
        missing = defaultdict(int)

        for rarity in Rarity:
            rarity_slice = self.raptor1[rarity]
            for index in rarity_slice.keys():
                if rarity == Rarity.LEGENDARY:
                    if self.raptor1[rarity][index] == 0:
                        missing[rarity] += 1
                    continue

                if self.raptor1[rarity][index] == 0:
                    missing[rarity] += 2
                elif self.raptor1[rarity][index] == 1:
                    missing[rarity] += 1

        return missing

    def find_missing_cards_cost(self) -> int:
        """
        This will look at the collection's missing cards and tally their dust value.
        :return:
        """
        cost = 0
        missing = self.find_missing_cards_by_rarity()
        dust = Dust.get_craft_values()
        for rarity in missing.keys():
            cost += missing[rarity] * dust[rarity][False]

        return cost


class Store(object):
    @staticmethod
    def buy_pack(player: Player) -> Pack:
        pack = Pack()

        # Check if player has hit 10 pack guarantee.
        if player.pack_count == (GUARANTEED_LEGENDARY - 1) and not player.collection.contains_legendary():
            logging.debug("Hit the 10 pack guarantee.")
            pack.add(Store.get_random_card_of_rarity(player.collection, Rarity.LEGENDARY))

        # Check if the player has hit any pity timer.
        if player.pity_timer[Rarity.EPIC] == (PITY_EPIC - 1):
            logging.debug("Hit the Epic pity timer.")
            pack.add(Store.get_random_card_of_rarity(player.collection, Rarity.EPIC))
            player.pity_timer[Rarity.EPIC] = 0

        if player.pity_timer[Rarity.LEGENDARY] == (PITY_LEGENDARY - 1):
            logging.debug("Hit the Legendary pity timer.")
            pack.add(Store.get_random_card_of_rarity(player.collection, Rarity.LEGENDARY))
            player.pity_timer[Rarity.LEGENDARY] = 0

        # For the remaining cards, use the drop rates.
        for i in range(1, PACK_SIZE - pack.size()):
            pack.add(Store.get_random_card_of_rarity(player.collection, Store.decide_rarity()))

        # For the final card, if the previous four cards were uncommon, then
        # remove common cards from the random pool.
        if pack.contains_only_commons():
            pity = Rarity.COMMON
            while pity == Rarity.COMMON:
                pity = Store.decide_rarity()
            pack.add(Store.get_random_card_of_rarity(player.collection, pity))
        else:
            pack.add(Store.get_random_card_of_rarity(player.collection, Store.decide_rarity()))

        # Increment pity timers if necessary.
        for rarity in [Rarity.LEGENDARY, Rarity.EPIC]:
            if not pack.contains(rarity):
                player.pity_timer[rarity] += 1

        return pack

    @staticmethod
    def decide_rarity() -> Rarity:
        rnd = random.random()

        if rnd < CARD_DROP_RATE_LEGENDARY:
            return Rarity.LEGENDARY
        elif rnd < CARD_DROP_RATE_LEGENDARY + CARD_DROP_RATE_EPIC:
            return Rarity.EPIC
        elif rnd < CARD_DROP_RATE_LEGENDARY + CARD_DROP_RATE_EPIC + CARD_DROP_RATE_RARE:
            return Rarity.RARE

        return Rarity.COMMON

    @staticmethod
    def get_random_card_of_rarity(col: Collection, rarity: Rarity) -> Card:
        # This is the slice of the collection that contains cards of this rarity.
        rarity_slice = col.raptor1[rarity]

        # This will find all the cards that are not full
        complete_count = 2
        if rarity == Rarity.LEGENDARY:
            complete_count = 1

        available_indices = []
        for index in rarity_slice.keys():
            if rarity_slice[index] >= complete_count:
                continue

            available_indices.append(index)

        # When this rarity is already complete, then we can return any card
        # of that rarity.
        if not available_indices:
            available_indices = list(range(1, len(rarity_slice) + 1))

        # Generate a random number.
        rnd = random.randint(1, len(available_indices))
        random_card_index = available_indices[rnd - 1]

        return Card("random", random_card_index, rarity)








