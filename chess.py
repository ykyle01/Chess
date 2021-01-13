import pygame as pg,sys
from pygame.locals import *
import time
import math

# Initialize global variables
white_turn = True
winner = None
stalemate = False
width = 480
height = 480
white_background = (240,217,181)

# Castling global variables - turns false if associated king or rook moves
w_kingside = True
w_queenside = True
b_kingside = True
b_queenside = True

# Chess 8*8 board
size = 60
background_board = pg.Surface((size * 8, size * 8))

# Initialize pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100),0,32)
pg.display.set_caption("Chess")

# Load images
w_pawn = pg.image.load('images/Chess_plt60.png')
w_rook = pg.image.load('images/Chess_rlt60.png')
w_bishop = pg.image.load('images/Chess_blt60.png')
w_knight = pg.image.load('images/Chess_nlt60.png')
w_king = pg.image.load('images/Chess_klt60.png')
w_queen = pg.image.load('images/Chess_qlt60.png')
b_pawn = pg.image.load('images/Chess_pdt60.png')
b_rook = pg.image.load('images/Chess_rdt60.png')
b_bishop = pg.image.load('images/Chess_bdt60.png')
b_knight = pg.image.load('images/Chess_ndt60.png')
b_king = pg.image.load('images/Chess_kdt60.png')
b_queen = pg.image.load('images/Chess_qdt60.png')

# Resize images
w_pawn = pg.transform.scale(w_pawn, (size, size))
w_rook = pg.transform.scale(w_rook, (size, size))
w_bishop = pg.transform.scale(w_bishop, (size, size))
w_knight = pg.transform.scale(w_knight, (size, size))
w_king = pg.transform.scale(w_king, (size, size))
w_queen = pg.transform.scale(w_queen, (size, size))
b_pawn = pg.transform.scale(b_pawn, (size, size))
b_rook = pg.transform.scale(b_rook, (size, size))
b_bishop = pg.transform.scale(b_bishop, (size, size))
b_knight = pg.transform.scale(b_knight, (size, size))
b_king = pg.transform.scale(b_king, (size, size))
b_queen = pg.transform.scale(b_queen, (size, size))

# Gets piece name from piece
def get_piece_name(piece):
    output = "Unfound"
    if piece == w_pawn:
        output = "White pawn"
    elif piece == w_rook:
        output = "White rook"
    elif piece == w_bishop:
        output = "White bishop"
    elif piece == w_knight:
        output = "White knight"
    elif piece == w_king:
        output = "White king"
    elif piece == w_queen:
        output = "White queen"
    elif piece == b_pawn:
        output = "Black pawn"
    elif piece == b_rook:
        output = "Black rook"
    elif piece == b_bishop:
        output = "Black bishop"
    elif piece == b_knight:
        output = "Black knight"
    elif piece == b_king:
        output = "Black king"
    elif piece == b_queen:
        output = "Black queen"
    return output

# Classify pieces
white = {w_pawn, w_rook, w_bishop, w_knight, w_king, w_queen}
black = {b_pawn, b_rook, b_bishop, b_knight, b_king, b_queen}

# Set initial board
board = [[b_rook,b_knight,b_bishop,b_queen,b_king,b_bishop,b_knight,b_rook],
        [b_pawn]*8,[None]*8,[None]*8,[None]*8,[None]*8,[w_pawn]*8,
        [w_rook,w_knight,w_bishop,w_queen,w_king,w_bishop,w_knight,w_rook]]

# Handling selected piece - Selection is formatted (piece, row, col)
available_moves = []
selection = (None, -1, -1)

# Draws the piece at the row and col - does nothing if piece is None
def draw_piece(piece, row, col):
    if piece is not None:
        screen.blit(piece,(col*size,row*size))

# Draws a translucent highlight of a given color at the row and col
def draw_highlight(color, row, col):
    center = (col*size+size/2, row*size+size/2)
    radius = 20
    
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    screen.blit(shape_surf, target_rect)

# Draws the background board and all the pieces
def show_board():
    # Fill and display board
    background_board.fill(white_background)
    for x in range(0,8,1):
        for y in range(0,8,1):
            if ((x+y)%2 == 1):
                pg.draw.rect(background_board, (148,111,81), (x*size, y*size, size, size))
    screen.blit(background_board, background_board.get_rect())

    for row in range(0,8,1):
        for col in range(0,8,1):
            piece = board[row][col]
            draw_piece(piece, row, col)

# Gets all available moves for a color
def all_available_moves(color):
    global selection
    output = []
    temp = selection
    for row in range(0,8,1):
        for col in range(0,8,1):
            piece = board[row][col]
            if (piece in color):
                selection = (piece, row, col)
                moves = get_available_moves(board, piece, row, col, True)
                output.extend(moves)
    selection = temp
    return output

