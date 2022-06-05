import pygame

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

class Square(pygame.sprite.Sprite):
	clicked = False
	value = None
	reduction = 10
	
	def __init__(self, screen, dimensions, position, color):
		pygame.sprite.Sprite.__init__(self)
		# inherit from sprite parent class

		self.screen = screen
		self.color = color

		self.dx, self.dy = dimensions
		
		pygame.font.init()
		self.font = pygame.font.SysFont("timesnewroman", 80)
		self.font_color = BLACK

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

		self.letter = self.font.render(self.value, False, self.font_color)

		return 1

	def draw_letter(self):
		x = self.rect.x + ((100 - self.letter.get_rect().w) / 2) 
		y = self.rect.y + ((100 - self.letter.get_rect().h) / 2) 
		pos = (x, y)
		
		self.screen.blit(self.letter, pos)