import curses
from operator import itemgetter

stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)

height, width = stdscr.getmaxyx()

# Limits
height_lim = height - 2 
width_lim = width - 1 

game_window = curses.newwin(height, width, 0, 0)
game_window.keypad(True)
game_window.timeout(100)
game_window.clear()

# Init invaders
invaders_move = 1
invaders = []

for y in range(2,5):
	for x in range(int(width*0.3), int(width*0.7), 2):
		invaders.append([y,x])

# Init spaceship
spaceship = width//2
rockets = []


while True:
	game_window.clear()

	# Game Over
	if not invaders or max(inv[0] for inv in invaders) == height_lim :
		curses.endwin()
		quit()
	
	# Draw invaders
	[game_window.addch(y, x, ord('W')) for y,x in invaders]
	# Draw rockets
	[game_window.addch(y, x, ord('!')) for y,x in rockets]
	# Draw spaceship
	game_window.addch(height_lim, spaceship, ord('M'))


	# Listen to input
	key = game_window.getch()

	# Actions : move spaceship or fire rocket
	if key == 32: # Space
	    rockets.append([height_lim, spaceship])
	elif key == curses.KEY_RIGHT and spaceship < width_lim:
	    spaceship = spaceship + 1
	elif key == curses.KEY_LEFT and spaceship > 0:
	    spaceship = spaceship - 1

	# Remove off-screen rockets
	rockets = list(filter(lambda rocket: rocket[0] > 0, rockets))

	# Move rockets
	for rocket in rockets:
		rocket[0] = rocket[0] - 1

	# Move invaders
	if max(inv[1] for inv in invaders) == width_lim or min(inv[1] for inv in invaders) == 0:
		invaders_move = invaders_move * -1
		# Vertical move
		invaders = list(map(lambda invader: [invader[0] + 1, invader[1]], invaders))

	# Horizontal move	
	invaders = list(map(lambda invader: [invader[0], invader[1] + invaders_move], invaders))
	
	# Remove destroyed invaders/rockets
	for rocket_idx, rocket in enumerate(rockets[:]):
		for invader_idx, invader in enumerate(invaders[:]):
			if rocket == invader:
				invaders.pop(invader_idx)
				rockets.pop(rocket_idx)
