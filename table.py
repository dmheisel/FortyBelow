import playerinput as pinput
from deck import Card, Deck
from players import Hand, Player


def main():
    table = Table(["David", "Jessica"])
    table.new_round()


class Table:
    """
    All actions that take place upon the playing table are in here,
    such as dealing cards and players updating their hands.
    """

    def __init__(self, players):
        self.players = [Player(name, Hand()) for name in players]
        self.deck = Deck()
        self.deck.shuffle()
        self.discard_pile = Deck(discard=True)
        self.scoresheet = {player: 0 for player in self.players}
        self.round_counter = 1

    def declare_player(self, player, message):
        print(f"{player}, {message}")
        player.hand.show()

    def reset_table(self):
        for player in self.players:
            player.hand.clear()
        self.deck.shuffle()
        self.discard_pile.card_list.clear()

    def deal(self):
        for player in self.players:
            player.hand.add_cards([card for card in self.deck.draw(6)])
        for card in self.deck.draw():
            self.discard_pile.discard(card)

    def new_round(self):
        self.deal()
        dealer = self.round_counter % len(self.players) - 1
        player_order = self.players[dealer:] + self.players[:dealer]

        for player in player_order:
            pinput.turn_output(self, player, set_up=True)

        while len(player_order) == len(self.players):
            if len(player_order) != len(self.players):
                break
            for player in player_order:
                pinput.turn_output(self, player)
                if all(not card.hidden for card in player.hand):
                    player_order.remove(player)

        for player in player_order:
            pinput.turn_output(self, player, last_turn=True)
        self.end_round()

    def end_round(self):
        for player in self.players:
            add_score = self.tally_score(player)
            self.scoresheet[player] += add_score
            print(
                f"{player}, you earned {add_score} points this round!"
                f"Your current score is {self.scoresheet.get(player)}"
            )
        if self.round_counter < 10:
            print(
                f"End of round {self.round_num} \n"
                f"Current standings are: {self.scoresheet}"
            )
            self.round_counter += 1
            self.reset_table()
            self.new_round()
        else:
            winner = min(self.scoresheet, key=self.scoresheet.get)
            print(
                "GAME END!\n"
                f"FINAL STANDINGS: {self.scoresheet}\n"
                f"WINNER: {winner} with {self.scoresheet.get(winner)} points!"
            )

    def tally_score(self, player):
        score = 0
        y = len(player.hand.cards) // 2
        pairs = [[player.hand.cards[x], player.hand.cards[x + y]] for x in range(0, y)]
        forty_checker = []
        for i in pairs:
            if all(not card.hidden for card in i) and i[0] == i[-1]:
                if forty_checker and forty_checker[-1] == i:
                    score -= 40
                    forty_checker.clear()
                else:
                    forty_checker.append(i)
            else:
                score += sum(i)
                forty_checker.clear()
        return score


if __name__ == "__main__":
    main()
