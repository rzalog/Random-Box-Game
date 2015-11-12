# randbox.py
# Simple game where a box moves around, and user has to click on it

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SCREENCENTER = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
SCREENCENTERX = WINDOWWIDTH / 2
SCREENCENTERY = WINDOWHEIGHT / 2
MENUMARGIN = 50
XMARGIN = 20
YMARGIN = 20
BOXSIZE = 100

FRAMES_UNTIL_NEW = 40	# how long program waits to draw a new random box
TIMELIMIT = 60			# time limit of game in seconds
POINTS_PER_BOX = 10

# colors
#				R		G		B
WHITE 	=	(	255,	255,	255)
BLACK 	= 	(	0,		0,		0)
GREY 	=	(	100,	100,	100)

# the box colors (aka the pretty colors)
#				R		G		B
RED 	= 	(	255, 	0, 		0)
GREEN 	= 	(	0,		255,	0)
BLUE 	= 	(	0,		0,		255)
YELLOW  = 	(	255, 	255,   	0)
ORANGE  = 	(	255, 	128, 	0)
PURPLE  = 	(	255,   	0, 		255)
CYAN    = 	(  	0, 		255, 	255)


BOXCOLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]

BGCOLOR = WHITE
DEFAULT_BOX_COLOR = RED
TEXTCOLOR = BLACK

FONT = "freesansbold.ttf"
FONTSIZE = 16
BIGFONTSIZE = 24

def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode( (WINDOWWIDTH, WINDOWHEIGHT) )

	pygame.display.set_caption("Random Box Game")

	gameEnded = False
	wantsToRestart = False

	mousex = 0
	mousey = 0

	timeFrames = 0		# to keep track of time
	squareFrames = 0	# to keep track of when to make a new random square
	score = 0
	boxesClicked = 0
	secondsLeft = TIMELIMIT
	pointsPerBox = POINTS_PER_BOX
	framesUntilNew = FRAMES_UNTIL_NEW

	DISPLAYSURF.fill(BGCOLOR)
	scoreRect = updateScore(score)
	timeRect = updateTime(secondsLeft)
	# creates a "protective" box around menu so random squares don't collide with it
	menuRect = pygame.Rect(0, 0, timeRect.width + 2 * YMARGIN, scoreRect.height + timeRect.height + 2 * YMARGIN)
	menuRect.center = SCREENCENTER

	currentRandSquare = drawRandSquareOnBoard(True, menuRect)

	while True:
		# main game loop
		mouseClicked = False
		timeFrames += 1
		squareFrames += 1

		for event in pygame.event.get():
			# event handling loop
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = pygame.mouse.get_pos()
				mouseClicked = True
			elif gameEnded:
				if event.type == KEYUP and event.key == K_r:
					wantsToRestart = True


		if not gameEnded:
			if timeFrames == FPS:
				# if one second has passed, update the time
				secondsLeft -= 1
				if secondsLeft == 0:
					timeExpired(score)
					gameEnded = True
				else:
					timeRect = updateTime(secondsLeft, timeRect)
					timeFrames = 0

			if squareFrames == FRAMES_UNTIL_NEW:
				# if enough frames have passed to draw a new square
				currentRandSquare = drawNewSquare(currentRandSquare, menuRect)
				squareFrames = 0

			if mouseClicked:
				# Check if we clicked on the square, otherwise don't do anything
				if currentRandSquare.collidepoint(mousex+1, mousey+1):
					boxesClicked += 1
					score += pointsPerBox
					clickedSquare(score)
					if boxesClicked % 5 == 0 and framesUntilNew >= 15:
						# after a certain amount of boxes, incrase speed
						# and the score per box
						framesUntilNew -= 5
						pointsPerBox += 5
					currentRandSquare = drawNewSquare(currentRandSquare, menuRect)
					squareFrames = 0
		if gameEnded and wantsToRestart:
			main()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def giveRandRect(width, height, xmin, xmax, ymin, ymax, color):
	# generic function to produce a Rect object within a given set of coordinates
	x = random.randint(xmin, xmax+1)
	y = random.randint(ymin, ymax+1)
	rect = pygame.Rect(x,y, width,height)
	return rect

