import pygame as p
import sys
import os

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
	load_images()
	board = [
		["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
		["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
		["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
	]
	print(board[5][1] == "--")

	p.init
	screen = p.display.set_mode((WIDTH, HEIGHT))
	screen.fill(p.Color("white"))
	clock = p.time.Clock()
	running = True
	colors = [p.Color("white"), p.Color("gray")]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			if (r+c)%2 == 0:
				p.draw.rect(screen, colors[0], ((r*SQ_SIZE, c*SQ_SIZE), (SQ_SIZE, SQ_SIZE)))
			elif (r+c)%2 == 1:
				p.draw.rect(screen, colors[1], ((r*SQ_SIZE, c*SQ_SIZE), (SQ_SIZE, SQ_SIZE)))
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[c][r] 
			if piece == "--":
				pass
			else:
				screen.blit(IMAGES[piece], (r*SQ_SIZE, c*SQ_SIZE))

	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
				p.quit()
				sys.exit()
		clock.tick(MAX_FPS)
		p.display.flip()


if __name__ == '__main__':
	main()