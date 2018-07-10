from projects.poker.classes import Player
from projects.poker.classes import Table
# from projects.poker.classes import Hand, Card


def main():
    player1 = Player(1000, "Adam")
    player2 = Player(1000, "Bert")
    player3 = Player(1000, "Chit")
    player4 = Player(1000, "Dale")
    table = Table()
    table.add_player(player1)
    table.add_player(player2)
    table.add_player(player3)
    table.add_player(player4)

    # print(table)
    table.print_status()

    # Check the deck
    # table.deck.dump()

    # Start a game.
    table.assign_dealer()
    table.set_small_blind(25)
    table.set_blinds()
    table.deal_hole_cards()
    table.print_status()

    # # test
    # ahand = Hand()
    # ahand.add(Card("H", 1))
    # ahand.add(Card("C", 2))
    # print(ahand)


if __name__ == "__main__":
    main()

