# randbox.py
# Simple game where a box moves around, and user has to click on it

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
MENUMARGIN = 50
XMARGIN = 20
YMARGIN = 20
BOXSIZE = 30

FRAMES_UNTIL_NEW = 60	# how long program waits to draw a new random box

# colors
#			R		G		B
RED = 	(	255, 	0, 		0)
GREEN = (	0,		255,	0)
BLUE = 	(	0,		0,		255)
GREY =	(	100,	100,	100)
WHITE =	(	255,	255,	255)
BLACK = (	0,		0,		0)

colors = [RED, GREEN, BLUE, GREY, WHITE, BLACK]

BGCOLOR = WHITE
BOXCOLOR = RED

def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode( (WINDOWWIDTH, WINDOWHEIGHT) )

	pygame.display.set_caption("Random Box Game")

	mousex = 0
	mousey = 0

	rectx = 0	# where the random square is currently located
	recty = 0

	frames = 0

	score = 0

	firstSquareDrawn = False

	DISPLAYSURF.fill(BGCOLOR)

	while True:
		# main game loop
		mouseClicked = False

		for event in pygame.event.get():
			# event handling loop
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.quit()
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = pygame.mouse.get_pos()
				mouseClicked = True

		if not firstSquareDrawn:
			rectx, recty = drawRandSquareOnBoard()
			firstSquareDrawn = True
		else:
			frames += 1
			if frames == FRAMES_UNTIL_NEW:
				# if enough frames have passed to draw a new square
				rectx, recty = drawNewSquare(rectx, recty)
				frames = 0

		if mouseClicked:
			# Check if we clicked on the square, otherwise don't do anything
			if mousex > rectx and mousex < rectx + BOXSIZE and mousey > recty and mousey < recty + BOXSIZE:
				didClickSquare()
				score += 1
				print("Score:", score)
				rectx, recty = drawNewSquare(rectx, recty)
				frames = 0


		pygame.display.update()
		FPSCLOCK.tick(FPS)

def drawRandRect(width, height, xmin, xmax, ymin, ymax, color):
	# generic function to draw a rectangle within a given set of coordinates
	x = random.randint(xmin, xmax+1)
	y = random.randint(ymin, ymax+1)
	pygame.draw.rect(DISPLAYSURF, color, (x,y, width, height))
	return x, y		# so that we know where we put the rectangle

def drawRandSquareOnBoard(chooseRandColor = True):
	# specialized version of drawRandRect specific to the game
	xmin = 0 + XMARGIN
	xmax = WINDOWWIDTH - BOXSIZE - XMARGIN
	ymin = 0 + MENUMARGIN + YMARGIN
	ymax = WINDOWHEIGHT - BOXSIZE - YMARGIN
	if chooseRandColor:
		# pick a random color, not including the background color
		color = random.choice(colors)
		while color == BGCOLOR:
			color = random.choice(colors)
	else:
		color = BOXCOLOR
	x, y = drawRandRect(BOXSIZE, BOXSIZE, xmin, xmax, ymin, ymax, color)
	return x, y

def drawNewSquare(x, y):
	# remove the square at (x, y) and draw a new random square
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (x, y, BOXSIZE, BOXSIZE))
	newx, newy = drawRandSquareOnBoard()
	return newx, newy

def didClickSquare():
	# what we are going to do if user succesfully clicks a square
	print("You did it!")

if __name__ == "__main__":
	main()
