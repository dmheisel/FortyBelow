"""
File to handle all player input options
Possible player actions:
Check current scores/hand score
Flip a card
Draw a card from the deck
Take the top discarded card
"""

def input_validator(range_ = None, acceptable_chars = None):
    """
    Decorator function used to validate user input.  If range is specified, checks if input is an int within the range.  Otherwise will check if input is contained within list of acceptable characters
    """
    def validating(func):
        def validated(*args, **kwargs):
            while True:
                ui = func(*args, **kwargs)
                if range_:
                    try:
                        ui = int(ui)
                    except ValueError:
                        print("please input a valid number.")
                        continue
                    if ui not in range_:
                        print(f'Input a valid number betwen {range_.start} and {range_.stop-1}')
                        continue
                if acceptable_chars and ui.lower() not in acceptable_chars:
                    print(f"Valid inputs are {' and '.join(acceptable_chars)}.  Please retry.")
                    continue
                else:
                    return ui
        return validated
    return validating



flip = "Flip a card in your hand."
draw = "Draw a card from the deck."
take_discard = "Take the top card from the the discard pile."
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
def regular_input(self, player):
    prompt = f"You may:\n"
    for number, action in action_key.items():
        prompt += f'{str(number)}. {action} \n'
    return input(prompt)

@input_validator(range_ = range(2))
def final_input(self, player):
    prompt = f"It is the last turn in the round.  You may:\n"
    prompt += f'0. {action_key[0]} \n'
    prompt += f'1. {action_key[1]}'
    #index = int(input(prompt))
    #while action_key[index] == check_score:
    #    print(
    #        f"{player}'s current hand is worth #{self.tally_score(player)}\n"
   #         f"The scoreboard is: {self.scoresheet}"
   #         )
   #     index = int(input(prompt))
    return input(prompt)
    
@input_validator(range_ = range(1,7))
def get_card_position():
    return input(f'{choose_position}')

@input_validator(acceptable_chars = ['y', 'n'])
def keep_or_discard(card):
    return input(f"You drew a {card}. \nDo you wish to keep it?\nInput 'y' for Yes, 'n' for No\n")

def starting_two_flips(player):
    print(f'{player}, flip your first card.')
    pos_1 = get_card_position()-1
    print(f'{player}, flip your second card.')
    pos_2 = get_card_position()-1
    while pos_2 == pos_1:
        print('You have already chosen that card: \n')
        pos_2 = get_card_position()-1
    for pos in [pos_1, pos_2]:
        player.hand.cards[pos].flip()
    print(f"{player}'s hand is now:\n")
    player.hand.show()

def turn(self, player, is_last =  False):
    print(
        f'The discard pile currently shows {self.discard_pile.card_list[0]}.\n'
        f'{player}, your hand is:'
        )
    player.hand.show()

    if is_last:
        action = action_key[final_input(self, player)]
        while action == check_score:
            print(
            f"{player}'s current hand is worth {self.tally_score(player)}\n"
            f"The scoreboard is: {self.scoresheet}"
            )
            action = action_key[final_input(self, player)]
    else:
        action = action_key[regular_input(self, player)]
        while action == check_score:
            print(
            f"{player}'s current hand is worth {self.tally_score(player)}\n"
            f"The scoreboard is: {self.scoresheet}"
            )
            action = action_key[regular_input(self, player)]


    if action == flip:
        flipped_card = player.hand.cards[get_card_position()-1]
        while not flipped_card.hidden:
            print("That card is already revealed.")
            flipped_card = player.hand.cards[get_card_position()-1]
        flipped_card.flip()
        print(f'{player} revealed {flipped_card}.  Their hand is now:')
        player.hand.show() 
        
    if action == draw:
        drawn_card = [card.flip() for card in self.deck.draw()][0]
        follow_up = keep_or_discard(drawn_card)
        if follow_up.lower() == 'n': 
            self.discard_pile.discard(drawn_card)
        else:
            pos = get_card_position()
            player.hand.add_card(pos, drawn_card)
            self.discard_pile.discard(player.hand.remove_card(pos))
            print(
                f"{player} added {drawn_card} into their hand.\n"
                "Their hand is now:\n"
                )
            player.hand.show()
                
    if action == take_discard:
        new_card = list(self.discard_pile.draw())[0]
        pos = get_card_position()
        player.hand.add_card(pos, new_card)
        old_card = player.hand.remove_card(pos)
        print(f"{player} took a {new_card} from the discard pile into their hand.")
        self.discard_pile.discard(old_card)
        print(f"{player}'s hand is now:")
        player.hand.show()

    if is_last:
        for card in player.hand.cards:
            card.flip()
        print("All cards are now revealed. \n"
               "Your hand is now:")
        player.hand.show()
