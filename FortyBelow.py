import random
from random import shuffle

#DONE -- set up card values
#DONE -- determine card locations in hand
#DONE -- determine sum, cancels
#DONE -- determine 40 below scores
#DONE -- figure out how to sum up card values with ints

#TODO -- tracker for whole game - ten rounds
#TODO -- figure out player input for a whole round
#

#TODO -- multiple players? computer opponent?  keep track of all scores/neighbor cards



def text_deco(func):
    def wrapper(x):
        print("---------------------")
        func(x)
        print("---------------------")
    return wrapper



class Card:
    def __init__(self, value, hidden=None):
        self.value = value
        self.hidden = True
        self.face = 'X'        
    
    def flip_card(self):
        self.hidden = False
        return self
    
    def discard(self):
        discard_pile.discard(self)
    
    #override repr function so when called returns either "X" when face down or card value if face-up    
    def __repr__(self):
        if self.hidden == True:
            return str(self.face)
        elif not self.hidden:
            return str(self.value)
    
   #if integer value of card is needed, provides face value or 0 if card is not flipped (0 will not end up with screwy score valuations with an unknown card value)
    def __int__(self):
        if self.hidden == True:
            return 0
        else: 
            return int(self.value)
    
    #overrides to allow getting a total value of all cards in hand
    def __add__(self, other): 
        return int(self) + other
    
    def __radd__(self, other): 
        return self.__add__(other)
    
    def __iadd__(self, other):
        return other.__add__(self)
    
    

class Deck:
    def __init__(self, pile_type):
        deck_list = []
        #can_discard = None        
        self.deck_list = deck_list
        self.pile_type = pile_type
        self.name = str.title(pile_type + ' pile')
        if self.pile_type == 'draw':
            self.populate()
        #if self.pile_type == 'discard':
        #    self.deck_list.append(Card(4))
        #self.top_card = self.deck_list[-1]        
        print(self.pile_type, self.deck_list)
        
    def populate(self):
        for n in range(-1, 10):
            self.deck_list.extend([Card(n) for i in range(8)])
        self.deck_list.extend([Card(-10) for i in range(4)])
        random.shuffle(self.deck_list)
        top_card = self.deck_list[-1]
        self.discard(top_card)

    def draw_card(self, draw_number = 1):
        for card in range(draw_number):
            yield self.deck_list.pop()
    
    def discard(self, card):
        discarded_card = card
        if discarded_card.face == 'X':
            discarded_card.flip_card()
        self.deck_list.pop()
        discard_pile.deck_list.append(discarded_card)

#player actions:
#DONE       draw hand at start of game
#DONE       flip a card in play
#DONE       draw a new card from the deck and determine its value
#   update?        use new card to replace card in play or discard.
#DONE       exchange a card in play with top card on discard pile
#DONE       check their score(unknown card values return 0 for score)


class Player:
    def __init__(self, name):
        self.name = name
        hand = []
        self.hand = hand
        
    def draw_hand(self, deck_name):
        for card in list(deck_name.draw_card(6)):
            self.hand.append(card)
        self.player_hand()
        return self.hand
    
    @text_deco
    def player_hand(self):
        #prints the layout of the player's card as follows:
        #card layout is:( 1 -- 3 -- 5)
        #               ( 2 -- 4 -- 6)
        print(f"== {self.hand[0]} == {self.hand[2]} == {self.hand[4]} ==\n== {self.hand[1]} == {self.hand[3]} == {self.hand[5]} ==\n =current discard option: {discard_pile.deck_list[-1]}")


    def flip_card(self, position):
        index = position - 1
        self.hand[index].flip_card()
        return self.player_hand()   
    
    def draw_next(self, deck):
        next_card = deck.deck_list[-1]
        next_card.flip_card()
        print(next_card)
        return next_card

    def exchange_card(self, card_position, deck):
        index = card_position-1        
        new_card = self.draw_next(deck)
        self.hand[index].discard()
        self.hand[index] = new_card
        return self.player_hand()
    
    
    def tally_score(self):
     #3 columns from 6 cards -- could increase card count for more columns to add new game options?  iterate through each column to check if pair matches and if so remove it.  If removing two in a row, add -40 ((use a counter to check for multiple matches in a row?))
        score = 0
        lst = self.hand
        card_pairs = [lst[x:x+2] for x in range(0, len(lst), 2)] #slices list into a list of columns
        counter = 0
        for i in card_pairs: ## iterates through each pair of cards
            if i[0] == i[1]:
                counter +=1
                if counter == 2:
                    score -= 40
                    counter = 0
            else:
                score += sum(i)
                counter = 0
        print(card_pairs)
        print(f'Total Score: {score}')
   
    #function to return a list with cancelled cards removed, and return -40 to the score if needed
def tally_score():
     #3 columns from 6 cards -- could increase card count for more columns to add new game options?  iterate through each column to check if pair matches and if so remove it.  If removing two in a row, add -40 ((use a counter to check for multiple matches in a row?))
    score = 0
    column_list = [lst[int(x):int(x)+2] for x in range(0, len(lst), 2)] #slices list into a list of columns
    counter = 0
    for i in column_list:
        if i[0] == i[1]:
            counter +=1
            if counter == 2:
                score -= 40
                counter = 0
        else:
            score = score + i[0]
            score  = score+ i[1]
            counter = 0
    print(column_list)
    print(f'Total Score: {score}')
    
#tally_score([-1,-10,3,1,3,3])

###########################
##TESTING FUNCTIONS BELOW##
###########################

discard_pile = Deck('discard')
play_deck = Deck('draw')

#print(discard_pile.deck_list)
#print(play_deck.pile_type, play_deck.deck_list)

testplayer = Player('Test')

testplayer.draw_hand(play_deck)
#testplayer.flip_card(2)
#testplayer.draw_next(play_deck)
#print(discard_pile.deck_list)
#testplayer.exchange_card(5, discard_pile)
#testplayer.flip_card(4)
#testplayer.flip_card(3)
testplayer.tally_score()
       
## SAVE FOR LATER USE?

        ## User input to determine if they will use the next card from the top of the draw deck.  D to discard to the discard pile face up or corresponding card position to replace that card
        #action = input(F'You drew {next_card} from the draw pile. Input card position you wish to replace or "D" for discard.\n')
        #follows up on input form action --- if D discards shown card, if replacing, discards the hand card and replaces with new one.
        #if action == 'D':
        #    discard_pile.discard(next_card)
        #    print(F'{next_card} discarded to the top of the discard pile.')
        #    print(discard_pile.deck_list[-1])
        #try:
        #    int(action)
        #    if int(action) >= 1 and int(action) <= 6:
        #        index = int(action)-1
        #        replaced_card = self.hand[index]
        #        discard_pile.discard(replaced_card)
        #        self.hand[index] = next_card
        #        print(f'Card position {action} has been replaced with {next_card}.  {replaced_card} has been removed and added to the discard pile.')
        #        print(discard_pile.deck_list[-1])
        #        return self.player_hand()
        #except ValueError:
        #    print('invalid input')
        #else:
        #    print('invalid input')
