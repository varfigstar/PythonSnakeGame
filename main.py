import pygame
import config
import random

BLUE = (51, 51, 255)
WHITE = (255, 255, 255)

class Display:
	"""Class for pygame 
	technical logic. Inizialisation 
	of screen (root), clock (fps-contorl
	mechanism).
	"""
	FPS = 30
	width = config.width
	height = config.height

	def __init__(self, width=width, 
				height=height):

		pygame.init()

		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()

	def fill_background(self, color=WHITE):
		self.screen.fill(color)
		pygame.display.flip()


class GameBoard(Display):
	"""Class with
	game logic and algorithms 
	to working with game map:
	generate apples, resize 
	snake.
	Subclass of Display.
	"""

	def __init__(self):
		self.matrix_map = self.generate_matrix()
		self.display = Display()


	def generate_matrix(self, shape=(9, 9)):
		matrix = []

		for vertical_row in range(0, shape[0]):
			row = []
			for horizontal_row in range(0, shape[1]):
				row.append(0) 
			matrix.append(row)

		self.coube_width = Display.width // shape[0]
		self.coube_height = Display.height // shape[1]

		return matrix

	def start_game(self):
		run = True
		while run:
			self.display.clock.tick(Display.FPS)

			#checking all events
			for event in pygame.event.get():
				#check is close button clicked
				if event.type == pygame.QUIT:
					run = False

			self.display.fill_background(color=WHITE)
			

def run():
	board = GameBoard()
	board.start_game()


if __name__=="__main__":

	run()
	pygame.quit()