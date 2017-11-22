

from copy import deepcopy

class algorithm:
	def __init__(self):
		pass

	def decideMove(self, board, symbol, _):
		""" decides best move """

		bestMove = (-1,-1000000)
		for move in board.possibleMoves():
			newboard = deepcopy(board)
			newboard.doMove(move, symbol)
			moveScore1 = newboard.evaluateBoard("X")
			moveScore2 = newboard.evaluateBoard("O")
			moveScore = 0
			scores = [200,8,1]
			for i in range(3):
				moveScore += (moveScore1[i] - moveScore2[i])*scores[i]
			if symbol == "O":
				moveScore = -1*moveScore
			if (moveScore > bestMove[1]):
				bestMove = (move, moveScore)
			print "move : " , move, "score : ", str(100.0*moveScore)[:5]
		return bestMove
