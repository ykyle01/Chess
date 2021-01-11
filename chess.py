import pygame as pg,sys
from pygame.locals import *
import time
import math

#Initialize global variables
white_turn = True
winner = None
draw = False
width = 480
height = 480
white_background = (240,217,181)

#Chess 8*8 board
size = 60
background_board = pg.Surface((size * 8, size * 8))

#Initialize pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height),0,32)
pg.display.set_caption("Chess")

#Load images
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

#Resize images
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

#Classify pieces
white = {w_pawn, w_rook, w_bishop, w_knight, w_king, w_queen}
black = {b_pawn, b_rook, b_bishop, b_knight, b_king, b_queen}

#Set initial board
board = [[b_rook,b_knight,b_bishop,b_queen,b_king,b_bishop,b_knight,b_rook],
        [b_pawn]*8,[None]*8,[None]*8,[None]*8,[None]*8,[w_pawn]*8,
        [w_rook,w_knight,w_bishop,w_queen,w_king,w_bishop,w_knight,w_rook]]

#Handling selected piece - Selection is formatted (piece, row, col)
available_moves = []
selection = (None, -1, -1)

def draw_piece(piece, row, col):
    if piece is not None:
        screen.blit(piece,(col*size,row*size))

def draw_highlight(row, col):
    color = (0,0,0,127)
    center = (col*size+size/2, row*size+size/2)
    radius = 20
    
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    screen.blit(shape_surf, target_rect)

def show_board():
    #Fill and display board
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

def in_bounds(row, col):
    return 0<=row and row<=7 and 0<=col and col<=7

#Handles pawn movement
def get_pawn_moves(piece, row, col, available_moves):
    #White pawn
    direction = -1
    starting_row = 6
    opposite_color = black
    #Black pawn
    if (piece == b_pawn):
        direction = 1
        starting_row = 1
        opposite_color = white
    #Single forward
    if in_bounds(row+direction,col) and board[row+direction][col] is None:
        available_moves.append((row+direction,col))
        #Double forward
        if (row == starting_row and board[row+2*direction][col] is None):
            available_moves.append((row+2*direction,col))
    #Captures (no en passant)
    if in_bounds(row+direction,col-1) and board[row+direction][col-1] in opposite_color:
        available_moves.append((row+direction,col-1))
    if in_bounds(row+direction,col+1) and board[row+direction][col+1] in opposite_color:
        available_moves.append((row+direction,col+1))

#Handles bishop movement
def get_bishop_moves(piece, row, col, available_moves):
    opposite_color = black
    if (piece == b_bishop):
        opposite_color = white
    #Go in each diagonal direction until stopped
    for row_direction, col_direction in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        stop = False
        i = 1
        while not stop:
            row_adjusted = row+i*row_direction
            col_adjusted = col+i*col_direction
            if in_bounds(row_adjusted, col_adjusted):
                if board[row_adjusted][col_adjusted] is None:
                    available_moves.append((row_adjusted, col_adjusted))
                elif board[row_adjusted][col_adjusted] in opposite_color:
                    available_moves.append((row_adjusted,col_adjusted))
                    stop = True
                else:
                    stop = True
            else:
                stop = True
            i = i+1

#Handles rook movement
def get_rook_moves(piece, row, col, available_moves):
    opposite_color = black
    if (piece == b_rook):
        opposite_color = white
    #Go in each horizontal/vertical direction until stopped
    for row_direction,col_direction in [(-1,0),(1,0),(0,-1),(0,1)]:
        stop = False
        i = 1
        while not stop:
            row_adjusted = row+i*row_direction
            col_adjusted = col+i*col_direction
            if in_bounds(row_adjusted, col_adjusted):
                if board[row_adjusted][col_adjusted] is None:
                    available_moves.append((row_adjusted, col_adjusted))
                elif board[row_adjusted][col_adjusted] in opposite_color:
                    available_moves.append((row_adjusted,col_adjusted))
                    stop = True
                else:
                    stop = True
            else:
                stop = True
            i = i+1

#Handles queen movement
def get_queen_moves(piece, row, col, available_moves):
    #Queens are combinations of bishops and rooks
    if piece == w_queen:
        get_bishop_moves(w_bishop, row, col, available_moves)
        get_rook_moves(w_rook, row, col, available_moves)
    elif piece == b_queen:
        get_bishop_moves(b_bishop, row, col, available_moves)
        get_rook_moves(b_rook, row, col, available_moves)

#Finds all possible moves for a given piece in a given position
def get_available_moves(piece, row, col):
    available_moves = []
    if (piece == w_pawn or piece == b_pawn):
        get_pawn_moves(piece, row, col, available_moves)
    elif (piece == w_bishop or piece == b_bishop):
        get_bishop_moves(piece, row, col, available_moves)
    elif (piece == w_rook or piece == b_rook):
        get_rook_moves(piece, row, col, available_moves)
    elif (piece == w_queen or piece == b_queen):
        get_queen_moves(piece, row, col, available_moves)
    return available_moves

#Draws the highlights for all available moves
def highlight_available_moves(available_moves):
    for row, col in available_moves:
        draw_highlight(row,col)

def userClick():
    #Get coordinates of mouse click
    x,y = pg.mouse.get_pos()
    col = math.trunc(x/size)
    row = math.trunc(y/size)
    piece = board[row][col]

    #Operates based on piece color and turn
    global available_moves
    global selection
    global white_turn

    #White choosing piece to move
    if white_turn and piece in white:
        show_board()
        available_moves = get_available_moves(piece, row, col)
        highlight_available_moves(available_moves)
        selection = (piece, row, col)
    #Black choosing piece to move
    elif not white_turn and piece in black:
        show_board()
        available_moves = get_available_moves(piece, row, col)
        highlight_available_moves(available_moves)
        selection = (piece, row, col)
    #Make move
    elif (row,col) in available_moves:
        board[row][col] = selection[0]
        board[selection[1]][selection[2]] = None
        selection = (None, -1, -1)
        show_board()
        available_moves = []
        white_turn = not white_turn
    #Cancel selection
    elif board[row][col] is None:
        available_moves = []
        selection = (None, -1, -1)
        show_board()

show_board()

#Run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            userClick()

    pg.display.update()
    CLOCK.tick(fps)