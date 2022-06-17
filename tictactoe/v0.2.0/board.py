import pygame
from square import Square

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

class Board:
	active = True
	winner = False
	border_size = 2
	
	def __init__(self, screen, sf):
		self.screen = screen
		self.sf = sf
		self.start()

	def start(self):
		self.turn = 1
		self.generate_squares()

	def generate_squares(self):
		self.squares = []
		sf = self.sf
		border_size = self.border_size
		x, y = 0, 0
		l = 0 # ??? what does this variable do
		for i in range(3):
			for n in range(3):
				square = Square(self.screen, (sf, sf), (x, y), WHITE)
				self.squares.append(square)
				x += sf + border_size
				l += 1 # ???
			x = 0
			y += sf + border_size

	def check_click(self, pos):
		clicked = [s for s in self.squares if s.rect.collidepoint(pos)] # index bcuz list

		if clicked:
			self.turn += clicked[0].change("X" if self.turn % 2 else "O")

	def check_win(self):
		squares = self.squares

		win_arrangements = [
			[0, 3, 6],
			[1, 4, 7],
			[2, 5, 8],
			[0, 1, 2],
			[3, 4, 5],
			[6, 7, 8],
			[0, 4, 8],
			[2, 4, 6]
		]

		for arr in win_arrangements:
			i1, i2, i3 = arr[0], arr[1], arr[2]
			s1, s2, s3 = squares[i1], squares[i2], squares[i3]
			if s1.value == s2.value and s2.value == s3.value and s1.value is not None:
				self.winner = s1.value

		if self.winner == False and len(tuple(filter(lambda v: (v.value is not None), squares))) == 9:
			self.winner = None
	
	def draw(self):
		squares = self.squares

		for square in squares:
			pygame.draw.rect(self.screen, square.color, square)
			if square.clicked:
				square.draw_letter()
	
	def update(self):
		self.draw()
		self.check_win()