import pygame, sys
import numpy as np
from tkinter import *
from tkinter import messagebox

# initializes pygame
pygame.font.init()
Tk().wm_withdraw()

'''
# Network
client = None
HOST_IP = "localhost"
HOST_PORT = 6060
'''

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (243, 196, 196)
LINE_COLOR = (185, 69, 69)
CIRCLE_COLOR = (66, 66, 66)
CROSS_COLOR = (210, 176, 115)

#สร้าง gui
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'Client' )
screen.fill( BG_COLOR )

messagebox.showinfo('Info','Player 1 started first')

#อาเรย์ 3D ของบอร์ด
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

#funtion
def draw_lines():
	#แนวนอน
	pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

	#แนวตั้ง
	pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
	pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

def draw_figures():
#ใช้สำหรับวาดรูปลงในช่อง
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
                        #O
			if board[row][col] == 1:
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
                        #X
			elif board[row][col] == 2:
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
#กำหนดค่าลงในอาเรย์
#อาเรย์ 3d ที่ได้จากไลบรารี่ numpy
#{ 0 , 0 , 0 }
#{ 0 , 0 , 0 }
#{ 0 , 0 , 0 }
#0 แทน ช่องว่าง
#1 แทน ผู้เล่น 1 , 2 แทน ผู้เล่น 2
	board[row][col] = player
def available_square(row, col):
	return board[row][col] == 0

def check_board_full():
#เช็คบอร์ดว่าเต็มไหม
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

def check_win(player):
#คอนดิชั่นเช็ค โดยจะเช็คได้ 4 แบบคือ แนวตั้ง แนวนอน เฉียงซ้ายและขวา
	#เช็คแนวตั้ง
	msg = "Player "+str(player)+" won, press space for restart..."
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			
			return True,messagebox.showinfo('Game Over!',msg)

	#เช็คแนวนอน
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True,messagebox.showinfo('Game Over!',msg)

	#เฉียงซ้าย
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True,messagebox.showinfo('Game Over!',msg)

	#เฉียงขวา
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True,messagebox.showinfo('Game Over!',msg)

	return False

#วาดเส้นทับตอนชนะ
def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

def restart():
	screen.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

draw_lines()

#เซ็ตเพล 1 เริ่มก่อน
player = 1
game_over = False

#mainloop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_row = int(mouseY // SQUARE_SIZE)
			clicked_col = int(mouseX // SQUARE_SIZE)

			if available_square( clicked_row, clicked_col ):

				mark_square( clicked_row, clicked_col, player )
				if check_win( player ):
					game_over = True
					
				player = player % 2 + 1

				draw_figures()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				restart()
				player = 1
				game_over = False

	pygame.display.update()

