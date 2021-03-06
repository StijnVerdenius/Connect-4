
import numpy as np
import time
from copy import deepcopy
from random import choice
import boardDef

import fuzzySystems as fuzz


"""
Holds the basic playing mechanism of the fuzzy agents

"""

class algorithm:


	def __init__(self):
		self.one = fuzz.fuzzySystem2()


	

	def decideMove(self, board, symbol, arguments):
		""" decides best move """

		# initialize score parameters
		totalscoreOpp = 0
		totalScoreSelf = 0

		# determine opponent
		opp = "O"
		if (symbol == "O"):
			opp = "X"

		# defense measure 1/2 initialisation for agent 3
		symbolelement = "'"+opp+"', "
		emptyslot = "' ', "
		schaak = (emptyslot + symbolelement*3 +emptyslot)[:-2]

		# determine inputvariables for current board
		moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
		moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 

		# initialize score parameters with exceptionally low scores so it will always find something better
		bestMove = (-1, -1000000000000)
		moveList = [-100000000000]*8

		# expand searchtree with own moves
		for move in board.possibleMoves():
			
			# the descsion needs to be made on own moves so keep score
			moveScore = 0

			# do the move
			newboard = deepcopy(board)
			newboard.doMove(move, symbol)

			# move specific score parameters (only for debugging)
			X = 0
			O = 0

			# determine inputvariables on newboard
			moveScoreOneX = [newboard.countPotentials("X")] + list(newboard.countWinIn(2,"X")[:-1])  
			moveScoreOneO = [newboard.countPotentials("O")] + list(newboard.countWinIn(2,"O")[:-1])

			# expand searchtree with opponent moves
			for moveNew in newboard.possibleMoves():
				newNewboard = deepcopy(newboard)
				newNewboard.doMove(moveNew, opp)

				# defense measure 2/2 for agent 3
				if (newNewboard.checkVictory(opp)):
					moveScore += -120*len(board.possibleMoves())

				# defense measure 1/2 for agent 3
				if (newNewboard.checkBoard(schaak) and not board.checkBoard(schaak)):
					
					moveScore += -90*len(board.possibleMoves())
					
				# determine inputvariables on newnewboard
				moveScoreTwoX = [newNewboard.countPotentials("X")] + list(newNewboard.countWinIn(2,"X")[:-1])  
				moveScoreTwoO = [newNewboard.countPotentials("O")] + list(newNewboard.countWinIn(2,"O")[:-1])

				# fuzzy inference, determine quality of 
				X1 = self.one.reasoner.inference(moveScoreTwoX+moveScoreOneX+moveScoreNowX+[board.movesMade])
				O1 = self.one.reasoner.inference(moveScoreTwoO+moveScoreOneO+moveScoreNowO+[board.movesMade])
				
				# determine difference
				S = X1-O1
				if (symbol == "O"):
					S = O1-X1

				# add to own-move-specific trackers (only for debugging)
				X += X1
				O += O1

				# add to movescore
				moveScore += S

			# to make sure if victorious situation pops up, thats the best option
			if (newboard.checkVictory(symbol)):
				moveScore = 100*len(board.possibleMoves())

			# take the average of the movescore
			moveScore = moveScore/len(board.possibleMoves())

			# (only for debugging)
			X,O = ((X+0.0)/len(board.possibleMoves())), ((O+0.0)/len(board.possibleMoves()))



			

			# place move in correct bin
			moveList[move-1] = moveScore



			# (only for debugging)
			print "move : " , move#, "score { X:", X, " O:", O, "} ", moveScore
			# if ( moveScore > bestMove[1]):
			# 	print "nieuw", bestMove
			# 	bestMove = (move, moveScore)

		
		# determine best move out of the results
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


		# return move
		return (choice(bestmoves), 11)






	def recursion(self, board, dataentryBuildupX, dataentryBuildupO):
		""" Determins bestmove in recursion way instead of hardcoded (unused atm) """

		# note: a more elegant solution, but not needed atm


		anyV = board.anyVictory()

		# basecase1
		if(anyV == "X"):
			return 11,-1
		elif(anyV == "O"):
			return -1, 11

		moveScoreNowX = [board.countPotentials("X")] + list(board.countWinIn(2,"X")[:-1])  
		moveScoreNowO = [board.countPotentials("O")] + list(board.countWinIn(2,"O")[:-1]) 
		dataentryBuildupX = dataentryBuildupX + moveScoreNowX
		dataentryBuildupO = dataentryBuildupO + moveScoreNowO

		# basecase2
		if (len(dataentryBuildupX) == (len(self.one.reasoner.inputs)-1)):

			X = self.one.reasoner.inference(dataentryBuildupX+[board.movesMade])
			O = self.one.reasoner.inference(dataentryBuildupO+[board.movesMade])

			return X,O

		else:

			#recursion
			X, O = 0,0
			for move in board.possibleMoves():
				newboard = deepcopy(board)
				newboard.doMove(move, newboard.onMove)

				X1, O1 = self.recursion(newboard, deepcopy(dataentryBuildupX), deepcopy(dataentryBuildupO))

				# if victorious situation underneath, let them know above
				if ((X1 == 11 or X1 == -1) and (O1 == 11 or O1 == -1)):
					return X1, O1

				X += X1
				O += O1

			return ((X+0.0)/len(board.possibleMoves())), ((O+0.0)/len(board.possibleMoves()))









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







	# 		print "move : " , move, "score { X:", X, " O:", O, "}"
		

	# 	if (bestMove[0] == -1):
	# 		return (choice(board.possibleMoves()), 0)
	# 	else:
	# 		return bestMove
		


	def decideMovesInOrder(self, board, symbol, arguments):
		""" decides moves in order of score """

		pass