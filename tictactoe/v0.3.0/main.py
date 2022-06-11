import pygame
import math

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

config = {
	"p1_symbol": "X",
	"p2_symbol": "O",
	"symbol_color": BLACK,
	"board_dimensions": (3, 3),
	"square_size": 100,
	"square_color": WHITE,
	"border_size": 2,
	"border_color": BLACK,
	"text_size": 24,
	"text_color": BLACK,
	"background_color": WHITE,
	"FPS": 30
}


class Square(pygame.sprite.Sprite):
	def __init__(self, game, pos):
		pygame.sprite.Sprite.__init__(self)

		self.clicked = False
		self.value = None

		self.game = game
		self.pos = pos

		ss = self.game.config["square_size"]
		color = self.game.config["square_color"]

		self.image = pygame.Surface((ss, ss))
		self.image.fill(color)

		rect = self.image.get_rect()
		rect.x, rect.y = pos
		self.rect = rect

	def update_value(self, symbol):
		if self.clicked:
			return 0

		self.clicked = True
		self.value = symbol  # change value to symbol

		self.letter = self.game.fonts["L"].render(self.value, False, self.game.config["text_color"])

		return 1

	def draw_letter(self):
		x = self.rect.x + ((100 - self.letter.get_rect().w) / 2)
		y = self.rect.y + ((100 - self.letter.get_rect().h) / 2)
		pos = (x, y)

		self.game.screen.blit(self.letter, pos)


class Board:
	"""Represents the board and contains the majority of functions necessary to play matches."""

	def __init__(self, game):
		self.game = game

	def populate_board(self):
		"""Generates a list of squares to fill the board."""
		config = self.game.config

		squares = []
		ss, bs = config["square_size"], config["border_size"]

		x, y = (0, 0)
		columns, rows = config["board_dimensions"]

		for c in range(columns):
			for r in range(rows):
				square = Square(self.game, (x, y))
				squares.append(square)
				x += ss + bs
			x = 0
			y += ss + bs
		# Generates a grid of squares

		self.squares = squares

	def handle_click(self, click_pos):
		"""Updates the value of clicked squares."""
		config = self.game.config
		clicked = [s for s in self.squares if s.rect.collidepoint(click_pos)]
		# a list of all squares that collide with the
		# mouse position when it was clicked
		clicked_square = clicked[0]

		p1, p2 = config["p1_symbol"], config["p2_symbol"]
		symbol = p1 if self.game.turn % 2 == 0 else p2

		self.game.turn += clicked_square.update_value(symbol)

	def draw(self):
		"""Draws the squares to the board."""
		squares = self.squares

		for square in squares:
			pygame.draw.rect(self.game.screen, self.game.config["square_color"], square)

			if square.clicked:
				square.draw_letter()

	def update(self):
		self.draw()
		self.game.check_win()


class Game:
	"""Represents the game."""

	def __init__(self, config):
		"""Initializes everything necessary for the game."""
		self.config = config
		self.timer = pygame.time.Clock()
		self.FPS = config["FPS"]

		ss, bs = config["square_size"], config["border_size"]
		scaled_dimensions = tuple(
		    map(lambda d: (d * ss) + ((d - 1) * bs), config["board_dimensions"]))
		# finds the dimensionsF required to fit the squares and
		# border with the specified size

		self.screen = pygame.display.set_mode(scaled_dimensions)

		ts = config["text_size"]
		pygame.font.init()
		self.fonts = {
			"L": pygame.font.SysFont("timesnewroman", math.floor(ts * (7/3))),
			"M": pygame.font.SysFont("timesnewroman", ts),
			"S": pygame.font.SysFont("timesnewroman", math.floor(ts * (3/4)))
		}

		self.board = Board(self)

		self.start_match()

	def start_match(self):
		self.active = True
		self.winner = False
		self.turn = 0

		self.board.populate_board()

		while self.active:
			print(True)
			self.update()

	def handle_events(self):
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
        
			if event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
				pos = pygame.mouse.get_pos()
	
				self.board.handle_click(pos)
	
			if event.type == pygame.KEYDOWN:
				keys = pygame.key.get_pressed()
	
				if keys[pygame.K_r]:
					print(False)
					self.start_match()
	
				if keys[pygame.K_q]:
					pygame.quit()

	def check_win(self):
		"""Checks if a player has won or if the game has resulted in a draw."""
		squares = self.board.squares

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
				i1, i2, i3 = arr[0], arr[1], arr[2] # TODO : maybe could be improved with list comprehension
				s1, s2, s3 = squares[i1], squares[i2], squares[i3]
				if s1.value == s2.value and s2.value == s3.value and s1.value is not None:
					# check if a player has occupied any sequence
					# of squares required to win
					self.winner = s1.value

		filled_squares = tuple(filter(lambda v: (v.value is not None), squares))
		max_squares = self.config["board_dimensions"][0] * self.config["board_dimensions"][1]
		
		if self.winner == False and len(filled_squares) == max_squares:
			# check if all squares are filled and if no one
			# has won (draw)
			self.winner = None

		if self.winner is not False:
			return True
		else:
			return False

	def handle_win(self):
		winner = self.winner
		sx, sy = self.screen.get_size()

		while winner is not False:
			self.screen.fill(self.config["background_color"])
			
			if winner is None:
				msg = self.fonts["M"].render("It's a draw.", False, self.config["text_color"])
				rect = msg.get_rect()
				w, h = rect.w, rect.h
				self.screen.blit(msg, ((sx / 2) - (w / 2), (sy / 2) - (h / 2))) # TODO
			elif winner:
				msgs = [
					self.fonts["L"].render(f"Player {winner}", False, BLACK),
					self.fonts["M"].render(f"has won the game!", False, BLACK)
				]

				for i, msg in enumerate(msgs):
					r = msg.get_rect()
					w, h = r.w, r.h if i == 0 else -(r.h)
					self.screen.blit(msg, ((sx / 2) - (w / 2), (sy / 2) - h))
				
			self.handle_events()

			pygame.display.update()
			self.timer.tick(self.FPS)
			
	def update(self):
		self.screen.fill(self.config["border_color"])

		self.handle_events()

		self.board.update()

		if self.check_win():
			self.handle_win()

		pygame.display.update()
		self.timer.tick(self.FPS)

game = Game(config)

game.start()