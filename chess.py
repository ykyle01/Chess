import pygame as pg,sys
from pygame.locals import *
import time
import math

#Initialize global variables
BW = "w"
winner = None
draw = False
width = 480
height = 480
white = (240,217,181)

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

#Resize images
w_pawn = pg.transform.scale(w_pawn, (size, size))
w_rook = pg.transform.scale(w_rook, (size, size))
w_bishop = pg.transform.scale(w_bishop, (size, size))
w_knight = pg.transform.scale(w_knight, (size, size))
w_king = pg.transform.scale(w_king, (size, size))
w_queen = pg.transform.scale(w_queen, (size, size))

#Set initial board
board = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[w_pawn]*8,[w_rook,w_knight,w_bishop,w_queen,w_king,w_bishop,w_knight,w_rook]]

def draw_piece(piece, row, col):
    if piece is not None:
        screen.blit(piece,(col*size,row*size))

def show_board():
    #Fill and display board
    background_board.fill(white)
    for x in range(0,8,1):
        for y in range(0,8,1):
            if ((x+y)%2 == 1):
                pg.draw.rect(background_board, (148,111,81), (x*size, y*size, size, size))
    screen.blit(background_board, background_board.get_rect())

    for row in range(0,8,1):
        for col in range(0,8,1):
            piece = board[row][col]
            draw_piece(piece, row, col)

def userClick():
    #Get coordinates of mouse click
    x,y = pg.mouse.get_pos()
    col = math.trunc(x/size)
    row = math.trunc(y/size)
    
    #Testing coordinate
    board[row][col] = w_pawn
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