def drawRandSquareOnBoard(chooseRandColor=True, menuRect=None):
	# specialized function to draw a random square on the game board
	# option to specify a given menu rectangle to avoid placing random squares in that area
	xmin = 0 + XMARGIN
	xmax = WINDOWWIDTH - BOXSIZE - XMARGIN
	ymin = 0 + MENUMARGIN + YMARGIN
	ymax = WINDOWHEIGHT - BOXSIZE - YMARGIN
	if chooseRandColor:
		# pick a random color, not including the background color
		color = random.choice(BOXCOLORS)
		while color == BGCOLOR:
			color = random.choice(BOXCOLORS)
	else:
		color = BOXCOLOR

	randSquare = giveRandRect(BOXSIZE, BOXSIZE, xmin, xmax, ymin, ymax, color)
	if menuRect != None:
		# if requested, make sure randSquare does not collide with the menuRect
		while menuRect.colliderect(randSquare):
			randSquare = giveRandRect(BOXSIZE, BOXSIZE, xmin, xmax, ymin, ymax, color)

	if menuRect != None and menuRect.colliderect(randSquare):
		print("THEY ARE GOING TO COLLIDE!")

	pygame.draw.rect(DISPLAYSURF, color, randSquare)
	return randSquare

def drawNewSquare(currentSquare, menuRect=None):
	# remove the square at (x, y) and draw a new random square
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (currentSquare.x, currentSquare.y, BOXSIZE, BOXSIZE))
	newRect = drawRandSquareOnBoard(True, menuRect)
	return newRect

def clickedSquare(score):
	# what we are going to do if user succesfully clicks a square
	updateScore(score)

def updateScore(score):
	# draw and update the score
	scoreFont = pygame.font.Font(FONT, FONTSIZE)
	scoreObj = scoreFont.render("Score: %d" % score, False, TEXTCOLOR)
	scoreRectObj = scoreObj.get_rect()
	scoreRectObj.center = SCREENCENTER
	scoreRectObj.top = SCREENCENTERY		# give room for time label
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, scoreRectObj)
	DISPLAYSURF.blit(scoreObj, scoreRectObj)

	return scoreRectObj

def updateTime(timeLeft, oldTimeRect=None):
	timeFont = pygame.font.Font(FONT, FONTSIZE)
	timeObj = timeFont.render("Time left: %d" % timeLeft, True, TEXTCOLOR)
	timeRectObj = timeObj.get_rect()
	timeRectObj.center = SCREENCENTER
	timeRectObj.bottom = SCREENCENTERY		# move it up above score label
	if oldTimeRect != None:
		pygame.draw.rect(DISPLAYSURF, BGCOLOR, oldTimeRect)		# white out the old time rectangle
	DISPLAYSURF.blit(timeObj, timeRectObj)
	return timeRectObj

def timeExpired(score):
	# when the game ends, blank out the screen and send a message to the user
	DISPLAYSURF.fill(BGCOLOR)

	finalScoreFont = pygame.font.Font(FONT, BIGFONTSIZE)
	finalScoreObj = finalScoreFont.render("Final Score: %d" % score, True, TEXTCOLOR)
	finalScoreObjRect = finalScoreObj.get_rect()
	finalScoreObjRect.center = SCREENCENTER
	finalScoreObjRect.bottom = SCREENCENTERY

	restartMsgFont = pygame.font.Font(FONT, BIGFONTSIZE)
	restartMsgObj = restartMsgFont.render("Press 'r' to restart and break your score!", True, TEXTCOLOR)
	restartMsgObjRect = restartMsgObj.get_rect()
	restartMsgObjRect.center = SCREENCENTER
	restartMsgObjRect.top = SCREENCENTERY

	DISPLAYSURF.blit(finalScoreObj, finalScoreObjRect)
	DISPLAYSURF.blit(restartMsgObj, restartMsgObjRect)


if __name__ == "__main__":
	main()
