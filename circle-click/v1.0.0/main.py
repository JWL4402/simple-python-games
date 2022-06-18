import pygame

WHITE = (255, 255, 255)

class Game:
	def __init__(self):
		WIN_DIMENSIONS = (800, 600)
		self.WIN = pygame.display.set_mode(WIN_DIMENSIONS)

		self.FPS = 30
		self.timer = pygame.time.Clock()

		pygame.display.set_caption("Circle Click")

	def start(self):
		self.active = True

		while self.active:
			self.update()
	
	def draw(self):
		self.WIN.fill(WHITE)

		pygame.display.update()

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

	def update(self):
		self.handle_events()

		self.draw()

		self.timer.tick(self.FPS)

def main():
	game = Game()
	game.start()

if __name__ == "__main__":
	main()