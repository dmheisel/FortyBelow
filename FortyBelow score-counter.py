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
        hidden = 'X'
        self.face = hidden
        
    def flip_card(self):
        self.face = self.value
        return self.face
        
    def __repr__(self):
        return str(self.face)
    

class Deck:
    def __init__(self, pile_type):
        deck_list = []
        #can_discard = None
        #top_card = deck_list[0]
        self.deck_list = deck_list
        self.pile_type = pile_type
        #self.can_discard = can_discard
        
        if self.pile_type == 'draw':
            self.populate()
        #else: can_discard = True
        print(self.deck_list)
        
        
    def populate(self):
        for n in range(-1, 10):
            self.deck_list.extend([Card(n) for i in range(8)])
        self.deck_list.extend([Card(-10) for i in range(4)])
        random.shuffle(self.deck_list)
        
    def draw_card(self, draw_number = 1):
        for card in range(draw_number):
            yield self.deck_list.pop()
    
    def discard(self, card):
        discarded_card = card
        if discarded_card.face == 'X':
            discarded_card.flip_card()
        self.deck_list.append(discarded_card)
        return self.deck_list[-1]

class Player:
    def __init__(self, name):
        self.name = name
        hand = []
        self.hand = hand
        
    
    def draw_hand(self, deck_name):
        for card in list(deck_name.draw_card(6)):
            self.hand.append(card)
        return self.hand
    
    def player_hand(self):
        #orints the layout of the player's card as follows:
        #card layout is:( 1 -- 2 -- 3)
        #               ( 4 -- 5 -- 6)
        print(f" {self.hand[0]} == {self.hand[1]} == {self.hand[2]}\n {self.hand[3]} == {self.hand[4]} == {self.hand[5]}")


    def flip_card(self, position):
        index = position - 1
        self.hand[index].flip_card()
        return self.player_hand()   
    
    def draw_next(self):
        next_card = play_deck.deck_list[-1]
        next_card.flip_card()
        ## User input to determine if they will use the next card from the top of the draw deck.  D to discard to the discard pile face up or corresponding card position to replace that card
        action = input(F'You drew {next_card} from the draw pile. Input card position you wish to replace or "D" for discard.\n')
        #follows up on input form action --- if D discards shown card, if replacing, discards the hand card and replaces with new one.
        if action == 'D':
            discard_pile.discard(next_card)
            print(F'{next_card} discarded to the top of the discard pile.')
            print(discard_pile.deck_list[-1])
        try:
            int(action)
            if int(action) >= 1 and int(action) <= 6:
                index = int(action)-1
                replaced_card = self.hand[index]
                discard_pile.discard(replaced_card)
                self.hand[index] = next_card
                print(f'Card position {action} has been replaced with {next_card}.  {replaced_card} has been removed and added to the discard pile.')
                print(discard_pile.deck_list[-1])
                return self.player_hand()
        except ValueError:
            print('invalid input')
        else:
            print('invalid input')
            
play_deck = Deck('draw')
discard_pile = Deck('discard')
#print(deck.deck_list)
#play_deck.populate()

testplayer = Player('Test')
#print(testplayer.hand)
#print(deck.deck_list)


testplayer.draw_hand(play_deck)

testplayer.player_hand()

print("=================")

testplayer.flip_card(4)

print("=================")
#testplayer.player_hand()
testplayer.flip_card(2)
print("=================")

#print(type(testplayer.hand[0]))
#print(type(testplayer.hand[1]))

testplayer.draw_next()

#print(type(testplayer.hand[4]))
#print(type(play_deck.deck_list[6]))

#testplayer.replace_card(4, play_deck)

#testplayer.player_hand()
#print(list(deck.draw_card(5)))
#print(deck.deck_list)
