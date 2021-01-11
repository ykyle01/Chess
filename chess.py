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

#Finds all possible moves for a given piece in a given position
def get_available_moves(piece, row, col):
    available_moves = []
    #Handles white and black pawn movement
    if (piece == w_pawn or piece == b_pawn):
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
        if board[row+direction][col] is None:
            available_moves.append((row+direction,col))
            #Double forward
            if (row == starting_row and board[row+2*direction][col] is None):
                available_moves.append((row+2*direction,col))
        #Captures (no en passant)
        if board[row+direction][col-1] in opposite_color:
            available_moves.append((row+direction,col-1))
        if board[row+direction][col+1] in opposite_color:
            available_moves.append((row+direction,col+1))
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
