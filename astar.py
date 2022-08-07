from re import T
import pygame
import math
from queue import PriorityQueue

# Configures the display surface
WIDTH = 800
DISPLAY = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Game")

RED = (250,128,114)
GREEN = (0, 255, 0)
BLUE = (0,191,255)
GREY = (128,128,128)
SILVER = (192,192,192)
ORANGE = (255,127,80)
VIOLET = (238,130,238)
TURQUOISE = (64, 224, 208)
YELLOW = (255, 255, 0)
WHITE = (255,250,250)

"""
The Node class represents the individual squares in the display map.
These are initialized in the color white, storing variables such as its position, width,
color (which determines its state), and a list of its adjacent neighbors.
"""
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == TURQUOISE

	def is_open(self):
		return self.color == BLUE
	
	def is_start(self):
		return self.color == VIOLET

	def is_end(self):
		return self.color == RED

	def is_wall(self):
		return self.color == GREY

	def reset(self):
		self.color = WHITE
	
	def make_start(self):
		self.color = VIOLET

	def make_end(self):
		self.color = RED

	def make_wall(self):
		self.color = GREY
	
	def make_open(self):
		self.color = BLUE

	def make_closed(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = ORANGE

	def draw(self, display):
		# Draws a rectangle on the given game surface at a specific node: 
		# rect(surface, color, (rect pos, rect dimensions))
		pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		# List that will contain 2, 3, or 4 neighbors depending on the node's position
		self.neighbors = []
		# If down, up, right, or left exist (and are not walls), they are added to neighbors
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
			self.neighbors.append(grid[self.row + 1][self.col]) # Down

		if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
			self.neighbors.append(grid[self.row - 1][self.col]) # Up

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): 
			self.neighbors.append(grid[self.row][self.col + 1]) # Right

		if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
			self.neighbors.append(grid[self.row][self.col - 1]) # Left

	def __lt__(self, other):
		return False

"""
The H-score returns an estimate of the distance from p1 to p2.
The 'Manhattan distance' is the sum of the absolute differences between the two vectors.
Thus, it is an absolute distance function, commonly used in Taxicab geometry.

Space: O(1)
Time: O(1)
"""
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

"""
Draws the optimal path (once found) on the game display.

Space: O(1)
Time: O(length of path) = O(n)
"""
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


"""
A* algorithm is a better performing extension of Dijkstra’s algorithm in that it can be used to
find the shortest path from point A to B, all while achieving better performance through the use
of heuristics to guide its search. 

At each iteration of its main loop, A* figures out which of its paths to extend. It does so based
on the cost of a path and the estimated cost required to extend this path all the way to the goal. 

Specifically, A* selects the path that minimizes f(n)=g(n)+h(n)

... where n is the next node on the path, g(n) is the cost of the path from the start node to n, 
and h(n) is a heuristic function that estimates the cost of the direct path from n to the goal.

Space: O(n)
Time: O(nlogn)

The space complexity of A* is roughly the same as that of all other graph search algorithms, as it
keeps all generated nodes in memory. In practice, this turns out to be the biggest drawback of A*
search, leading to the development of memory-bounded heuristic searches, such as Iterative deepening
A*, memory bounded A*, and SMA*.
"""
def astar_search(draw, grid, start, end):
	open_set = PriorityQueue()
	# Count serves as a tie-breaker in case two nodes have the same F-score
	count = 0
	# Adds the start node to the PQ, with an F-score and count of 0
	open_set.put((0, count, start))
	# Dictionary that keeps track of the path to a certain node
	came_from = {}
	# The G-score is the current shortest distance to get from start to current node
	g_score = {node: float("inf") for row in grid for node in row}
	# The start node's g_score is 0
	g_score[start] = 0
	# The F-score is the addition of the H-score and the G-score
	f_score = {node: float("inf") for row in grid for node in row}
	# The start node's f_score is 0 + h_score
	f_score[start] = h(start.get_pos(), end.get_pos())
	# This will store the same values as open_set for quick lookups
	open_set_hash = {start}

	# A Star runs until the open_set is empty (we have considered all of the necessary nodes)
	while open_set:
		for event in pygame.event.get():
			# Lets the player quit the program while the algorithm is running
			if event.type == pygame.QUIT:
				pygame.quit()

		# Gets the current highest-priority node from the PQ
		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			# End was popped from the priority queue (this path had the lowest F-score)
			# The optimal path search is over and we can now draw the solution on the display
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		# Iterates through all the node's neighbors
		for neighbor in current.neighbors:
			# Potential new g_score for the neighbor node
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				# A shorter path was found from the start to the neighbor
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		# Calls the Lambda function that was given as an argument
		draw()

		if current != start:
			current.make_closed()

	return False


"""
Returns a 2-D Array for the Pathfinding game called grid, containing (rows * rows) total Nodes.
All nodes are initialized as WHITE squares with equal widths.

Space: O(nodes) = O(1)
Time: O(nodes) = O(1)
"""
def create_grid(rows, display_width):
	pygame.display.set_caption("Pathfinding Game")
	grid = []
	node_width = display_width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, node_width, rows)
			grid[i].append(node)

	return grid


"""
Draws all the grid lines on the display.

Space: O(1)
Time: O(rows) = O(1)
"""
def draw_grid(display, rows, display_width):
	node_width = display_width // rows
	for i in range(rows):
		# Draws one straight horizontal line  
		# The method is: line(surface, color, start_pos, end_pos)
		pygame.draw.line(display, SILVER, (0, i * node_width), (display_width, i * node_width))
	for j in range(rows):
		# Draws one straight vertical line
		pygame.draw.line(display, SILVER, (j * node_width, 0), (j * node_width, display_width))


"""
Draws every node in the 2-D grid on the display, then updates the display.

Space: O(1)
Time: O(nodes) = O(1)
"""
def draw(display, grid, rows, width):
	display.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(display)

	draw_grid(display, rows, width)
	pygame.display.update()


"""
Returns an integer (row, col) position based on the specific pos that was clicked by the player.

Space: O(1)
Time: O(1)
"""
def get_clicked_pos(pos, rows, display_width):
	node_width = display_width // rows
	x, y = pos

	row = x // node_width
	col = y // node_width

	return row, col


def main(display, width):
	ROWS = 80
	grid = create_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(display, grid, ROWS, width)
		for event in pygame.event.get():
			# If player exits the program, this deactivates pygame library, and ends while loop
			if event.type == pygame.QUIT:
				run = False

			# If player left-clicks:
			if pygame.mouse.get_pressed()[0]:
				# Returns the x and y position of the mouse cursor relative to the game display.
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				
				# If start does not exist, also checks start is not the same as end
				if not start and node != end:
					start = node
					start.make_start()

				# If end does not exist, also checks end is not the same as start
				elif not end and node != start:
					end = node
					end.make_end()

				# Player has created both start and end, now walls can also be created
				elif node != end and node != start:
					node.make_wall()

			# If player right-clicks:
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				# Clicked node is reset to be white
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				# Game starts if spacebar is pressed (and start and end nodes were created)
				if event.key == pygame.K_SPACE and start and end:
					# All neighbors have to update given the current state of the display
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					# Runs the A* Search Algorithm
					pygame.display.set_caption("A* Search Algorithm")
					astar_search(lambda: draw(display, grid, ROWS, width), grid, start, end)
					pygame.display.set_caption("Click R to reset the display")

				# Resets the board if player hits the "r" key after the algorithm is finished
				if event.key == pygame.K_r:
					start = None
					end = None
					grid = create_grid(ROWS, width)

	pygame.quit()

main(DISPLAY, WIDTH)