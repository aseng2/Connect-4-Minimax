import numpy
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER1_TURN = 0
PLAYER2_TURN = 1

PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

# Create board
def create_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Drop the Piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Checks if the col is free
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Get the open row
def get_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Prints the game board
def print_board(board):
    flipped_board = numpy.flip(board, 0)
    rows, cols = flipped_board.shape

    flipped_board = flipped_board.astype(int)

    for i in range(rows):
        print("|", end="")
        for j in range(cols):
            print(f"{flipped_board[i,j]:2}", end = " |")
        print()
    print("-" * (cols*4))

    print("|", end= "")
    for j in range(cols):
        print(f"{j}", end= " | ")

# Function for checking if the player is going to win
def winning_move(board, piece):
    # Horizontal Win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # Vertical Win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # Postive diagonal Win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # Negative diagonal Win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Get what location is valid to place piece
def get_valid_locations(board):
    valid_locations = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, PLAYER1_PIECE) or winning_move(board, PLAYER2_PIECE) or len(get_valid_locations(board)) == 0

def score_position(board, piece):
    score = 0
    center_array = [int(board[r][COLUMN_COUNT//2]) for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(board[r][c]) for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER1_PIECE if piece == PLAYER2_PIECE else PLAYER2_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER2_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER1_PIECE):
                return (None, -10000000000000)
            else: # No more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, PLAYER2_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER2_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER1_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Create empty board
board = create_board()

# Game State
game_over = False
turn = 0 #Player 1 starts first

print_board(board)
print("\n")

# Game Loop
while not game_over:
    if turn % 2 == PLAYER1_TURN:
        col = int(input("Player 1 Make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_open_row(board, col)
            drop_piece(board, row, col, PLAYER1_PIECE)

            if winning_move(board, PLAYER1_PIECE):
                print("Player 1 win, congratulations!")
                game_over = True 
                print_board(board)
                break
        
        print_board(board)
        print("\n")
        turn +=1

    #This will turn into the AI 
    # if turn % 2 == PLAYER2_TURN and not game_over:
    #     col = int(input("Player 2 Make your selection (0-6): "))
    #     if is_valid_location(board, col):
    #         row = get_open_row(board, col)
    #         drop_piece(board, row, col, PLAYER2_PIECE)

    #         if winning_move(board, PLAYER2_PIECE):
    #             print("Player 2 win, congratulations!")
    #             game_over = True 
    #             print_board(board)
    #             break
    else:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_open_row(board, col)
            drop_piece(board, row, col, PLAYER2_PIECE)

            if winning_move(board, PLAYER2_PIECE):
                print("AI wins!")
                game_over = True
                break
        
        print_board(board)
        print("\n")
        turn +=1