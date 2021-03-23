import pygame

class Display:
	"""Class for pygame 
	technical logic. Inizialisation 
	of screen (root), clock (fps-contorl
	mechanism).
	"""

	width = 600
	height = 600

	def __init__(self, width=600, 
				height=600, fps=30):

		pygame.init()

		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()


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

def run():
	GameBoard()



if __name__=="__main__":

	run()