import pygame
import config
import random

BLUE = (51, 51, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Snake(pygame.sprite.Sprite):
	def __init__(self, coube_width, coube_height):
		pygame.sprite.Sprite.__init__(self)
		self.coube_width = coube_width
		self.coube_height = coube_height
		self.image = pygame.Surface((coube_width, coube_height))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.center = (config.width / 2, config.height / 2)
		self.move_side = "right"

	def update(self):
		if self.move_side == "right":
			self.rect.x += self.coube_width
			

		elif self.move_side == "left":
			self.rect.x -= self.coube_width
			
		if self.rect.left > config.width:
			self.rect.x = 0


class Display:
	"""Class for pygame 
	technical logic. Inizialisation 
	of screen (root), clock (fps-contorl
	mechanism).
	"""
	FPS = 3
	width = config.width
	height = config.height

	def __init__(self, width=width, 
				height=height):

		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()

	def draw_sprites(self, all_sprites):
		#Take sprite group; iter in sprite group every sprite with update methond; filling background.
		all_sprites.update()
		self.screen.fill(BLACK)
		all_sprites.draw(self.screen)

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
		self.all_sprites = pygame.sprite.Group()
		self.snake = Snake(self.coube_width, self.coube_height)

		self.all_sprites.add(self.snake)

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

			self.display.draw_sprites(self.all_sprites)

			#flip all drawed pixels on the user screen
			pygame.display.flip()

def run():
	board = GameBoard()
	board.start_game()


if __name__=="__main__":

	run()
	pygame.quit()