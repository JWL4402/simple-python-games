import pygame

blue = pygame.Color(0, 0, 255)
orange = pygame.Color(255, 128, 0)

class Square(pygame.sprite.Sprite):
	clicked = False
	
	def __init__(self, screen, dimensions, position, color):
		pygame.sprite.Sprite.__init__(self)
		# inherit from sprite parent class

		self.screen = screen
		self.color = color

		self.image = pygame.Surface(dimensions)
		self.image.fill(color)

		rect = self.image.get_rect()
		rect.x, rect.y = position
		self.rect = rect

	def change(self, value):
		if self.clicked:
			return 0
		self.clicked = True
		self.value = value

		self.color = orange if value == "X" else blue

		# TODO : Add code to show which player clicked

		return 1