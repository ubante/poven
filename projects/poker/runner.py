from projects.poker.classes import Player
from projects.poker.classes import Table
from projects.poker.classes import Hand, Card


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
    print("-- Hole cards dealt.")
    table.print_status()

    # Bet
    table.preflop_bet()
    print("-- After the preflop bet.")
    table.print_status()

    c1 = Card("C", 3)
    c2 = Card("D", 4)
    # print("\n")
    print(c1.is_suited(c2))

    c1 = Card("C", 4)
    c2 = Card("D", 5)
    # print("\n")
    print(c1.is_paired(c2))


if __name__ == "__main__":
    main()

