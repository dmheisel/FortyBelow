import random

#TODO - in table.round(): determine player order for each round.  
#       first player should alternate each round, and order should be
#       maintained for the last turn in the round.  Likely have to 
#       create a player list that is shifted based on round number.
#TODO - update player actions to include check current scores
#       including hand score and total accumulated score over game
#DONE - throw input error if player attempts to flip a card that's
#       already been flipped over.  Should get to re-choose action.
#DONE - Update scoring -- 40 belows now only occur when all four
#       cards in neighboring columns match.
#TODO - clean up player input.
#       Code currently has player input commented out and gives 
#       a random integer to simulate random input(to test that
#       a complete game could be played without going through
#       entire process)
#DONE - check if cards are properly being flipped whenever action 
#       is taken -- are cards X value being added to hand?
#TODO - clean up rounds?  make code more readable for how rounds
#       and turns are processed




def main():
    table = Table(['David', 'Jessica'])
    table.start_game()

def banner_deco(func):
    def wrapper(x, *y):
        width = 72
        stars = '*' * width
        print(f'{stars}')
        func(x, *y)
        print(f'{stars}')
    return wrapper

def verified_input(prompt, type_=None, min_=None, max_=None, range_=None):
    """
    Function that verifies any user input meets the criteria required to proceed.
    Throws an error and requests new input from user if invalid input is given.
    """
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join((", ".join(map(str, range_[:-1])), str(range_[-1])))))
        else:
            return ui

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
        print(f'Starting Round {self.round_num}')
        for player in self.players:
            #self.declare_player(player, 'You may flip two cards before play starts.')
            #card_1 = verified_input(
            #    f"""{player}, you may flip two cards before play starts. Please choose the #position of the first card you wish to flip:
            #    ~~ 1 ~~ 3 ~~ 5 ~~
            #    ~~ 2 ~~ 4 ~~ 6 ~~
            #    """
            #, type_=int, min_=1, max_=6)
            card_1 = random.randint(1, 6)
            player.hand.cards[int(card_1)-1].flip_card()
            #card_2 = verified_input(
            #    f"""{player}, please choose the position of the second card you wish to flip."""
            #, type_=int, min_=1, max_=6)
            card_2 = random.randint(1, 6)
            player.hand.cards[int(card_2)-1].flip_card()
            self.declare_player(player, 'your cards have been flipped.  Your hand is now:')       
        self.round()

    def round(self):
        """
        Rounds repeat until a player flips all of their cards.
        Once a player flips all their cards, every other player
        draws one last card from the deck before scores are tallied.
        """
        current_player = self.round_num % len(self.players) - 1        
        round_list = self.players[current_player:] + self.players[:current_player]
        
        while len(round_list) == len(self.players):
            if len(round_list) != len(self.players):
                break
            for player in round_list:
                self.declare_player(player, 'it is now your turn.  Here are your current cards:')
                self.turn(player)
                if all(not card.hidden for card in player.hand.cards):
                    round_list.remove(player)
                    
        for player in round_list:
            self.last_turn(player)                
        
        for player in self.players:
            self.scores[player] += player.tally_score()
            print(f'{player}, you earned {player.tally_score()} points this round!')
            print(f'Your current score is {self.scores.get(player)}')

        print(f'End of round {self.round_num}')
        print(f'Current standings are: {self.scores}')
        self.check_winner()

    def turn(self, player):
        """
        Requests input from the player for their next action
        and responds based on player input.  Follow up input for 
        flipping a card asks for card position(column, row)
        Follow up input for checking card in deck asks to discard or 
        choose a card to replace
        """
        #act = verified_input(
        #f"""{self.discard_pile.top_card} is the top card on the discard pile.
        #Please select an action:
        #1. Flip a card in your hand.
        #2. Draw the next card in the deck.
        #3. Draw from the discard pile.
        #"""
        #, type_=int, min_=0, max_=3)
        act = random.randint(1, 3)
        if int(act) == 1:
            #act2 = verified_input(
            #    f"""{player}, please choose a card position to flip:
            #    ~~ 1 ~~ 3 ~~ 5 ~~
            #    ~~ 2 ~~ 4 ~~ 6 ~~
            #    """
            #, type_=int, min_=1, max_=6)
            act2 = random.randint(0, 6)
            
            flipped_card = player.hand.cards[int(act2)-1]
            while not flipped_card.hidden:
                #act2 = verified_input("That card is already flipped.  Please choose a different position")
                print("That card is already flipped.  Please choose a different position")
                act2 = random.randint(0,6)
                flipped_card = player.hand.cards[int(act2)-1]
            flipped_card.flip_card()
            print(f"{player} flipped over {flipped_card} and their hand is now:")
            player.hand.show_hand()

        if int(act) == 2:
            top_card = list(self.play_deck.draw_card())[0]
            top_card.flip_card()
            #act2 = verified_input(
            #    f"""You drew {top_card}. Do you want to keep this card?
            #    Input '0' to discard or choose a position to swap:
            #    ~~ 1 ~~ 3 ~~ 5 ~~
            #    ~~ 2 ~~ 4 ~~ 6 ~~
            #    """
            #, type_=int, min_=0, max_=6,)
            print(f'{player} drew {top_card} from the deck.')
            act2 = random.randint(0, 6)
            if int(act2) == 0:
                print(f'{player} discarded {top_card}.  Their hand is unchanged.')
                self.discard_pile.add_card(top_card)

            else:
                player.hand.add_card(int(act2), top_card)
                print(f"{player} added {top_card} into their hand.")
                self.discard_pile.add_card(player.hand.remove_card(int(act2)))
                print(f"{player}'s hand is now:")
                player.hand.show_hand() 
        if int(act) == 3:
            #act2 = verified_input(
            #   f"""You take {self.discard_pile.top_card} from the discard pile.
            #    Please choose a card position to swap:
            #    ~~ 1 ~~ 3 ~~ 5 ~~
            #    ~~ 2 ~~ 4 ~~ 6 ~~
            #    """
            #, type_=int, min_=0, max_=6)
            act2 = random.randint(1, 6)
            new_card = self.discard_pile.top_card
            player.hand.add_card(int(act2), new_card)
            discarded = player.hand.remove_card(int(act2))
            print(f"{player} took {new_card} from the discard pile into their hand.")
            self.discard_pile.add_card(discarded)
            print(f"{player}'s hand is now:")
            player.hand.show_hand()

    def last_turn(self, player):
        """
        Last turn is similar to a regular turn but you cannot draw from 
        the discard pile.  Player can check top card of draw deck once 
        and replace any card in hand, and any yet un-flipped cards are flipped.
        Last turn automatically adds player's score to score tally.
        """
        self.declare_player(player, 'it is now the last turn. \nYou may draw one card from the deck.  Here are your current cards:')
        top_card = list(self.play_deck.draw_card())[0]
        top_card.flip_card()
        #act = verified_input(
        #f"""You drew {top_card.flip_card()} from the deck.  
        #=======================================
        #Input '0' to discard this card or 
        #choose a position in your hand to swap.
        #~~ 1 ~~ 3 ~~ 5 ~~
        #~~ 2 ~~ 4 ~~ 6 ~~
        #Any remaining face-down cards will be flipped.
        #"""
        #, type_=int, min_=0, max_=6)
        act = random.randint(0, 6)
        print(f'{player} drew {top_card} from the deck.')
        if int(act) == 0:
            print(f'{player} discarded {top_card}.  Their hand is unchanged.')
            self.discard_pile.add_card(top_card)
            print
        else:
            player.hand.add_card(int(act), top_card)
            print(f"{player} added {top_card} into their hand.")
            self.discard_pile.add_card(player.hand.remove_card(int(act)))
        for card in player.hand.cards:
            if card.hidden:
                card.flip_card()
        print(f"Any remaining cards face-down have been flipped. {player}'s hand is now:")
        player.hand.show_hand()   

    def check_winner(self):
        if self.round_num < 10:
            self.round_num += 1
            self.start_game()
        elif self.round_num == 10:
            winner = min(self.scores, key=self.scores.get)
            print(f'The winner is {winner} with {self.scores.get(winner)} points!')

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
            print(f'{self.top_card} has been added to the discard pile.')
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
        ~ 1 -- 3 -- 5 ~
        ~ 2 -- 4 -- 6 ~
        ===============
        """
        print(f"~ {self.cards[0]} == {self.cards[2]} == {self.cards[4]} ~\n~ {self.cards[1]} == {self.cards[3]} == {self.cards[5]} ~")

#################################################################
#################################################################

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.score = 0
    
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
        card_pairs = [self.hand.cards[x:x+2] for x in range(0, len(self.hand.cards), 2)]
        temp_40_checker = []
        for i in card_pairs:
            if i[0] == i[-1]:
                if temp_40_checker and temp_40_checker[-1] == i:
                    score -= 40
                    temp_40_checker.clear()
                else:
                    temp_40_checker.append(i)
            else:
                score += sum(i)
                temp_40_checker.clear()
        self.score = score
        return self.score  

##############################################################

if __name__ == '__main__':
    main()
