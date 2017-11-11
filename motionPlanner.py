""" HackHolyoke 2017
checkmAIt

Given a starting coordinate pair
and an ending coordinate pair,
outputs commands to navigate the
arm to that place, grab the piece,
navigate the board, and release the
piece.

Requires: networkx, numpy 
"""
import networkx as nx
import numpy as np
#import serial

class MotionPlanner(object):
	""" Contains a graph of spaces on a
	chessboard. Given a string, decides
	the best path to complete the motion
	"""

	def __init__(self):
		self.start_board()

		# Create some repetative strings
		self.grab_str = str.encode('U \n\n')
		self.release_str = str.encode('D \n\n')
		#self.ser = serial.Serial('/dev/tty.usbserial', 9600)

	def create_board_graph(self, piece_place):
		""" Given the coordinates of the piece
		to be moved, creates a graph with all
		possible movements.

		piece_place: tuple of our piece coordinates
		"""
		self.board = nx.Graph()
		file_range = np.arange(-1.0, 9.0)
		column_range = np.arange(-2.0,10.0)

		for i in column_range:
			for j in file_range:
				edge_list = [((i,j),(i,j-1.0), 1.0),
							((i,j),(i,j+1.0), 1.0),
							((i,j),(i-1.0,j), 1.0),
							((i,j),(i+1.0,j), 1.0),
							((i,j),(i-1.0,j-1.0), 1.414),
							((i,j),(i-1.0,j+1.0), 1.414),
							((i,j),(i+1.0,j+1.0), 1.414),
							((i,j),(i+1.0,j-1.0), 1.414)]
				self.board.add_weighted_edges_from(edge_list)

		for space in (self.occupied_spaces - {piece_place}):
			self.board.remove_node(space)

	def find_path(self, start, end):
		""" Given the starting and ending
		coordinates, calculates the shortest
		path through
		"""
		self.create_board_graph(start)
		if end not in self.board.nodes():
			print("Ending Coordinate not found")
			return []

		try: return nx.shortest_path(self.board, start, end, weight = 'weight')

		except nx.exception.NetworkXNoPath: return []

	def start_board(self):
		""" Sets all the spaces that are occupied
		at game start as occupied, all 
		"""
		self.occupied_spaces = set()

		# Fake top and bottom files get erased
		for space in zip(np.arange(-3.0, 11.0), [0]*14):
			self.occupied_spaces.add(space)
		for space in zip(np.arange(-3.0, 11.0), [9]*14):
			self.occupied_spaces.add(space)

		# Fake left and right columns get erased
		for space in zip([-2.0]*12, np.arange(-2.0, 10.0)):
			self.occupied_spaces.add(space)
		for space in zip([9.0]*12, np.arange(-2.0, 10.0)):
			self.occupied_spaces.add(space)

		# One player side taken out
		for space in zip(np.arange(0.0, 8.0), [0.0]*8):
			self.occupied_spaces.add(space)
		for space in zip(np.arange(0.0, 8.0), [1.0]*8):
			self.occupied_spaces.add(space)

		# Second player side taken out
		for space in zip(np.arange(0.0, 8.0), [7.0]*8):
			self.occupied_spaces.add(space)
		for space in zip(np.arange(0.0, 8.0), [6.0]*8):
			self.occupied_spaces.add(space)

	def parse_string(self, mv_str):
		""" Given a string that specifies
		starting and ending coordinates,
		returns the starting and ending
		coordinates as tuples
		mv_str = 
		'startcolumn startfile -> endcolumn endfile \n\n'

		returns: start_coord, end_coord
		"""
		sc, sf, arrow, ec, ef, nl = mv_str.split(' ')
		start_coord = (float(sc), float(sf))
		end_coord = (float(ec), float(ef))

		return start_coord, end_coord

	def make_command_strings(self, mv_str):
		""" Given a string that specifies the
		starting and ending coordinates, returns
		a list of strings detailing the moves
		that the arm must make.
		mv_str = 
		'startcolumn startfile -> endcolumn endfile \n\n'
		
		returns: list of strings formatted as:
			['M %f %f \n\n', 'U \n\n' ... 'D \n\n']
		"""
		start_coord, end_coord = self.parse_string(mv_str)
		self.occupied_spaces -= {start_coord}
		path = self.find_path(start_coord, end_coord)
		instruction_list = [self.move_string(start_coord), self.grab_str]
		for node in path:
			instruction_list.append(self.move_string(node))

		instruction_list.append(self.release_str)
		self.occupied_spaces.add(end_coord)
		return instruction_list

	def move_string(self, coord):
		""" Given a coordinate tuple,
		returns a string that fits the format
		'M float float'
		"""
		return str.encode('M ' + str(coord[0]) + ' ' + str(coord[1]) + ' \n\n')

	def run(self, mv_str):
		""" Waits to receive a string.
		when the string is received,
		creates a list of commands to
		pass onward.
		"""
		mv_string = mv_str #get string
		instruction_list = self.make_command_strings(mv_str)
		for instruction in instruction_list:
			print(instruction)
			#self.ser.write(instruction)


if __name__ == '__main__':
	mp = MotionPlanner()
	strings = mp.run("2.0 4.0 -> 6.0 4.0 \n\n")
