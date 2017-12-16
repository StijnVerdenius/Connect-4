
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


	def recursion(self, board, dataentryBuildupX, dataentryBuildupO):
		anyV = board.anyVictory()

		if(anyV == "X"):
			return 11,-1
		elif(anyV == "O"):
			return -1, 11

		moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
		moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 
		dataentryBuildupX = dataentryBuildupX + moveScoreNowX
		dataentryBuildupO = dataentryBuildupO + moveScoreNowO

		if (len(dataentryBuildupX) == (len(self.one.reasoner.inputs)-1)):

			# print dataentryBuildupX+[board.movesMade]
			# print dataentryBuildupO+[board.movesMade]

			X = self.one.reasoner.inference(dataentryBuildupX+[board.movesMade])
			O = self.one.reasoner.inference(dataentryBuildupO+[board.movesMade])
			return X,O

		else:
			X, O = 0,0
			for move in board.possibleMoves():
				newboard = deepcopy(board)
				newboard.doMove(move, newboard.onMove)

				X1, O1 = self.recursion(newboard, dataentryBuildupX, dataentryBuildupO)
				X += X1
				O += O1
			return ((X+0.0)/len(board.possibleMoves())), ((O+0.0)/len(board.possibleMoves()))




	def decideMove(self, board, symbol, arguments):
		""" decides best move """

		bestMove = (-1,-2)
		totalscoreOpp = 0
		totalScoreSelf = 0

		thres = arguments[0]

		moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
		moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 



		for move in board.possibleMoves():
			newboard = deepcopy(board)
			newboard.doMove(move, symbol)

			X,O = self.recursion(newboard, moveScoreNowX, moveScoreNowO)

			if (symbol == "X"):
				if ( X > O+thres and X > bestMove[1]):
					bestMove = (move, X)
			elif (symbol == "O"):
				if ( O > X+thres and O > bestMove[1]):
					bestMove = (move, O)



			print "move : " , move, "score { X:", X, " O:", O, "}"
		

		if (bestMove[0] == -1):
			return (choice(board.possibleMoves()), 0)
		else:
			return bestMove

		


	def decideMovesInOrder(self, board, symbol, arguments):
		""" decides moves in order of score """

		pass