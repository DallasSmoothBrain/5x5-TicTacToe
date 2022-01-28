""" 
A simple tkinter GUI for 5x5 Tic Tac Toe
    
This module acts as both view and controller module for the model defined
in game_logic.py.
"""

# -------------------------------- Imports -------------------------------------
try:
    import tkinter as tk        # Python 3.x module name
except:
    import Tkinter as tk        # Python 2.x module name

from itertools import product   # To iterate over the board

import game_logic               # Handle game state, winning, etc
# ------------------------------------------------------------------------------

# Variables
g_starting_token = 'X'          # Hard-coded starting player


"""
Defines the game window and handles board interactions
"""
class GameWindow (tk.Tk):

    """
    Initialize GUI window settings and create grid for game board
    """
    def __init__(self):
        super().__init__()

        # Window configuration settings
        self.title("5x5 Tic-Tac-Toe")
        self.iconphoto(False, tk.PhotoImage(file='res/xo.png'))
        self.resizable(False, False)
        self.configure(bg="#222227")

        # Value switches from 'O' to 'X' every time a token is placed
        self.player_token = g_starting_token

        # Initialize tkinter frames
        self.frm_top = tk.Frame(self)                   # Top info frame
        self.frm_board = tk.Frame(self)                 # Central board frame
        self.frm_bottom = tk.Frame(self, bg='#222227')  # Bottom controls frame
        self.frm_bottom.rowconfigure(0, minsize=60)     # Sets height of frame

        # Position frames vertically
        self.frm_top.grid(row=0)
        self.frm_board.grid(row=1)
        self.frm_bottom.grid(row=2)

        # Create info label
        self.lbl_top = tk.Label(
            self.frm_top,                               # In top frame
            text = f"{self.player_token}'s turn",       # "X's turn"
            justify = 'center',                         # Center label in frame
            width = 10,                                 # Fix width
            pady = 15,                                  # Give label some space
            font = ('Berlin Sans FB Demi', 20, 'bold'), # A fancy font
            background = "#222227",                     # Blueish-black
            foreground = 'white'                        # White text
        )

        # Create restart button
        self.btn_restart = tk.Button(                   
            self.frm_bottom,                            # In bottom frame
            command = self.restart,                     # Set callback method
            text = "Restart",                           # Button text
            width = 8,                                  # Fix width
            height = 1,                                 # Fix height
            font = ('Helvetica', 12),                   # Another fancy font
            background = "#444444",                     # Grey button
            foreground = 'white',                       # White text
            activebackground = "#111111",               # Darker when clicked
            activeforeground = 'white'                  # White text still
        )
        
        # Position GUI elements
        self.lbl_top.grid(sticky='ew')      # Center the info label in top frame
        self.btn_restart.grid(sticky='e')   # Put restart button in bottom frame

        # ------------------------- Board creation -----------------------------
        # Create 2D list of 5 rows, each containing [0, 1, 2, 3, 4]
        self.board_squares = [[j for j in range(5)] for i in range(5)]
        
        # Iterate through each entry in the list
        for x, y in product(range(5), range(5)):

            # Represent each square on the board as a button
            self.board_squares[x][y] = tk.Button(
                self.frm_board,                         # In board frame
                name = f'{x}{y}',                       # For element access
                width = 4,                              # Fix width
                height = 1,                             # Font size dependant
                font = ('Tempus Sans ITC', 30, 'bold')  # One more fancy font
            )

            # Position the square appropriately
            self.board_squares[x][y].grid(row=x, column=y, sticky='w')

            # Bind callback method for each button
            self.board_squares[x][y].bind('<Button-1>', self.place_token)
    # end __init__()


    """
    Update the board display and handle game logic
    """
    def place_token(self, event):

        # Ensure that game is not over
        if game_logic.game_over:
            return

        # Get reference to button
        square = event.widget

        # Ensure that space is empty
        if square['text']: 
            return # Return if text is not empty string

        # retrieve x and y location from name of widget
        x = int(str(square)[9])
        y = int(str(square)[10])

        # Update board display
        square.configure(text=self.player_token)

        # Convert placed token to game_logic module's representation
        token_code = 1 if self.player_token == 'X' else 2
        game_logic.place_token(token_code, x, y)    # Update game logic

        # Check and react to game over flag
        if game_logic.game_over:
            # Assume tie initially
            status_text = 'Tie!'

            # Check winner
            if game_logic.winner == 1:
                status_text = 'X wins!'
            elif game_logic.winner == 2:
                status_text = 'O wins!'

            # Update top info label text
            self.lbl_top['text'] = status_text

            # Highlight the winning row in the board display
            self.highlight_row()

        else: # Game is not over
            # Switch player turns
            self.player_token = 'X' if self.player_token == 'O' else 'O'
            # Update top info label text
            self.lbl_top['text'] = f"{self.player_token}'s turn"
    # end place_token()


    """
    Highlight the winning row in the board display
    """
    def highlight_row(self):
        # Set color based on winner
        color = 'black'     # No color change if tie
        if game_logic.winner == 1:
            color = 'red'   # If X wins
        elif game_logic.winner == 2:
            color = 'blue'  # If O wins

        # Iterate through the squares that contain the winning tokens
        for x, y in game_logic.winning_row:
            self.board_squares[x][y].configure(fg=color)    # Update text color


    """
    Handle game restart
    """
    def restart(self):
        # Clear all squares and reset colors
        for x, y in product(range(5), range(5)):
            self.board_squares[x][y]['text'] = ''
            self.board_squares[x][y]['fg'] = 'black'

        # Reset game logic
        game_logic.reset()

        # Reset turn to hard-coded starting player
        self.player_token = g_starting_token

        # Reset top info label text
        self.lbl_top['text'] = f"{self.player_token}'s turn"
# end class GameWindow

window = GameWindow()   # Create instance of tkinter window
window.mainloop()       # Run program
