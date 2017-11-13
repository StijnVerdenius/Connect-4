
import numpy as np


class board:
	def __init__(self, n=8, m=8):
		self.length = n
		self.height = m
		self.board = []
		for _ in range(m):
			newline = []
			for _ in range(n):
				newline.append(" ")
			self.board.append(newline)

	def possibleMoves(self):
		possible = []
		for x in range(len(self.board)):
			if (self.board[0][x] == " "):
				possible.append(x+1)
		return possible


	def doMove(self, position, symbol):
		for row in range(-self.height,0)[::-1]:

			if (self.board[row][position-1] == " "):
				
				self.board[row][position-1] = symbol
				return True
		return False

	def checkVictory(self, symbol, printing = False):
		condition =(("'"+symbol+"', ")*4)[:-2]
		
		if (not self.checkrows(symbol, condition)):
			
			if (not self.checkcollumns(symbol, condition)):
				
				if (not self.checkdiag(symbol, condition)):
		
					return False
		if (printing):
			print "WINNER : ", symbol
		return True

	def countrows(self, condition):
		counter = 0
		for row in self.board:
			counter += str(row).count(condition)
				
		return counter

	def countcollumns(self, condition):
		counter = 0
		for collumn in zip(*self.board):
			counter += str(collumn).count(condition)
		return counter

	def countdiag(self, condition):
		counter = 0
		for x in range(5):
			listi = [r[i+x] for i, r in list(enumerate(self.board))[:8-x]] + ["ban"] + [r[-i-x-1] for i, r in list(enumerate(self.board))[:8-x]] + ["ban"] + [r[i-x] for i, r in list(enumerate(self.board))[x:]] + ["ban"] + [r[-i+x-1] for i, r in list(enumerate(self.board))[x:]]
			counter += str(listi).count(condition)
		return counter



	def checkrows(self, symbol, condition):
		i = 0 
		for row in self.board:
			
			if (condition in str(row)):
				return True
			i += 1
		return False

	def checkcollumns(self, symbol, condition):
		i = 0
		for collumn in zip(*self.board):

			
			if (condition in str(collumn)):
				return True
			i += 1
		return False

	def checkdiag(self, symbol, condition):
		for x in range(5):
			
			listi = [r[i+x] for i, r in list(enumerate(self.board))[:8-x]] + ["ban"] + [r[-i-x-1] for i, r in list(enumerate(self.board))[:8-x]] + ["ban"] + [r[i-x] for i, r in list(enumerate(self.board))[x:]] + ["ban"] + [r[-i+x-1] for i, r in list(enumerate(self.board))[x:]]
			if (condition in str(listi)):
				return True
				
		return False


	def toString(self):
		stri = "\n   1   2   3   4   5   6   7   8   \n"
		for y in self.board:
			stri = stri+"|"
			for x in y:
				stri = stri +"-("+x+")"
			stri = stri+"-|\n"
		print (stri)


	def countBoard(self, condition):
		return (self.countrows(condition)+ self.countcollumns(condition)+ self.countdiag(condition))

		