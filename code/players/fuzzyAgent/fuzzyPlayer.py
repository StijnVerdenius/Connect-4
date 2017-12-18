
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
		self.one = fuzz.fuzzySystem2()


	# def recursion(self, board, dataentryBuildupX, dataentryBuildupO, symbol):
	# 	anyV = board.anyVictory()

	# 	if(anyV == "X" and symbol == "O"):
	# 		return 11,-1
	# 	elif(anyV == "O" and symbol == "X"):
	# 		return -1, 11

	# 	moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
	# 	moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 
	# 	dataentryBuildupX = dataentryBuildupX + moveScoreNowX
	# 	dataentryBuildupO = dataentryBuildupO + moveScoreNowO

	# 	if (len(dataentryBuildupX) == (len(self.one.reasoner.inputs)-1)):

	# 		# print dataentryBuildupX+[board.movesMade]
	# 		# print dataentryBuildupO+[board.movesMade]

	# 		X = self.one.reasoner.inference(dataentryBuildupX+[board.movesMade])
	# 		O = self.one.reasoner.inference(dataentryBuildupO+[board.movesMade])

	# 		return X,O

	# 	else:
	# 		X, O = 0,0
	# 		for move in board.possibleMoves():
	# 			newboard = deepcopy(board)
	# 			newboard.doMove(move, newboard.onMove)

	# 			X1, O1 = self.recursion(newboard, deepcopy(dataentryBuildupX), deepcopy(dataentryBuildupO), symbol)

	# 			if ((X1 == 11 or X1 == -1) and (O1 == 11 or O1 == -1)):
	# 				return X1, O1

	# 			X += X1
	# 			O += O1

	# 		return ((X+0.0)/len(board.possibleMoves())), ((O+0.0)/len(board.possibleMoves()))




	# def decideMove(self, board, symbol, arguments):
	# 	""" decides best move """

	# 	bestMove = (-1,-2)
	# 	totalscoreOpp = 0
	# 	totalScoreSelf = 0

	# 	thres = arguments[0]

	# 	moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
	# 	moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 



	# 	for move in board.possibleMoves():
	# 		newboard = deepcopy(board)
	# 		newboard.doMove(move, symbol)

	# 		X,O = self.recursion(newboard, moveScoreNowX, moveScoreNowO, symbol)

	# 		if (symbol == "X"):
	# 			if ( X > O+thres and X > bestMove[1]):
	# 				bestMove = (move, X)
	# 		elif (symbol == "O"):
	# 			if ( O > X+thres and O > bestMove[1]):
	# 				bestMove = (move, O)



	# 		print "move : " , move, "score { X:", X, " O:", O, "}"
		

	# 	if (bestMove[0] == -1):
	# 		return (choice(board.possibleMoves()), 0)
	# 	else:
	# 		return bestMove


	def decideMove(self, board, symbol, arguments):
		""" decides best move """


		 
		
		totalscoreOpp = 0
		totalScoreSelf = 0

		opp = "O"
		if (symbol == "O"):
			opp = "X"

		symbolelement = "'"+opp+"', "
		emptyslot = "' ', "

		schaak = (emptyslot + symbolelement*3 +emptyslot)[:-2]

		thres = arguments[0]

		moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
		moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 

		bestMove = (-1, -1000000000000)

		moveList = [-100000000000]*8

		for move in board.possibleMoves():

			
			
			moveScore = 0
			newboard = deepcopy(board)
			newboard.doMove(move, symbol)

			X = 0
			O = 0

			moveScoreOneX = [newboard.countPotentials("X")] + list(newboard.countWinIn(2,"X")[:-1])  
			moveScoreOneO = [newboard.countPotentials("O")] + list(newboard.countWinIn(2,"O")[:-1])


			


			for moveNew in newboard.possibleMoves():
				newNewboard = deepcopy(newboard)
				newNewboard.doMove(moveNew, opp)

				

				if (newNewboard.checkVictory(opp)):
					moveScore += -120*len(board.possibleMoves())

				if (newNewboard.checkBoard(schaak) and not board.checkBoard(schaak)):
					
					moveScore += -90*len(board.possibleMoves())
					
					

				moveScoreTwoX = [newNewboard.countPotentials("X")] + list(newNewboard.countWinIn(2,"X")[:-1])  
				moveScoreTwoO = [newNewboard.countPotentials("O")] + list(newNewboard.countWinIn(2,"O")[:-1])


				X1 = self.one.reasoner.inference(moveScoreTwoX+moveScoreOneX+moveScoreNowX+[board.movesMade])
				O1 = self.one.reasoner.inference(moveScoreTwoO+moveScoreOneO+moveScoreNowO+[board.movesMade])
				
				S = X1-O1
				if (symbol == "O"):
					S = O1-X1


				X += X1
				O += O1

				moveScore += S

			if (newboard.checkVictory(symbol)):
				moveScore = 100*len(board.possibleMoves())


			moveScore = moveScore/len(board.possibleMoves())

			X,O = ((X+0.0)/len(board.possibleMoves())), ((O+0.0)/len(board.possibleMoves()))



			if ( moveScore > bestMove[1]):
				print "nieuw", bestMove
				bestMove = (move, moveScore)

			moveList[move-1] = moveScore


			print "move : " , move, "score { X:", X, " O:", O, "} ", moveScore

		

		oldMax = max(moveList)
		secondMoveList = deepcopy(moveList)
		bestmoves = []
		while (len(secondMoveList) > 0 and max(secondMoveList) == oldMax):
			oldMax = max(secondMoveList)
			ind1 = moveList.index(oldMax)
			moveList[ind1] = -11000000
			ind2 = secondMoveList.index(oldMax)
			secondMoveList.pop(ind2)
			bestmoves.append(ind1+1)



		return (choice(bestmoves), 11)




















	# 		print "move : " , move, "score { X:", X, " O:", O, "}"
		

	# 	if (bestMove[0] == -1):
	# 		return (choice(board.possibleMoves()), 0)
	# 	else:
	# 		return bestMove
		


	def decideMovesInOrder(self, board, symbol, arguments):
		""" decides moves in order of score """

		pass