"""
File to handle all player input options
Possible player actions:
Check current scores/hand score
Flip a card
Draw a card from the deck
Take the top discarded card
"""


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


def verif_input(prompt, type_=None, min_=None, max_=None, range_=None):
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
                    print(
                        template.format(
                            " or ".join(
                                (", ".join(map(str, range_[:-1])), str(range_[-1]))
                            )
                        )
                    )
        else:
            return ui


def turn_input(self, player, set_up=False, last_turn=False):
    """
    Defines list of options for the player based on current turn:
    Game start only allows card flips, last turn doesn't allow 
    taking from the discard pile.  
    Requests input from prompted list.
    """

    if set_up:
        action = flip
        prompt1 = f"{player}, {flip}.\n{choose_position}"
        prompt2 = "Please choose your second card to flip.\n"
        position = verif_input(prompt1, type_=int, range_=range(1, 7))
        position_2 = verif_input(prompt2, type_=int, range_=range(1, 7))
        return action, [position, position_2], None

    elif last_turn:
        action_list = [draw, check_score]
    else:
        action_list = [flip, draw, take_discard, check_score]

    def prompt_list():
        text = f"{player.name}, it is your turn.  You may:\n"
        for number, letter in enumerate(action_list, 1):
            text += f"{str(number)}. {letter}\n"
        return text

    while True:
        player_choice = verif_input(
            f"{prompt_list()}", type_=int, range_=range(1, len(action_list) + 1)
        )
        action = action_list[player_choice - 1]

        if action == flip or action == take_discard:
            position = verif_input(f"{choose_position}", type_=int, range_=range(1, 7))
            return action, [position], None

        elif action == draw:
            drawn_card = [card.flip() for card in self.deck.draw()][0]
            prompt = f"You drew a {drawn_card}.\n Input 0 to discard. Otherwise:\n"
            position = verif_input(
                prompt + choose_position, type_=int, range_=range(0, 7)
            )
            return action, position, drawn_card

        elif action == check_score:
            print(
                f"Your current known hand is worth {self.tally_score(player)}\n"
                f"The current scores are {self.scoresheet}"
            )


def turn_output(self, player, set_up=False, last_turn=False):

    action, position, drawn_card = turn_input(self, player, set_up, last_turn)

    if action == flip:
        for n in position:
            flipped_card = player.hand.cards[n - 1]
            while not flipped_card.hidden:
                position = verif_input(
                    "That card has already been revealed.\n" + f"{choose_position}",
                    type_=int,
                    range_=range(1, 7),
                )
                flipped_card = player.hand.cards[position - 1]
            else:
                flipped_card.flip()
                print(f"{player} flipped over a {flipped_card}.")

        print(f"{player}'s' hand is now:")
        player.hand.show()

    elif action == take_discard:

        new_card = list(self.discard_pile.draw())[0]
        player.hand.add_card(position[0], new_card)
        old_card = player.hand.remove_card(position[0])
        print(f"{player} took a {new_card} from the discard pile into their hand.")
        self.discard_pile.discard(old_card)
        print(f"{player}'s hand is now:")
        player.hand.show()

    elif action == draw:

        if position == 0:
            self.discard_pile.discard(drawn_card)

            if last_turn:
                for card in player.hand.cards:
                    if card.hidden:
                        card.flip()
                print(
                    "Any remaining face down cards have been revealed.\n"
                    "Your hand is now:"
                )
                player.hand.show()

        else:
            player.hand.add_card(position, drawn_card)
            self.discard_pile.discard(player.hand.remove_card(position))

            if not last_turn:
                print(
                    f"{player} added {drawn_card} into their hand.\n"
                    "Their hand is now:\n"
                )
                player.hand.show()
            else:
                for card in player.hand.cards:
                    if card.hidden:
                        card.flip()
                print(
                    f"{player} added {drawn_card} into their hand.\n"
                    "Any remaining face down cards have been revealed.\n"
                    "Their hand is now:"
                )
                player.hand.show()
