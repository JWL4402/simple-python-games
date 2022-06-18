import pygame
import numpy as np
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
	def __init__(self):
		WIN_DIMENSIONS = (800, 700)
		self.WIN = pygame.display.set_mode(WIN_DIMENSIONS)

		self.FPS = 30
		self.timer = pygame.time.Clock()

		self.circles = pygame.sprite.Group()

		self.max_circles = 9
		self.cir_chance = 1.3 / self.FPS # num circle / second

		pygame.display.set_caption("Circle Click")

	def start(self):
		self.active = True

		self.difficulty_factor = 0

		if len(self.circles.sprites()) > 0:
			self.circles.empty()

		self.scoreboard = Scoreboard(self)

		while self.active:
			self.update()
	
	def scale_difficulty(self):
		self.difficulty_factor += 0.001
		df = self.difficulty_factor
		self.max_circles = 9 + df
		self.cir_chance = (1.3 / self.FPS) + (df / 10) # num circle / second

	def create_circle(self):
		if not len(self.circles.sprites()) < self.max_circles:
			return
		
		if random.uniform(0.0, 1.0) < self.cir_chance:
			self.circles.add(Circle(self))

	def check_circle_escape(self):
		escaped = pygame.sprite.spritecollide(self.scoreboard, self.circles, False)
		if len(escaped) > 0:
			self.scoreboard.lives -= 1
			self.circles.remove(escaped)

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			
			if event.type == pygame.KEYDOWN:
				self.handle_key_input()

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.handle_mouse_input(event.pos)

	def handle_key_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.start()
	
	def handle_mouse_input(self, click_pos):
		clicked = list(filter(lambda c: c.rect.collidepoint(click_pos), self.circles.sprites()))
		# TODO : scoring system
		if len(clicked) == 0:
			return
		self.scoreboard.score += 100 + int((self.difficulty_factor // 1) * 25)
		self.circles.remove(clicked)

	def draw(self):
		self.WIN.fill(WHITE)

		for circle in self.circles:
			pygame.draw.circle(self.WIN, circle.color, circle.rect.center, circle.radius)
		
		self.scoreboard.draw()
		
		pygame.display.update()

	def update(self):
		self.handle_events()

		self.create_circle()

		self.circles.update()
		self.check_circle_escape()

		self.draw()

		self.scale_difficulty()

		self.timer.tick(self.FPS)

class Scoreboard(pygame.sprite.Sprite):
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)

		self.game = game

		self.background_color = BLACK
		self.text_color = WHITE

		self.score = 0
		self.lives = 3

		WIN_w, WIN_h = self.game.WIN.get_size()
		self.dim = (WIN_w, 100)

		self.image = pygame.Surface(self.dim)
		self.image.fill(self.background_color)

		self.pos = (0, WIN_h - 100)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.pos
	
	def draw(self):
		pygame.draw.rect(self.game.WIN, self.background_color, self.rect)

		font = pygame.font.SysFont("impact", 60)
		score = font.render(f"Score: {self.score}", False, self.text_color)
		score_pos = (10, self.pos[1] + self.dim[1] // 2 - score.get_rect().h // 2)
		lives = font.render(f"Lives: {self.lives}", False, self.text_color)
		lives_pos = (self.dim[0] // 2 + 10, self.pos[1] + self.dim[1] // 2 - lives.get_rect().h // 2)
		self.game.WIN.blit(score, score_pos, score.get_rect())
		self.game.WIN.blit(lives, lives_pos, lives.get_rect())

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
		size_min, size_max = (30, 65)
		size = random.choice(range(size_min, size_max + 1))

		df = self.game.difficulty_factor
		self.velocity = round(random.choice(
			np.linspace(1.0 + df, 2.5 + df, 31).astype(float).tolist()))
		self.velocity_max = round(random.choice(
			np.linspace(3.0 + df, 5.5 + df, 51).astype(float).tolist()))
		self.acceleration = round(random.choice(
			np.linspace(0.01 + df/1000, 0.04 + df/1000, 4).astype(float).tolist()))
		# numpy was the only way I could find to do get a range with a
		# step that is a float. Not very readable.

		self.image = pygame.Surface((size, size))
		self.image.fill(self.color)

		WIN_width = self.game.WIN.get_size()[0]
		r = size // 2
		self.radius = r

		x = random.choice(range(10 + r, (WIN_width - 10 - r) + 1))
		y = r + 10
		self.pos = (x, y)

		self.rect = self.image.get_rect(center = self.pos)
	
	def update(self):
		if self.velocity < self.velocity_max:
			self.velocity += self.acceleration

		self.rect.move_ip((0, self.velocity))


def main():
	pygame.init()
	game = Game()
	game.start()

if __name__ == "__main__":
	main()