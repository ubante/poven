"""
Focus on testing important methods, like buy_pack().
"""
from collections import defaultdict
from unittest import TestCase

from projects.hearthstone.src.common import Collection, Card, Rarity, Store, Player, Dust
from projects.hearthstone.src.constants import RAPTOR1_COUNT_LEGENDARY, RAPTOR1_COUNT_EPIC, RAPTOR1_COUNT_RARE, \
    RAPTOR1_COUNT_COMMON


class TestPlayer(TestCase):
    def test_is_complete(self):
        pass


class TestCollection(TestCase):
    def setUp(self):
        self.col = Collection()

    def fill_rarity(self, rarity):
        complete_count = 2
        if rarity == Rarity.LEGENDARY:
            complete_count = 1

        for index in self.col.raptor1[rarity]:
            self.col.raptor1[rarity][index] = complete_count

    def test_add(self):
        # Make sure that initial dust is zero.
        self.assertEqual(self.col.extra_dust_value, 0)

        # Add a common card; dust value should still be zero.
        self.col.add(Card("test add", 11, Rarity.COMMON))
        self.assertEqual(self.col.extra_dust_value, 0)

        # Add the same common card again; dust value should still be zero.
        self.col.add(Card("test add", 11, Rarity.COMMON))
        self.assertEqual(self.col.extra_dust_value, 0)

        # Add it a third time.  Dust value should still now be 5.
        self.col.add(Card("test add", 11, Rarity.COMMON))
        dust = Dust.get_disenchant_values()
        self.assertEqual(self.col.extra_dust_value, dust[Rarity.COMMON][False])

        # Add a rare card.
        self.col.add(Card("test add", 21, Rarity.RARE))
        self.assertEqual(self.col.extra_dust_value, dust[Rarity.COMMON][False])

        # Add that rare card a total of three times.
        self.col.add(Card("test add", 21, Rarity.RARE))
        self.col.add(Card("test add", 21, Rarity.RARE))
        self.assertEqual(self.col.extra_dust_value,
                         dust[Rarity.COMMON][False] + dust[Rarity.RARE][False])

    def test_is_rarity_complete(self):
        # We'll use epics and assume the same results for other rarities.
        # First test non-completeness.
        self.assertFalse(self.col.is_rarity_complete(Rarity.EPIC))

        # Fill that rarity and confirm completeness.
        self.fill_rarity(Rarity.EPIC)
        self.assertTrue(self.col.is_rarity_complete(Rarity.EPIC))

    def test_is_fully_complete(self):
        # First test non-fully-completeness.
        self.assertFalse(self.col.is_fully_complete())

        # Fill the collection and confirm that it is now fully complete.
        for rarity in Rarity:
            self.fill_rarity(rarity)
        self.assertTrue(self.col.is_fully_complete())

    def test_is_solid(self):
        # First test the negation.
        self.assertFalse(self.col.is_solid())

        for rarity in [Rarity.COMMON, Rarity.RARE, Rarity.EPIC]:
            self.fill_rarity(rarity)
        self.assertTrue(self.col.is_solid())

    def test_contains_legendary(self):
        # First assert that the collection has no legendaries.
        self.assertFalse(self.col.contains_legendary())

        # Add a legendary card and confirm the change.
        legend = Card("Test Legend", 10, Rarity.LEGENDARY)
        self.col.add(legend)
        self.assertTrue(self.col.contains_legendary())

    def test_find_missing_cards_by_rarity(self):
        # The local collection object should have no cards so we can compare it
        # to an empty defaultdict.
        comparison = defaultdict(int)
        comparison[Rarity.LEGENDARY] = 7 * RAPTOR1_COUNT_LEGENDARY
        comparison[Rarity.EPIC] = 2 * RAPTOR1_COUNT_EPIC
        comparison[Rarity.RARE] = 2 * RAPTOR1_COUNT_RARE
        comparison[Rarity.COMMON] = 2 * RAPTOR1_COUNT_COMMON

        missing = self.col.find_missing_cards_by_rarity()

        # Test the negation.
        self.assertNotEqual(comparison, missing)

        # Fix the number of missing legendaries.
        comparison[Rarity.LEGENDARY] = RAPTOR1_COUNT_LEGENDARY
        self.assertEqual(comparison, missing)

        # Add a legendary card to the collection.
        self.col.add(Card("test legendary", 11, Rarity.LEGENDARY))
        missing = self.col.find_missing_cards_by_rarity()

        # This should be unequal to the comparison DD.
        self.assertNotEqual(comparison, missing)

        # Fix the comparison DD to make them equal again.
        comparison[Rarity.LEGENDARY] -= 1
        self.assertEqual(comparison, missing)

    def test_find_missing_cards_cost(self):
        # Compute the cost to make the collection fully complete.
        # This is around 100k dust.
        craft = Dust.get_craft_values()
        expected_cost = 0
        expected_cost += RAPTOR1_COUNT_LEGENDARY * craft[Rarity.LEGENDARY][False]
        expected_cost += RAPTOR1_COUNT_EPIC * craft[Rarity.EPIC][False] * 2
        expected_cost += RAPTOR1_COUNT_RARE * craft[Rarity.RARE][False] * 2
        expected_cost += RAPTOR1_COUNT_COMMON * craft[Rarity.COMMON][False] * 2

        actual_cost = self.col.find_missing_cards_cost()
        self.assertEqual(expected_cost, actual_cost)

    def tearDown(self):
        pass


class TestStore(TestCase):
    def setUp(self):
        self.player = Player("unittest")

    def test_buy_pack(self):
        pack = Store.buy_pack(self.player)
        self.assertEqual(len(pack.cards), 5)
        self.assertFalse(pack.contains_only_commons())

    def test_get_random_card(self):
        common = Store.get_random_card_of_rarity(self.player.collection, Rarity.COMMON)
        self.assertTrue(common.rarity, Rarity.COMMON)

        rare = Store.get_random_card_of_rarity(self.player.collection, Rarity.RARE)
        self.assertTrue(rare.rarity, Rarity.RARE)

        epic = Store.get_random_card_of_rarity(self.player.collection, Rarity.EPIC)
        self.assertTrue(epic.rarity, Rarity.EPIC)

        legendary = Store.get_random_card_of_rarity(self.player.collection, Rarity.LEGENDARY)
        self.assertTrue(legendary.rarity, Rarity.LEGENDARY)
