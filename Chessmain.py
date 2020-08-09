import pygame as p
import Engine
import os
import sys
import random
import MinMax

WIDTH = HEIGHT = 512 #some power of 2 scaled to the images
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
	pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load(os.path.join("Images", piece  + ".png")), (SQ_SIZE, SQ_SIZE))

def main():
	p.init
	screen = p.display.set_mode((WIDTH, HEIGHT))
	screen.fill(p.Color("white"))
	clock = p.time.Clock()
	gs = Engine.Gamestate()
	allMoves = gs.generate_valid_moves()
	moveMade = False
	load_images()
	running = True
	squareSelected = ()
	playerClicks = []
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
				p.quit()
				sys.exit()
			elif e.type == p.MOUSEBUTTONDOWN:
				position = p.mouse.get_pos()
				r = position[1]//SQ_SIZE
				c = position[0]//SQ_SIZE
				if  squareSelected == (r, c):
					squareSelected = ()
					playerClicks = []
				else:
					squareSelected = (r, c)
					playerClicks.append(squareSelected)

				if len(playerClicks) == 2:
					move = [list(playerClicks[0]), list(playerClicks[1]), gs.board[playerClicks[0][0]][playerClicks[0][1]],  gs.board[playerClicks[1][0]][playerClicks[1][1]]] 
					if move in allMoves:
						gs.make_move(move)
						squareSelected = ()
						playerClicks = []
						# allMoves = gs.generate_valid_moves()
						# rand = random.randint(0, len(allMoves) - 1)
						# gs.make_move(allMoves[rand])
						value, move = MinMax.min_max_search(2, gs, "b", alpha = -10**16, beta = 10**16)
						if move != None:
							gs.make_move(move)
						else:
							print("NO MOVE FOUND")
						moveMade = True
			elif e.type == p.KEYDOWN:
				if e.key == p.K_DELETE:
					gs.undo_move()
					moveMade = True

		if moveMade:
			allMoves = gs.generate_valid_moves()
			moveMade = False


		draw_gamestate(screen, gs, allMoves, squareSelected)
		clock.tick(MAX_FPS)
		p.display.flip()

def highlight_last_move(screen, gs):
	if len(gs.moveLog) != 0:
		lastMove = gs.moveLog[-1]
		rowStart = lastMove[0][0]
		colStart = lastMove[0][1]
		rowEnd = lastMove[1][0]
		colEnd = lastMove[1][1]
		s = p.Surface((SQ_SIZE, SQ_SIZE))
		s.set_alpha(100)
		s.fill(p.Color("green"))
		screen.blit(s, (colStart*SQ_SIZE, rowStart*SQ_SIZE))
		screen.blit(s, (colEnd*SQ_SIZE, rowEnd*SQ_SIZE))
	

def highlight_squares(screen, gs, validMoves, squareSelected):
	if squareSelected != ():
		r, c = squareSelected
		if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
			s = p.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(100)
			s.fill(p.Color("blue"))
			screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
			s.fill(p.Color("yellow"))
			for move in validMoves:
				if move[0][0] == r and move[0][1] == c:
					screen.blit(s, (move[1][1]*SQ_SIZE, move[1][0]*SQ_SIZE))

def draw_gamestate(screen, gs, validMoves, squareSelected):
	draw_board(screen) #draw the squares
	highlight_squares(screen, gs, validMoves, squareSelected)
	highlight_last_move(screen, gs)
	draw_pieces(screen, gs.board) #draw pieces ontop of screen

def draw_board(screen):
	colors = [p.Color("white"), p.Color("gray")]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
				color = colors[(r+c)%2]
				p.draw.rect(screen, color, ((c*SQ_SIZE, r*SQ_SIZE), (SQ_SIZE, SQ_SIZE)))

def draw_pieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c] 
			if piece != "--":
				screen.blit(IMAGES[piece], (c*SQ_SIZE, r*SQ_SIZE))
	
if __name__ == '__main__':
	main()



