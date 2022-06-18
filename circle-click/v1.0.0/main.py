import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
	def __init__(self):
		WIN_DIMENSIONS = (800, 600)
		self.WIN = pygame.display.set_mode(WIN_DIMENSIONS)

		self.FPS = 30
		self.timer = pygame.time.Clock()

		self.circles = pygame.sprite.Group()

		self.max_circles = 6
		self.cir_chance = 0.8 / self.FPS # 0.5 / second

		pygame.display.set_caption("Circle Click")

	def start(self):
		self.active = True

		if len(self.circles.sprites()) > 0:
			self.circles.empty()

		while self.active:
			self.update()

	def create_circle(self):
		if not len(self.circles.sprites()) < self.max_circles:
			return
		
		if random.uniform(0.0, 1.0) < self.cir_chance:
			self.circles.add(Circle(self))
	
	def draw(self):
		self.WIN.fill(WHITE)

		for circle in self.circles:
			pygame.draw.circle(self.WIN, circle.color, circle.pos, circle.radius)

		pygame.display.update()

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			
			if event.type == pygame.KEYDOWN:
				self.handle_key_input()

	def handle_key_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.start()

	def update(self):
		self.handle_events()

		self.create_circle()

		self.draw()

		self.timer.tick(self.FPS)

class Circle(pygame.sprite.Sprite):
	def __init__(self, game):
		"""Initializes the circle class."""
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.color = BLACK

		self.create()

		# ensure no circles collide with each other
		if len(self.game.circles.sprites()) > 0:
			while pygame.sprite.spritecollide(self, self.game.circles, False, pygame.sprite.collide_circle):
				self.create()

	def create(self):
		"""Creates a circle with a randomized position and size."""
		size_min, size_max = (20, 50)
		size = random.choice(range(size_min, size_max + 1))

		self.image = pygame.Surface((size, size))
		self.image.fill(self.color)

		WIN_width = self.game.WIN.get_size()[0]
		r = size // 2
		self.radius = r

		x = random.choice(range(10 + r, WIN_width - 10 - r))
		y = r + 10
		self.pos = (x, y)

		self.rect = self.image.get_rect(center = self.pos)


def main():
	game = Game()
	game.start()

if __name__ == "__main__":
	main()