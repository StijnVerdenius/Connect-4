

import numpy as np
import time
from copy import deepcopy
from random import choice
from functools import wraps
import boardDef

class algorithm:
	def __init__(self):
		pass


	def memoize(func):
		""" @function for cache use """

		cache = {}
		@wraps(func)
		def wrap(*args):
			if str(args) not in cache:
				cache[str(args)] = func(*args)	            
			return cache[str(args)]
		return wrap

	

	def decideMove(self, board, symbol, arguments):
		""" decides best move """

		bestMove = (-1,-1)
		timeLimit = arguments[0]
		for move in board.possibleMoves():
			moveScore = self.simulateMove(board,symbol,timeLimit, move)
			if (moveScore > bestMove[1]):
				bestMove = (move, moveScore)
			print "move : " , move, "score : ", str(100.0*moveScore)[:5]
		return bestMove

	def decideMovesInOrder(self, board, symbol, timeLimit):
		""" decides moves in order of score """

		moves = []

		for move in  board.possibleMoves():
			moveScore = self.simulateMove(board,symbol,timeLimit, move)
			moves.append(moveScore)
		return moves

	

	def simulateMove(self, board,symbol,timeLimit, move):
		""" take a random sample of a move by scre for a certain time limit """

		simulationScore = 0.0
		simulationAmount = 0.0
		cross = False
		if(symbol == "X"):
			cross = True
		
		# set time
		start = time.time()
		while( (time.time() - start) < timeLimit):

			simulationScore  += self.simulation(deepcopy(board), cross, move, symbol)
			simulationAmount += 1.0
		
		return (simulationScore/simulationAmount)

	
	def simulation(self, board, cross, move, symbol):
		""" does a simulation of a game by playing it out from start to end by selecting random moves """

		winner = False
		score = 0.0
		crossTurn = False

		# first do the first move
		board.doMove(move, symbol)
		if (not cross):
			crossTurn = True

		# check victory conditions
		if (cross):
			if(board.checkVictory("X")):
				winner = True
				score += 1.0
			elif(board.checkVictory("O")):
				winner = True
		else:
			if(board.checkVictory("O")):
				winner = True			
				score += 1.0
			elif(board.checkVictory("X")):
				winner = True

		# then do simulation
		while (not winner):
			
			possible = board.possibleMoves()

			# if nothing is possible the boatrd is full: it's a tie
			if (len(possible) < 1):
				winner = True
				score += 0.1
				break

			# do move
			try:
				move = choice(possible)
			except:
				break 
			if (crossTurn):
				board.doMove( move, "X")
			else:
				board.doMove( move, "O")
			
			# check victory conditions
			if (cross):
				if(board.checkVictory("X")):
					winner = True
					
					score += 1.0
					break
				elif(board.checkVictory("O")):
					winner = True
					
					break
			else:
				if(board.checkVictory("O")):
					winner = True
					
					score += 1.0
					break
				elif(board.checkVictory("X")):
					winner = True
					
					break
			crossTurn = not crossTurn
		return score




