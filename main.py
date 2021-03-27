import pygame
import config
import random


BLUE = (51, 51, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class SnakeBlock(pygame.sprite.Sprite):
	def __init__(self, snake):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((snake.coube_width, snake.coube_height))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()


class Apple(pygame.sprite.Sprite):
	"""Class that place apple on map
	and generate new random position 
	after eating of apple.
	Taking an argument Snake's instanse to
	handling is position of snake 
	on apple block (eating handler).
	"""
	def __init__(self, coube_height, coube_width, snake, all_sprites=None):
		pygame.sprite.Sprite.__init__(self)
		self.all_sprites = all_sprites
		self.coube_width = coube_width
		self.coube_height = coube_height
		self.image = pygame.Surface((coube_width, coube_height))
		self.image.fill(RED)
		self.snake = snake 
		self.rect = self.image.get_rect()
		self.generate_random_pos()


	def update(self):
		if self.snake.rect.x == self.rect.x and self.snake.rect.y == self.rect.y:	
			self.generate_random_pos()	
			block = SnakeBlock(snake=self.snake)
			self.snake.blocks.append(block)
			block.rect.x, block.rect.y = self.snake.all_moves[len(self.snake.all_moves)-len(self.snake.blocks)]
			
			
			self.all_sprites.add(block)

	def generate_random_pos(self):
		self.rect.x = random.choice(range(0, config.width+1, self.coube_width)) 
		self.rect.y = random.choice(range(0, config.height+1, self.coube_height))
		if self.rect.x >= config.width:
			self.rect.x = config.width - self.coube_width
		if self.rect.y >= config.height:
			self.rect.y = config.height - self.coube_height


class Snake(pygame.sprite.Sprite):
	"""Class that describe 
	logic of snake: rotation, eating,
	moving and etc. 
	"""
	def __init__(self, coube_width, coube_height):
		pygame.sprite.Sprite.__init__(self)
		self.coube_width = coube_width
		self.coube_height = coube_height
		self.image = pygame.Surface((coube_width, coube_height))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.move_side = "right"
		self.speed_counter = 0
		self.rect.x = random.choice(range(0, config.width+1, self.coube_width))
		self.rect.y = random.choice(range(0, config.height+1, self.coube_height))
		self.key = pygame.K_RIGHT
		self.blocks = []
		self.all_moves = []

	def render_body(self):
		if len(self.blocks) > 0:
			block_number = 0
			for block in self.blocks:
				if self.rect.x == block.rect.x and self.rect.y == block.rect.y:
					print("You dead!")
					pygame.quit()
				block.rect.x, block.rect.y = self.all_moves[len(self.all_moves)-block_number-1]
				block_number += 1

	def update(self):
		if self.speed_counter == 15:
			#death hadnling
			self.all_moves.append((self.rect.x, self.rect.y))

			if self.key is pygame.K_LEFT and self.move_side != "right":
				self.move_side = "left"
			elif self.key is pygame.K_RIGHT and self.move_side != "left":
				self.move_side = "right"
			elif self.key is pygame.K_UP and self.move_side != "down":
				self.move_side = "up"
			elif self.key is pygame.K_DOWN and self.move_side != "up":
				self.move_side = "down"

			if self.move_side == "right":
				self.rect.x += self.coube_width
			elif self.move_side == "left":
				self.rect.x -= self.coube_width
			elif self.move_side == "up":
				self.rect.y -= self.coube_width
			elif self.move_side == "down":
				self.rect.y += self.coube_width

			if self.rect.right > config.width:
				self.rect.x = 0
			elif self.rect.left < 0: 
				self.rect.x = config.width - self.coube_width
			elif self.rect.bottom > config.height:
				self.rect.y = 0
			elif self.rect.top < 0: 
				self.rect.y = config.height - self.coube_height

			self.render_body()
			self.speed_counter = 0
		else: 
			self.speed_counter += 1 

				
class Display:
	"""Class for pygame 
	technical logic. Inizialisation 
	of screen (root), clock (fps-contorl
	mechanism).
	"""
	FPS = 30
	width = config.width
	height = config.height

	def __init__(self, width=width, height=height):
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
		self.generate_matrix()
		self.display = Display()
		self.all_sprites = pygame.sprite.Group()
		self.snake = Snake(self.coube_width, self.coube_height)
		self.apple = Apple(self.coube_width, self.coube_height, self.snake)
		self.all_sprites.add(self.snake, self.apple)
		self.apple.all_sprites = self.all_sprites

	def generate_matrix(self, shape=(9, 9)):
		self.coube_width = Display.width // shape[0]
		self.coube_height = Display.height // shape[1]


	def start_game(self):
		run = True
		while run:
			self.display.clock.tick(Display.FPS)
			#checking all events
			for event in pygame.event.get():
				#check is close button clicked
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.snake.key = pygame.K_LEFT
					elif event.key == pygame.K_RIGHT:
						self.snake.key = pygame.K_RIGHT
					elif event.key == pygame.K_UP:
						self.snake.key = pygame.K_UP
					elif event.key == pygame.K_DOWN:
						self.snake.key = pygame.K_DOWN
			self.display.draw_sprites(self.all_sprites)
			#flip all drawed pixels on the user screen
			pygame.display.flip()


def run():
	board = GameBoard()
	board.start_game()


if __name__=="__main__":
	run()
	pygame.quit()