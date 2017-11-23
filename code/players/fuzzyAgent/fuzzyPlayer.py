
import numpy as np
import time
from copy import deepcopy
from random import choice
import boardDef

import fuzzySystems as fuzz


"""
Holds the basic playing mechanism of the fuzzy player

"""

class algorithm:
	def __init__(self):
		self.one = fuzz.fuzzySystem1()
		self.turn = 0
		self.two = fuzz.fuzzySystem2()

	def decideMove(self, board, symbol, arguments):
		""" decides best move """

		bestMove = (-1,-2)
		totalscoreOpp = 0
		totalScoreSelf = 0
		for move in board.possibleMoves():
			newboard = deepcopy(board)
			newboard.doMove(move, symbol)
			moveScore1 = list(newboard.evaluateBoard("X")[:-2])
			moveScore2 = list(newboard.evaluateBoard("O")[:-2])
			
			

			owngain = self.one.reasoner.inference([self.turn] + moveScore1)
			oppgain = self.one.reasoner.inference([self.turn] + moveScore2)

			totalscoreOpp += owngain
			totalScoreSelf += oppgain

			moveScore = owngain-oppgain

			if symbol == "O":
				moveScore = -1*moveScore
			if (moveScore > bestMove[1]):
				bestMove = (move, moveScore)


			
			print "move : " , move, "score : ", str(moveScore)[:5]

		if symbol == "O":
			print "evaluation state : ", self.two.reasoner.inference([totalscoreOpp, totalScoreSelf])
		else: 
			print "evaluation state : ", self.two.reasoner.inference([totalscoreOpp, totalScoreSelf][::-1])
		
		self.turn += 1
		return bestMove
		return (board.possibleMoves()[0] , _)


	def decideMovesInOrder(self, board, symbol, arguments):
		""" decides moves in order of score """

		pass