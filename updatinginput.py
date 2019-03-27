"""
File to handle all player input options
Possible player actions:
Check current scores/hand score
Flip a card
Draw a card from the deck
Take the top discarded card
"""

def input_validator(range_ = None):
    """
    Decorator function intended to verify user input.  Checks if input is an integer within range passed as arg to decorator with keyword 'range_'
    """
    def validating(func):
        def validated(*args, **kwargs):
            while True:
                try: 
                    ui = int(func(*args, **kwargs))
                except ValueError:
                    print("Please input a valid number")
                    continue
                if range_  and ui not in range_:
                    print(f'Please input a valid number between {range_.start} and {range_.stop - 1}.')
                else:
                    return ui
        return validated
    return validating

flip = "Flip a card in your hand."
draw = "Draw a card from the deck."
take_discard = "Take the top card on the discard pile."
check_score = "Check the scoresheet and this hand's current score."
choose_position = (
    "Please select a position in your hand from the chart below.\n"
    "==================================\n"
    "~~ 1 ~~ 2 ~~ 3 ~~\n"
    "~~ 4 ~~ 5 ~~ 6 ~~\n"
    "==================================\n"
)

action_key = {0: check_score, 1: draw, 2: take_discard, 3: flip}

@input_validator(range_ = range(4))
def regular_input(player):
    prompt = f"{player.name}, it is your turn.  You may:\n"
    for number, action in action_key:
        prompt += f'{str(number)}. {action} \n'
    return input(prompt)

@input_validator(range_ = range(2))
def final_input(player):
    prompt = f"{player.name}, it is the last turn in the round.  You may:\n"
    prompt += f'0. {action_key[0]} \n'
    prompt += f'1. {action_key[1]}' 
    return input(prompt)
    
@input_validator(range_ = range(1,7))
def get_card_position():
    return input(f'{choose_position}')

def starting_two_flips(player):
    print(f'{player}, flip your first card.')
    pos_1 = get_card_position()
    print(f'{player}, flip your second card.')
    pos_2 = get_card_position()
    return pos_1, pos_2

def action_parsing(self, player, action):
    
    if action_key[action] == check_score:
        print(self.tally_score(player))
    
    if action_key[action] == draw:
        drawn_card = [card.flip() for card in self.deck.draw()][0]
        print(f"You drew a {drawn_card}.\n Input 0 to discard. Otherwise:\n")
        @input_validator(range_ = 7)
        def keep_or_discard():
            return input(f'You drew a {drawn_card}.\n Input 0 to discard. Otherwise:\n {choose_position}')
        

    

    if action_key[action] == take_discard:
        pos = get_card_position()


    if action_key[action] == flip:
        pos = get_card_position()
        flipped_card = player.hand.cards[pos-1]
        while not flipped_card.hidden:
            print('That card is already revealed.')
            pos = get_card_position()
            flipped_card = player.hand.cards[pos-1]
        else:
            flipped_card.flip()
            print(f'{player} revealed a {flipped_card}')
        print(f"{player}'s' hand is now:")
        player.hand.show()
