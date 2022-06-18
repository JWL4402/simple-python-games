import pygame
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

config = {
	"FPS": 60,
	"grid_size": (7, 6), # columns, rows
	"square_size": 50,
	"square_color": BLUE,
	"border_size": 2,
	"border_color": BLACK
}

grid_size = config["grid_size"]
square_size = ss = config["square_size"]
border_size = bs = config["border_size"]

screen_dimensions = tuple(map(
	lambda d: d * square_size + (d - 1) * border_size, 
	grid_size))
WIN = pygame.display.set_mode(screen_dimensions)

class Slot(pygame.sprite.Sprite):
	"""Represents a slot on the grid."""
	cir_color = WHITE
	
	def __init__(self, game, pos, grid_pos):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.grid_pos = grid_pos
		self.column, self.row = grid_pos
		self.color = self.game.config["square_color"]

		dimensions = (ss, ss)

		self.image = pygame.Surface(dimensions)
		self.image.fill(self.color)

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = pos

	def update_value(self):
		"""Changes the colour of the slot to red or yellow."""
		slots_column = list(filter(lambda s: s.column == self.column, self.game.slots))

		potential_slots = list(filter(lambda s: s.cir_color == WHITE, slots_column))
		
		if not len(potential_slots):
			return 0

		slot = potential_slots[-1]
		
		slot.cir_color = RED if self.game.turn % 2 == 1 else YELLOW

		self.game.moves.append(slot)
		
		return 1

class Game():
	"""Represents the game."""
	timer = pygame.time.Clock()

	def __init__(self, config):
		self.config = config
	
	def start_match(self):
		"""Begins a match of Connect 4."""
		self.active = True
		self.turn = 1
		self.winner = False
		self.moves = []
		self.populate_slots()

		pygame.display.set_caption("Connect 4")

		while self.active:
			self.update()

	def populate_slots(self):
		"""Generates all Slot objects required to populate the grid."""
		self.slots = []
		columns, rows = self.config["grid_size"]
		x, y = (0, 0)
		for column in range(columns):
			for row in range(rows):
				self.slots.append(Slot(self, (x, y), (1 + column, rows - row)))
				y += ss + bs
			y = 0
			x += ss + bs
		# ^ creates the necessary amount of slots based on the number
		# of columns and rows.
	
	def undo(self):
		"""Undos the last move."""
		if len(self.moves) > 0:
			last_move = self.moves[-1]
			last_move.cir_color = WHITE

			self.turn -= 1

			del self.moves[-1]

	def handle_click(self, click_pos):
		"""Handles user input via the mouse."""
		clicked = [s for s in self.slots if s.rect.collidepoint(click_pos)]
		
		if len(clicked):
			self.turn += clicked[0].update_value()

	def check_win(self):
		"""Checks if a player has won or if the game is a draw."""
		if len(self.moves) > 0:

			def filter_next(cur_slot, potential_slot, direction):
				column = cur_slot.column + direction[0]
				row = cur_slot.row + direction[1]

				return row == potential_slot.row and column == potential_slot.column

			def check_adjacent(slot, axis, direction, reversed=False):
				"""
				Checks how many consecutive slots in a specified 
				direction are the same colour.
				"""
				dir = list(map(lambda s: s * -1, direction)) if reversed else direction

				cur_slot = axis[-1] if not reversed else axis[0 if len(axis) == reversed else -1]
				
				next_slot = list(filter(lambda s: filter_next(cur_slot, s, dir), self.slots))
				# ^ get next slot based off of direction of current slot

				if not len(next_slot) > 0: # if there is no next slot (edge of board)
					if not reversed: # go other way if havent already
						check_adjacent(axis[0], axis, direction, len(axis))
					else: # or end
						return
				else:
					next_slot = next_slot[0] # eliminate list
					
					if cur_slot.cir_color == next_slot.cir_color:
						# if the next slot is the same color as cur slot
						axis.append(next_slot)
						check_adjacent(next_slot, axis, direction, reversed)
					else:
						if not reversed:
							check_adjacent(axis[0], axis, direction, len(axis))
						else:
							return
			
			last_move = self.moves[-1]

			adjacent_slots = []
			axises = [(1, 0), (0, 1), (1, 1), (-1, 1)]
			# all of the axex that the player could win by
			
			for axis in axises:
				moves = [last_move]
				check_adjacent(moves[0], moves, axis)
				adjacent_slots.append(moves)
			
			winning_axes = list(filter(lambda l: len(l) >= 4, adjacent_slots))
			# any axis that has 4 or more slots of the same color is
			# a 'winning axis'

			if len(winning_axes):

				self.winner = winning_axes[0][0].cir_color
				
				for i, s in enumerate(winning_axes[0]):
					if i < 4:
						s.cir_color = BLACK

			if len(list(filter(lambda s: s.cir_color == WHITE, self.slots))) == 0:
				# if all slots are filled but no one has won, declare draw
				self.winner = None

			if self.winner is not False:
				self.font = pygame.font.SysFont("timesnewroman", 54)

	def handle_win(self):
		"""Displays a winning message after a player won or a draw message."""
		WIN.fill(WHITE)
		
		msg = []
		if self.winner == RED:
			msg.append(self.font.render("RED won.", False, RED))
		elif self.winner == YELLOW:
			msg.append(self.font.render("YELLOW won.", False, YELLOW))
		elif self.winner is None:
			msg.append(self.font.render("It's a draw.", False, WHITE))

		msg = msg[0]
		
		r = msg.get_rect()
		w, h = r.w, r.h
		sx, sy = WIN.get_size()
		WIN.blit(msg, ((sx / 2) - (w / 2), (sy / 2) - (h / 2)))

	def handle_events(self):
		"""Handles the event loop."""
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
				
			if event.type == pygame.MOUSEBUTTONDOWN and self.winner is False:
				pos = pygame.mouse.get_pos()
				self.handle_click(pos)
				self.check_win()

			if event.type == pygame.KEYDOWN:
				keys = pygame.key.get_pressed()
				if keys[pygame.K_r]:
					self.start_match()
				if keys[pygame.K_q]:
					pygame.quit()
					exit()
				if keys[pygame.K_u] and self.winner is False:
					self.undo()

	def draw(self):
		"""Draws everything to the board."""
		for slot in self.slots:
			highlighted = False
			highlighted_slot = [s for s in self.slots if s.rect.collidepoint(pygame.mouse.get_pos())]
			if len(highlighted_slot):
				highlighted = slot.column == highlighted_slot[0].column
			
			pygame.draw.rect(WIN, slot.color if not highlighted else tuple(map(lambda v: math.floor(v * (3/4)), slot.color)), slot)
			pygame.draw.circle(WIN, slot.cir_color, (slot.rect.x + (ss / 2), slot.rect.y + (ss / 2)), ss * (2/5))
		
		if self.winner is not False:
			self.handle_win()

	def update(self):
		"""Executes the main gameplay loop."""
		WIN.fill(self.config["border_color"])
		
		self.handle_events()
			
		self.draw()
		
		pygame.display.update()
		self.timer.tick(self.config["FPS"])

def main():
    pygame.init()
    game = Game(config)
    game.start_match()

if __name__ == "__main__":
    main()