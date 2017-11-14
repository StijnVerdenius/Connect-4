
import numpy as np
import time
from copy import deepcopy
from random import choice
import boardDef
import skfuzzy as fuzz



class algorithm:
	def __init__(self):
		pass

	def decideMove(self, board, symbol, arguments):
		""" decides best move """

		recursionLevel = arguments[0]
		_ = None
		return (board.possibleMoves()[0] , _)


	def decideMovesInOrder(self, board, symbol, arguments):
		""" decides moves in order of score """

		pass