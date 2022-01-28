"""
Define game logic for 5x5 Tic Tac Toe

This module defines the model for the game and handles logic for placing new
tokens on the board, checking for a winner, and saving/loading each game's 
history to a file called "games.log".

Game history is intended be used to train a neural network AI opponent.
"""

# -------------------------------- Imports -------------------------------------
from itertools import product   # To iterate over the board
# ------------------------------------------------------------------------------

# Variables
# Game board representation (5x5 list of zeros)
board = [[0 for j in range(5)] for i in range(5)]

# Count occupied spaces
used_squares = 0

# Game over status
game_over = False

# 0: no winner, 1: X wins, 2: O wins
winner = 0

# Winning row coordinates
# If winner is found, 4 (x, y) tuples are appended to this list
winning_row = []

# Board history for the current game
# Updates each time a token is placed
# Board history is stored in condensed format
board_history = []


"""
Places a token on the board and updates the state of the game

Parameters:
placed_token (int): 0 = empty square, 1 = 'X', 2 = 'O'
token_x (int):      Row that the token is placed in
token_y (int):      Column that the token is placed in
"""
def place_token(placed_token, token_x, token_y):
    global used_squares
    # Place the token onto the board and record it in this game's history
    board[token_x][token_y] = placed_token
    used_squares += 1 # Increment the number of used spaces on the board
    record_board()
    # Check if a player has won or the game ends in a tie
    if used_squares > 6: # Optimization - impossible to win before turn 7
        update_game_state() # Check for endgame conditions


"""
Place a token to the game board and check for endgame conditions
Does no error checking -- relies on controller to provide error-free values
"""
def update_game_state():
    global game_over, winner, board

    # ------------------ Algorithm to check for game winner --------------------

    # For each square of the game board
    for x, y in product(range(5), range(5)):

        token = board[x][y] # Get token at that square

        if token != 0: # If square is occupied
            # Iterate through surrounding squares
            for i, j in product(range(-1, 2), range(-1, 2)):

                if i == 0 and j == 0:   # Skip self
                    continue

                # Skip out of bounds squares
                if (x + i) > 4 or (x + i) < 0:
                    continue
                if (y + j) > 4 or (y + j) < 0:
                    continue
            
                # If matching token is found
                if board[x+i][y+j] == token:
                    
                    fourinarow = True   # Assume winning row of tokens

                    # Repeat search in the same direction 2 more times
                    for k in range(2, 4):
                        # Ensure that next square in line is in bounds
                        # If not, can't be four in a row
                        if (x + (k*i)) > 4 or (x + (k*i)) < 0:
                            fourinarow = False
                            continue
                        if (y + (k*j)) > 4 or (y + (k*j)) < 0:
                            fourinarow = False
                            continue

                        # If next token in line is not a match
                        if board[x + (k*i)] [y + (k*j)] != token:
                            # Mark as non-winner and move on
                            fourinarow = False
                            continue

                    # If four in a row were found, assign winner and end game
                    if fourinarow:
                        game_over = True
                        winner = token

                        # Save coordinates of winning row
                        for k in range(4):
                            winning_row.append( (x + (k*i), (y + (k*j)) ))

                        # Save the compressed history of the finished game
                        record_game()
                        
                        return # Stop here

    # If no winner was found but board is full
    if used_squares >= 25:
        game_over = True # gg
# end update_game_state()


"""
Handle game reset logic
"""
def reset():
    global board, used_squares, winner, winning_row, game_over, board_history
    
    # Re-initialize board to all zeros
    board = [[0 for j in range(5)] for i in range(5)]
    
    # Reset occupied spaces count to 0
    used_squares = 0

    # Reset winner to 0 (no winner)
    winner = 0

    # Reset winning row to empty list
    winning_row = []

    # Reset endgame status
    game_over = False

    # Reset game history
    board_history = []


"""
Condense the current state of the game board and append it to an list
"""
def record_board():
    # Condensed representation
    # 25 values (one for each square), empty = 0, 'X' = 1, 'O' = 2
    board_data = [token for row in board for token in row]
    # Append condensed representation to list
    board_history.append(board_data)


"""
Convert the game history into a string and save it to a file
String representation is "{winner},{game_state_1},{game_state_2},..."
"""
def record_game():
    # Build string representation
    # 25 characters (one for each square), 0 = empty, 1 = 'X', 2 = 'O'
    condensed_history = [] # Empty list (will contain strings)
    
    # Iterate through game states
    for i, state in enumerate(board_history):
        condensed_history.append('')   # Initialize list element to empty string
        for square in state:           # For each board square in current state
            condensed_history[i] += str(square)  # Append character rep of token

    # Convert list of strings to single comma separated string
    condensed_history = ','.join(condensed_history)

    # Save winner, then csv list of game states
    with open("games.log", 'a') as f:
        f.write(f"{winner},{condensed_history}\n")


"""
Load board from the condensed string representation

Parameters:
str_rep (string): The string representation the state of the board
"""
def load_board(str_rep):
    global board, used_squares
    
    # Iterate through each space in the board
    for i, j in product(range(5), range(5)):
        token = str_rep[i*5 + j]    # Calculate index of token at current square
        board[i][j] = token         # Update square with appropriate token
        if token != 0:              # If current square is occupied
            used_squares += 1        # Increment occupied squares count

    # Check for endgame conditions in loaded board state
    update_game_state()
