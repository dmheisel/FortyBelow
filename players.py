class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def __repr__(self):
        return self.name


######################################################################


class Hand:
    """
    Player's hand consists of six cards in three columns of two.
    Card positions are zero indexed
    """

    def __init__(self):
        self.cards = []

    def __repr__(self):
        return str(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def add_card(self, position, card):
        self.cards.insert(position, card)  # inserts before index
        # -1 is unneccessary

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_card(self, position):
        return self.cards.pop(position - 1)

    def clear(self):
        self.cards.clear()

    def show(self):
        """
        prints out the current hand with layout of cards in 3 colums as follows:
        ===============
        ~ 1 -- 2 -- 3 ~
        ~ 4 -- 5 -- 6 ~
        ===============
        """
        print(
            f"~ {self.cards[0]} == {self.cards[1]} == {self.cards[2]} ~\n~ {self.cards[3]} == {self.cards[4]} == {self.cards[5]} ~"
        )

