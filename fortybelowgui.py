from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
#WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class FortyBelowUI(Frame):
    """
    Using Tkinter UI to set the table for the game and represent input/output 
    from player
    """
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0
        
        def __initUI(self):
            self.parent.title('FortyBelow')
            self.pack(fill=BOTH, expand=1)