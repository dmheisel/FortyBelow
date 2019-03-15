import random
import playerinput as pinput
"""
#TODO: Figure out UI!
"""
def main():
    table = Table(['David', 'Jessica'])
    table.start_game()

def banner_deco(func):
    def wrapper(x, *y):
        width = 50
        stars = '*' * width
        print(f'{stars}')
        func(x, *y)
        print(f'{stars}')
    return wrapper

#################################################################
#################################################################

class Table:

    """
    All actions that take place upon the playing table are in here,
    such as dealing cards and players updating their hands.
    """
    def __init__(self, players):
        self.players = [Player(name, Hand()) for name in players]
        self.play_deck = Deck()
        self.discard_pile = Deck(discard = True)
        self.round_num = 1
        self.scores = {player:0 for player in self.players}

    @banner_deco
    def declare_player(self, player, message): 
        print(f'{player}, {message}')
        player.hand.show_hand()

    def deal_hands(self):
        """
        Resets the decks and shuffles out 6 cards to each player, then
        discards the top card from the deck into the discard pile.
        """
        print('Collecting cards... \n'
            'Shuffling deck... \n'
            'Dealing hands... \n'
            'Discarding the top card...')
        self.play_deck.populate()
        self.play_deck.shuffle()
        self.discard_pile.deck.clear()

        for player in self.players:
            player.hand.cards.clear()
            player.hand.add_cards(list(self.play_deck.draw_card(6)))
        for card in self.play_deck.draw_card():
            self.discard_pile.add_card(card.flip_card())
    
    def start_game(self):
        """
        Game setup shuffles deck, deals cards, starts the round,
        and allows each player to flip two cards before play begins.
        """
        self.deal_hands()
        
        #@banner_deco
        print(f'Starting Round {self.round_num}')
        
        if self.round_num == 1:
            for player in self.players:
                pinput.turn_output(self, player, set_up = True)           
        
        self.round_()

    def round_(self):
        """
        Rounds repeat until a player flips all of their cards.
        Once a player flips all their cards, every other player
        draws one last card from the deck before scores are tallied.
        """
        current_player = self.round_num % len(self.players) - 1        
        current_players = self.players[current_player:] + self.players[:current_player]
        
        while len(current_players) == len(self.players):
            if len(current_players) != len(self.players):
                break
            for player in current_players:
                self.turn(player)
                if all(not card.hidden for card in player.hand.cards):
                    current_players.remove(player)
        for player in current_players:
            self.last_turn(player)                
        self.scoring()
        

    def scoring(self):
        for player in self.players:
                added_score = player.tally_score()
                self.scores[player] += added_score
                print(f'{player}, you earned {added_score} points this round!'
                      f'Your current score is {self.scores.get(player)}')
        if self.round_num <10:
            print(f'End of round {self.round_num} \n'
                  f'Current standings are: {self.scores}')
            self.round_num += 1
            self.start_game()
        else:
            winner = min(self.scores, key=self.scores.get)
            print('The game has ended! \n'
                f'Current standings are: {self.scores} \n'
                f'The winner is {winner} with {self.scores.get(winner)} points!')
        
    def turn(self, player):
        self.declare_player(player, 
        'it is now your turn.\n'
        +f'the top of the discard pile is {self.discard_pile.top_card}\n'
        +'here are your current cards:')
        pinput.turn_output(self, player)

    def last_turn(self, player):
        self.declare_player(player, 'it is now the last turn. \nYou may draw one final card from the deck.  Here are your current cards:')
        pinput.turn_output(self, player, last_turn=True)

#################################################################
#################################################################

class Card:
    def __init__(self, value):
        self.value = value
        self.hidden = True
        hidden = 'X'
        self.face = hidden

    def __repr__(self):       
        if self.hidden ==  True:
            return str(self.face)
        else:
            return str(self.value)
    
    def __int__(self):
        """
        if an integer value is needed (for counting up score) and the card 
        is face down, returns 0 instead of the card's value as that won't
        effect the score valuation with an unknown card value
        """
        if self.hidden == True:
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
    
    def flip_card(self):
        self.hidden = False
        return self

#################################################################
#################################################################
    
class Deck:
    """
    Decks can be filled, shuffled, drawn from, and added to(only in the
    case of discard piles)
    """
    
    def __init__(self, discard = False):
        self.deck = []
        self.name = "Deck"
        self.discard = discard
        self.top_card = None
        if self.discard:
            self.name = "Discard Pile"
            
    def populate(self):
        """
        Creates a deck of 100 cards. 96 cards: 
        8 each valued -1 thru 10, 4 each valued -10
        """
        self.deck.clear
        for n in range(-1, 10):
            self.deck.extend([Card(n) for i in range(8)])
        self.deck.extend([Card(-10) for i in range(4)])
        self.top_card = self.deck[-1]
        
    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self, amount = 1):
        """
        Yields the next card popped from the deck, and an amount can be specified to yield multiple cards in a row (e.g. for dealing a new hand)
        """
        for n in range(amount):
            yield self.deck.pop()

    def add_card(self, card):
        if self.discard:
            card.flip_card()
            self.deck.append(card)
            self.top_card = self.deck[-1]
            print(f'A {self.top_card} has been added to the discard pile.')
        else:
            print("ERROR: This deck cannot accept cards")

#################################################################
#################################################################

class Hand:
    """
    Player's hand consists of six cards displayed in three columns of two.
    Card positions are zero indexed and this is adjusted for by subtracting
    one from input referencing a specific position.
    """
    
    def __init__(self):
        self.cards = []
    
    def __repr__(self):
        return self.cards

    def add_card(self, position, card):
        self.cards.insert(position, card)

    def add_cards(self, cards):
        self.cards.extend(cards)
    
    def remove_card(self, position):
        self.cards[position-1].flip_card()
        return self.cards.pop(position-1)

    @banner_deco    
    def show_hand(self):
        """
        prints out the current hand with layout of cards in 3 colums as follows:
        ===============
        ~ 1 -- 2 -- 3 ~
        ~ 4 -- 5 -- 6 ~
        ===============
        """
        print(f"~ {self.cards[0]} == {self.cards[1]} == {self.cards[2]} ~\n~ {self.cards[3]} == {self.cards[4]} == {self.cards[5]} ~")

#################################################################
#################################################################

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        
    
    def __repr__(self):
        return self.name

    def flip(self, position):
        self.hand.cards[position-1].flip_card()
        return self.hand.show_hand()

    def tally_score(self):
        """
        Splits cards into three pairs by column, adds card values if 
        values are known and returns total score.
        Last round initiates flipping all cards prior to calling tally.
        Scoring process is:
        Sum of each column, EXCEPT columns that have matching cards are 0
        Neighboring columns that contain all one card are -40
        """        
        score = 0
        y = len(self.hand.cards)//2
        card_pairs = [[self.hand.cards[x], self.hand.cards[x+y]] for x in range(0, y)]
        temp_40_checker = []
        for i in card_pairs:
            if i[0] == i[-1] and not i[0].hidden and not i[1].hidden:
                if temp_40_checker and temp_40_checker[-1] == i:
                    score -= 40
                    temp_40_checker.clear()
                else:
                    temp_40_checker.append(i)
            else:
                score += sum(i)
                temp_40_checker.clear()
        return score  

##############################################################

if __name__ == '__main__':
    main()
