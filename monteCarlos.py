

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

	
	def decideMove(self, board, symbol, timelimit):
		bestmove = (-1,-1)

		for move in board.possibleMoves():
			movescore = self.simulateMove(board,symbol,timelimit, move)
			if (movescore > bestmove[1]):
				bestmove = (move, movescore)
			print "move : " , move, "score : ", str(100.0*movescore)[:5]
		return bestmove

	def decideMovesInOrder(self, board, symbol, timelimit):
		moves = []

		for move in  board.possibleMoves():
			movescore = self.simulateMove(board,symbol,timelimit, move)
			moves.append(movescore)
		return moves

	

	def simulateMove(self, board,symbol,timelimit, move):
		simulationScore = 0.0
		simulationAmount = 0.0
		cross = False
		if(symbol == "X"):
			cross = True
		
		start = time.time()
		while( (time.time() - start) < timelimit):

			simulationScore  += self.simulation(deepcopy(board), cross, move, symbol)
			simulationAmount += 1.0
		
		return (simulationScore/simulationAmount)

	
	def simulation(self, board, cross, move, symbol):
		winner = False
		score = 0.0
		crossTurn = False
		board.doMove(move, symbol)
		if (not cross):
			crossTurn = True


		if (cross):# check victory conditions
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
		while (not winner):
			
			possible = board.possibleMoves()

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
			

			if (cross):# check victory conditions
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




