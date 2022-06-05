import pygame
import math
from board import Board

clock = pygame.time.Clock()
FPS = 30

grid_dimensions = (3, 3)
scaling_factor = sf = 100
scaled_dimensions = tuple(map(lambda d: d * sf, grid_dimensions))

screen = pygame.display.set_mode(scaled_dimensions)

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

pygame.font.init()
FONT_L = pygame.font.SysFont("timesnewroman", math.floor(sf * 0.36))
FONT_M = pygame.font.SysFont("timesnewroman", math.floor(sf * 0.24))
FONT_S = pygame.font.SysFont("timesnewroman", math.floor(sf * 0.16))

board = Board(screen, sf)

while board.active:
	screen.fill(BLACK)

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()

			board.check_click(pos)

		if event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_r]:
				board.start()

			if keys[pygame.K_q]:
				board.active = False

	board.update()

	if board.winner is None:
		sx, sy = screen.get_size()
		draw_msg = FONT_M.render(f"It's a draw.", False, 
 BLACK)
		while board.winner is None:
			screen.fill(WHITE)

			r = draw_msg.get_rect()
			w, h = r.w, r.h
			screen.blit(draw_msg, ((sx / 2) - (w / 2), (sy / 2) - (h / 2)))

			pygame.display.update()
			clock.tick(FPS)

			events = pygame.event.get()
			for event in events:	
				if event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_r]:
						board.winner = False
						board.start()
					if keys[pygame.K_q]:
						board.winner = False
						board.active = False
		
	elif board.winner:
		winner = board.winner
		sx, sy = screen.get_size()
		
		player_msg = FONT_L.render(f"Player {winner}", False, BLACK)
		win_msg = FONT_M.render(f"has won the game!", False, BLACK)

		while board.winner:
			screen.fill(WHITE)
			
			r = player_msg.get_rect()
			w, h = r.w, r.h
			screen.blit(player_msg, ((sx / 2) - (w / 2), (sy / 2) - h))

			r = win_msg.get_rect()
			w, h = r.w, r.h
			screen.blit(win_msg, ((sx / 2) - (w / 2), (sy / 2) + h))
			
			pygame.display.update()
			clock.tick(FPS)
			
			events = pygame.event.get()
			for event in events:	
				if event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_r]:
						board.winner = False
						board.start()
					if keys[pygame.K_q]:
						board.winner = False
						board.active = False
	
	pygame.display.update()
	clock.tick(FPS)