import pygame
from board import Board

clock = pygame.time.Clock()
FPS = 30

grid_dimensions = (3, 3)
scaling_factor = sf = 100
scaled_dimensions = tuple(map(lambda d: d * sf, grid_dimensions))

screen = pygame.display.set_mode(scaled_dimensions)

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

board = Board(screen, sf)

while True:
	screen.fill(black)

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()

			board.check_click(pos)

	board.update()
	
	pygame.display.update()
	clock.tick(FPS)