# Returns whether a position is reachable by an opponent's piece
def opposite_reachable(used_board, position):
    opposite_color = black
    if not white_turn:
        opposite_color = white
    for row in range(0,8,1):
        for col in range(0,8,1):
            piece = used_board[row][col]
            if (piece in opposite_color):
                moves = get_available_moves(used_board, piece, row, col, False) 
                if (position in moves):
                    return True
    return False

# Ensures player cannot make a move that goes into check
def king_checked(used_board):
    color = white
    king_position = (-1,-1)
    if not white_turn:
        color = black
    # Finds corresponding king
    for row in range(0,8,1):
        for col in range(0,8,1):
            piece = used_board[row][col]
            if (color == white and piece == w_king) or (color == black and piece == b_king):
                king_position = (row,col)
    return opposite_reachable(used_board, king_position)

def legal_move(row, col):
    hypothetical_board = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]
    for i in range(0,8,1):
        hypothetical_board[i] = board[i].copy()
    make_move(hypothetical_board, row, col)
    return not king_checked(hypothetical_board)

def in_bounds(row, col):
    return 0<=row and row<=7 and 0<=col and col<=7

def check_bounds_legality(used_board, row, col, opposite_color, legal_check):
    return in_bounds(row,col) and (not legal_check or legal_move(row,col))

# Handles pawn movement
def get_pawn_moves(used_board, piece, row, col, available_moves, legal_check):
    # White pawn
    direction = -1
    starting_row = 6
    opposite_color = black
    # Black pawn
    if (piece == b_pawn):
        direction = 1
        starting_row = 1
        opposite_color = white
    # Single forward
    if check_bounds_legality(used_board, row+direction, col, opposite_color, legal_check) and used_board[row+direction][col] is None:
        available_moves.append((row+direction,col))
        # Double forward
        if (row == starting_row and check_bounds_legality(used_board, row+2*direction, col, opposite_color, legal_check) and used_board[row+2*direction][col] is None):
            available_moves.append((row+2*direction,col)) 
    # Captures (no en passant)
    if check_bounds_legality(used_board, row+direction, col-1, opposite_color, legal_check) and used_board[row+direction][col-1] in opposite_color:
        available_moves.append((row+direction,col-1))
    if check_bounds_legality(used_board, row+direction, col+1, opposite_color, legal_check) and used_board[row+direction][col+1] in opposite_color:
        available_moves.append((row+direction,col+1))

# Goes in a direction until stopped
def go_direction(used_board, row, col, opposite_color, row_direction, col_direction, available_moves, stop_at_one, legal_check):
    color = white
    if opposite_color == white:
        color = black
    stop = False
    i = 1
    while not stop:
        row_adjusted = row+i*row_direction
        col_adjusted = col+i*col_direction
        if not in_bounds(row_adjusted, col_adjusted) or used_board[row_adjusted][col_adjusted] in color:
            break
        if (not legal_check or legal_move(row_adjusted, col_adjusted)):
            if used_board[row_adjusted][col_adjusted] is None:
                available_moves.append((row_adjusted, col_adjusted))
            elif used_board[row_adjusted][col_adjusted] in opposite_color:
                available_moves.append((row_adjusted, col_adjusted))
                stop = True
            else:
                stop = True
        if stop_at_one:
            stop = True
        i = i+1

# Handles bishop movement
def get_bishop_moves(used_board, piece, row, col, available_moves, stop_at_one, legal_check):
    opposite_color = black
    if (piece == b_bishop):
        opposite_color = white
    # Go in each diagonal direction until stopped
    for row_direction, col_direction in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        go_direction(used_board, row, col, opposite_color, row_direction, col_direction, available_moves, stop_at_one, legal_check)

# Handles rook movement
def get_rook_moves(used_board, piece, row, col, available_moves, stop_at_one, legal_check):
    opposite_color = black
    if (piece == b_rook):
        opposite_color = white
    # Go in each horizontal/vertical direction until stopped
    for row_direction, col_direction in [(-1,0),(1,0),(0,-1),(0,1)]:
        go_direction(used_board, row, col, opposite_color, row_direction, col_direction, available_moves, stop_at_one, legal_check)

# Handles queen movement
def get_queen_moves(used_board, piece, row, col, available_moves, stop_at_one, legal_check):
    # Queens are combinations of bishops and rooks
    if piece == w_queen:
        get_bishop_moves(used_board, w_bishop, row, col, available_moves, stop_at_one, legal_check)
        get_rook_moves(used_board, w_rook, row, col, available_moves, stop_at_one, legal_check)
    elif piece == b_queen:
        get_bishop_moves(used_board, b_bishop, row, col, available_moves, stop_at_one, legal_check)
        get_rook_moves(used_board, b_rook, row, col, available_moves, stop_at_one, legal_check)

# Helper function for castling to check squares are unattacked and empty
def check_between(used_board, range):
    for row, col in range:
        # Check empty
        if used_board[row][col] is not None:
            return False
        # Checks not attacked
        if opposite_reachable(used_board, (row,col)):
            return False
    return True

