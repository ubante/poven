from projects.poker.classes import Player, CallingStationPlayer, InteractivePlayer, FoldingPlayer
from projects.poker.classes import Table
from projects.poker.classes import Hand, Card


def main():
    table = Table()

    player1 = Player(1000, "Adam")
    player2 = Player(1000, "Bert")
    player3 = CallingStationPlayer(1000, "Chit")
    player4 = Player(1000, "Dale")
    player5 = InteractivePlayer(1000, "Self")
    player7 = FoldingPlayer(1000, "Fifi")

    table.add_player(player1)
    table.add_player(player2)
    table.add_player(player3)
    table.add_player(player4)
    table.add_player(player5)
    table.add_player(player7)

    # print(table)
    table.print_status()

    # Check the deck
    # table.deck.dump()

    # Start a game.
    table.assign_dealer()
    table.define_blinds(25)
    table.post_blinds()
    table.deal_hole_cards()
    print("-- Hole cards dealt.")
    table.print_status()

    # Bet
    print("-- This is the preflop bet.")
    table.preflop_bet()
    print("\n-- After the preflop bet.")
    table.print_status()
    print("-- After moving the bets into the main pot.")
    table.move_bets_to_pot()
    table.print_status()


    # c1 = Card("C", 3)
    # c2 = Card("D", 4)
    # # print("\n")
    # print(c1.is_suited(c2))
    #
    # c1 = Card("C", 4)
    # c2 = Card("D", 5)
    # # print("\n")
    # print(c1.is_paired(c2))


if __name__ == "__main__":
    main()

