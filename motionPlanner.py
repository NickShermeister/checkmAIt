""" Wiz-nerds 2018
Olin College Passionate Pursuit

Requires: networkx, numpy
to install: pip3 install networkx
"""

import networkx as nx
import numpy as np
from datatypes import *

import time

class MotionPlanner(object):
	""" Contains a graph of spaces on a
	chessboard. Given a string, decides
	the best path to complete the motion
	"""

	def __init__(self):
		self.file_range = np.arange(0, 8) # rows
		self.rank_range = np.arange(-3, 11) # columns
		self.start_board()

		self.made_way_flag = False # May need to toggle if something moved out of the way
		self.made_way_coord = tuple() # Where the thing moved to
		self.contested_space = tuple() # space being fought over
		self.loop_count = 0 # counter to prevent infinite loop

	def start_board(self):
		""" Sets all the spaces that are occupied
		at game start as occupied
		"""
		self.occupied_spaces = set()
		player_space = np.arange(0, 8)

		self.spaces = {}
		for i in np.arange(-4, 12):
			for j in np.arange(-1, 9):
				self.spaces[(i,j)] = PieceCoord(i,j)

		# One player side taken out
		for space in player_space:
			self.occupied_spaces.add(self.spaces[(space, 0)]) # player row 1
			self.occupied_spaces.add(self.spaces[(space, 1)]) # player row 2
			self.occupied_spaces.add(self.spaces[(space, 6)]) # ai row 1
			self.occupied_spaces.add(self.spaces[(space, 7)]) # ai row 2

	def create_board_graph(self, coord:PieceCoord):
		""" Given the coordinates of the piece
		to be moved, creates a graph with all
		possible movements.

		coord: PieceCoord of our piece coordinates
		"""

		self.board = nx.Graph()
		self.loop_count = 0
		for i in self.rank_range:
			for j in self.file_range:
				edge_list = [(self.spaces[(i,j)], self.spaces[(i,j-1)], 1.0),
							(self.spaces[(i,j)], self.spaces[(i,j+1)], 1.0),
							(self.spaces[(i,j)], self.spaces[(i-1,j)], 1.0),
							(self.spaces[(i,j)], self.spaces[(i+1,j)], 1.0),
							(self.spaces[(i,j)], self.spaces[(i-1,j-1)], 1.414),
							(self.spaces[(i,j)], self.spaces[(i-1,j+1)], 1.414),
							(self.spaces[(i,j)], self.spaces[(i+1,j-1)], 1.414),
							(self.spaces[(i,j)], self.spaces[(i+1,j+1)], 1.414)]
				self.board.add_weighted_edges_from(edge_list)

		# remove nodes that shouldn't exist
		for j in self.rank_range:
			try:
				self.board.remove_node(self.spaces[(-1,j)])
				self.board.remove_node(self.spaces[(8,j)])
			except:
				pass

		for i in self.file_range:
			try:
				self.board.remove_node(self.spaces[(i,-1)])
				self.board.remove_node(self.spaces[(i,14)])
			except:
				pass

		for space in self.occupied_spaces - {self.spaces[(coord.x, coord.y)]}:
			for edge in self.board.edges(space.as_tuple()):
				self.board[edge[0]][edge[1]]['weight'] += 2

	def find_path(self, start:PieceCoord, end:PieceCoord) -> [PieceCoord]:
		""" Given the starting and ending
		coordinates, calculates the shortest
		path through
		"""
		self.create_board_graph(start)
		if self.spaces[(end.x,end.y)] not in self.board.nodes():
			print("Ending Coordinate not found")
			return []

		s = (start.x, start.y)
		e = (end.x, end.y)
		try: return nx.shortest_path(self.board, self.spaces[s], self.spaces[e], weight = 'weight')

		except nx.exception.NetworkXNoPath: 
			print("No path found")
			return []

	def make_command_list(self, move:PieceMove) -> [Action]:
		""" Given a string that specifies the
		starting and ending coordinates, returns
		a list of strings detailing the moves
		that the arm must make.
		"""
		self.loop_count += 1
		print(self.loop_count)
		instruction_list = []
		if self.spaces[move.start.as_tuple()] not in self.occupied_spaces:
			print(str(move.start) + " is not an occupied space")
			return []
		if self.loop_count < 5:
			self.occupied_spaces -= {move.start}
			path = self.find_path(move.start, move.end)
			last = move.start
			instruction_list.append(Action().PenDown())
			instruction_list.append(Action().GotoCoord(move.start))
			instruction_list.append(Action().PenUp())

			for node in path[1:]:
				if node in self.occupied_spaces:
					instruction_list = instruction_list + self.make_way(last, node, path)
				instruction_list.append(Action().GotoCoord(node))
				last = node

			instruction_list.append(Action().PenDown())
			self.occupied_spaces.add(move.end)
			if self.made_way_flag:
				print("returning piece...")
				instruction_list = instruction_list + self.return_moved()
		self.print_board()
		return instruction_list

	def make_way(self, start_coord:PieceCoord, in_way_coord:PieceCoord, path_list) -> [Action]:
		""" Given a coordinate, moves the piece there
		to an unoccupied space nearby that is not in
		the path_list.
		"""
		instruction_list = [Action().PenDown()]
		self.contested_space = in_way_coord
		for space in self.board.neighbors(in_way_coord):
			if space not in self.occupied_spaces and space not in path_list:
				move = PieceMove(in_way_coord, space)
				instruction_list = instruction_list + self.make_command_list(move)
				self.made_way_coord = space
				break
		instruction_list.append(Action().GotoCoord(start_coord))
		instruction_list.append(Action().PenUp())
		self.made_way_flag = True
		return instruction_list

	def print_board(self):
		""" Prints the board """
		board = ""
		for j in reversed(self.file_range):
			board = board + "|"
			for i in self.rank_range:
				if self.spaces[(i,j)] in self.occupied_spaces:
					board = board + "X|"
				else:
					board = board + " |"
			board = board + "\n"
		print(board)

	def return_moved(self) -> [Action]:
		""" Returns a moved piece to its starting position """
		self.made_way_flag = False
		move = PieceMove(self.made_way_coord, self.contested_space)

		return self.make_command_list(move)

	# def capture(self, move:PieceMove):
	# 	""" Not sure what this is for """
	# 	path = self.find_path(move.start, move.end)
	# 	print("Path:", path)
	# 	if len(path) == 1:
	# 		return path[0]
	# 	return path[-2]
	def test(self, move):
		""" Waits to receive a string.
		when the string is received,
		creates a list of commands to
		pass onward.
		"""
		instruction_list = self.make_command_list(move)
		for instruction in instruction_list:
			print("Sending Command: ")
			print(instruction)

if __name__ == '__main__':
	mp = MotionPlanner()
	mp.test(PieceMove(PieceCoord(2,1), PieceCoord(3,4)))
