"""
Focus on testing important methods, like buy_pack().
"""
from unittest import TestCase

from projects.hearthstone.src.common import Collection, Card, Rarity, Store, Player


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

    def test_is_complete(self):
        # We'll use epics and assume the same results for other rarities.
        # First test non-completeness.
        self.assertFalse(self.col.is_complete(Rarity.EPIC))

        # Fill that rarity and confirm completeness.
        self.fill_rarity(Rarity.EPIC)
        self.assertTrue(self.col.is_complete(Rarity.EPIC))

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