# Checks castling
def check_castling(used_board, castle):
    if castle == "w_kingside":
        return w_kingside and not king_checked(used_board) and check_between(used_board, [(7,5),(7,6)])
    elif castle == "w_queenside":
        return w_queenside and not king_checked(used_board) and check_between(used_board, [(7,1),(7,2),(7,3)])
    elif castle == "b_kingside":
        return b_kingside and not king_checked(used_board) and check_between(used_board, [(0,5),(0,6)])
    elif castle == "b_queenside":
        return b_queenside and not king_checked(used_board) and check_between(used_board, [(0,1),(0,2),(0,3)])
    
# Handles king movement
def get_king_moves(used_board, piece, row, col, available_moves, legal_check):
    # Kings are queens that can only move one square
    if piece == w_king:
        get_queen_moves(used_board, w_queen, row, col, available_moves, True, legal_check)
        if not legal_check or check_castling(used_board, "w_kingside"):
            available_moves.append((7,6))
        if not legal_check or check_castling(used_board, "w_queenside"):
            available_moves.append((7,2))
    elif piece == b_king:
        get_queen_moves(used_board, b_queen, row, col, available_moves, True, legal_check)
        if not legal_check or check_castling(used_board, "b_kingside"):
            available_moves.append((0,6))
        if not legal_check or check_castling(used_board, "b_queenside"):
            available_moves.append((0,2))

# Handles knight movement
def get_knight_moves(used_board, piece, row, col, available_moves, legal_check):
    opposite_color = black
    if (piece == b_knight):
        opposite_color = white
    for row_direction, col_direction in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        go_direction(used_board, row, col, opposite_color, row_direction, col_direction, available_moves, True, legal_check)

# Finds all possible moves for a given piece in a given position
def get_available_moves(used_board, piece, row, col, legal_check):
    available_moves = []
    if (piece == w_pawn or piece == b_pawn):
        get_pawn_moves(used_board, piece, row, col, available_moves, legal_check)
    elif (piece == w_bishop or piece == b_bishop):
        get_bishop_moves(used_board, piece, row, col, available_moves, False, legal_check)
    elif (piece == w_rook or piece == b_rook):
        get_rook_moves(used_board, piece, row, col, available_moves, False, legal_check)
    elif (piece == w_queen or piece == b_queen):
        get_queen_moves(used_board, piece, row, col, available_moves, False, legal_check)
    elif (piece == w_king or piece == b_king):
        get_king_moves(used_board, piece, row, col, available_moves, legal_check)
    elif (piece == w_knight or piece == b_knight):
        get_knight_moves(used_board, piece, row, col, available_moves, legal_check)
    return available_moves

# Draws the highlights for all available moves
def highlight_available_moves(available_moves):
    for row, col in available_moves:
        draw_highlight((0,0,0,127), row,col)

# Makes a move on a given board
def make_move(used_board, row, col):
    used_board[row][col] = selection[0]
    used_board[selection[1]][selection[2]] = None
    

def userClick():
    # Get coordinates of mouse click
    x,y = pg.mouse.get_pos()
    col = math.trunc(x/size)
    row = math.trunc(y/size)
    piece = board[row][col]

    # Operates based on piece color and turn
    global available_moves
    global selection
    global white_turn

    # Choosing piece to move
    if (white_turn and piece in white) or (not white_turn and piece in black):
        show_board()
        draw_highlight((0,255,255,127),row,col)
        selection = (piece, row, col)
        available_moves = get_available_moves(board, piece, row, col, True)
        highlight_available_moves(available_moves)
    # Make move
    elif (row,col) in available_moves:
        make_move(board, row, col)
        selection = (None, -1, -1)
        show_board()
        available_moves = []
        white_turn = not white_turn
        check_win()
    # Cancel selection
    elif board[row][col] is None:
        available_moves = []
        selection = (None, -1, -1)
        show_board()

# Checks for checkmate and stalemate
def check_win():
    global winner
    global stalemate
    if white_turn:
        all_moves = all_available_moves(white)
        if not all_moves:
            if king_checked(board):
                winner = black
            else:
                stalemate = True
    else:
        all_moves = all_available_moves(black)
        if not all_moves:
            if king_checked(board):
                winner = white
            else:
                stalemate = True
    game_status()

# Prints which color to move, stalemate, or winner
def game_status():
    if winner is None:
        if white_turn:
            message = "White's Turn to Move"
        else:
            message = "Black's Turn to Move"
    else:
        if winner is white:
            message = "White won!"
        else:
            message = "Black won!"
    if stalemate:
        message = "Stalemate"
    
    screen.fill ((0, 0, 0), (0, 480, 480, 100))
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # Copy the rendered message onto the board
    text_rect = text.get_rect(center=(width/2, 580-50))
    screen.blit(text, text_rect)
    pg.display.update()

show_board()
game_status()

# Run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            userClick()

    pg.display.update()
    CLOCK.tick(fps)