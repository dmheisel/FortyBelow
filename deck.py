import random


class Card:
    def __init__(self, value):
        self.value = value
        self.hidden = True

    def __repr__(self):
        if self.hidden == True:
            return "X"
        else:
            return str(self.value)

    def __int__(self):
        if self.hidden:
            return 0
        else:
            return int(self.value)

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return other.__add__(self)

    def __eq__(self, other):
        return int(self) == other

    def flip(self):
        self.hidden = False
        return self


#######################################################################


class Deck:
    """
    Decks can be filled, shuffled, drawn from, and added to(only in the
    case of discard piles)
    """

    def __init__(self, discard=False):
        self.card_list = []
        self.cards = iter(self.card_list)
        self.is_discard = discard
        if self.is_discard:
            self.name = "Discard Pile"
        else:
            self.name = "Draw Pile"
            self.build()

    def __repr__(self):
        return str(self.card_list)

    def build(self):
        """
        Creates a deck of 100 cards. 96 cards: 
        8 each valued -1 thru 10, 4 each valued -10
        """
        for n in range(-1, 11):
            self.card_list.extend([Card(n) for i in range(8)])
        self.card_list.extend([Card(-10) for i in range(4)])

    def shuffle(self):
        random.shuffle(self.card_list)
        self.cards = iter(self.card_list)

    def draw(self, amount=1):
        counter = 0
        while counter < amount:
            try:
                yield next(self.cards)
                counter += 1
            except StopIteration:
                self.shuffle()

    def discard(self, card):
        if self.is_discard:
            card.flip()
            self.card_list.insert(0, card)
            print(f"A {card} has been added to the discard pile")
        else:
            print("This deck cannot accept cards")


test_deck = Deck()
test_deck.shuffle()

drawn_card = [card.flip() for card in test_deck.draw()]
print(drawn_card)
