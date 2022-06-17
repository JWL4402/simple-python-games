import pygame
from square import Square

white = pygame.Color(255, 255, 255)

class Board:
	squares = []
	turn = 1
	
	def __init__(self, screen, sf):
		self.screen = screen
		self.sf = sf
		
		self.generate_squares()

	def generate_squares(self):
		sf = self.sf
		x, y = 0, 0
		l = 0
		for i in range(3):
			for n in range(3):
				square = Square(self.screen, (sf, sf), (x, y), white)
				self.squares.append(square)
				x += 100
				l += 1
			x = 0
			y += 100

	def check_click(self, pos):
		clicked = [s for s in self.squares if s.rect.collidepoint(pos)][0] # index bcuz list

		self.turn += clicked.change("X" if self.turn % 2 else "O")


	
	def draw(self):
		squares = self.squares

		for square in squares:
			pygame.draw.rect(self.screen, square.color, square)
	
	def update(self):
		self.draw()