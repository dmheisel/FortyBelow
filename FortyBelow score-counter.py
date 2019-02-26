import random
from random import shuffle

#TODO -- set up card values
#TODO -- determine card locations in hand
#TODO -- determine sum, cancels
#TODO -- determine 40 below scores
#TODO -- tracker for whole game - ten rounds

class Card:
    def __init__(self, value): #TODO add hidden function later
        self.value = value
        #self.hidden = True
        self.shown = 'X'
        
    def flip_card(self):
        self.shown = self.value
        return self.shown
        
    def __repr__(self):
        return str(self.shown)

class Deck:
    def __init__(self):
        deck_list = []
        self.deck_list = deck_list
        for n in range(-1, 10):
            self.deck_list.extend([Card(n) for i in range(8)])
        self.deck_list.extend([Card(-10) for i in range(4)])
        random.shuffle(self.deck_list)
    def draw_card(self, draw_number):
        for num in range(draw_number):
            yield self.deck_list.pop()

class Player:
    def __init__(self, name):
        self.name = name
        hand = {}
        self.hand = hand
        n=0
        for card in list(deck.draw_card(6)):
            self.hand[n] = card
            n+=1
    
    def player_hand(self):
        print(f" {self.hand[0]} == {self.hand[1]} == {self.hand[2]}\n {self.hand[3]} == {self.hand[4]} == {self.hand[5]}")

    def flip_card(self, position):
        flipped_card = self.hand[position]
        self.hand[position] = flipped_card.flip_card()
       





deck = Deck()
#print(deck.deck_list)

testplayer = Player('Test')
#print(testplayer.hand)
#print(deck.deck_list)

testplayer.player_hand()
testplayer.flip_card(2)
testplayer.player_hand()
testplayer.flip_card(5)
testplayer.player_hand()
#print(list(deck.draw_card(5)))
#print(deck.deck_list)