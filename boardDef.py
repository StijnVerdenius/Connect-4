
import numpy as np


class board:
	def __init__(self, n=8, m=8):

		# initiation
		self.length = n
		self.height = m
		self.board = []
		for _ in range(m):
			newline = []
			for _ in range(n):
				newline.append(" ")
			self.board.append(newline)

	def possibleMoves(self):
		""" returns possible moves on a board """

		possible = []
		for x in range(len(self.board)):
			if (self.board[0][x] == " "):
				possible.append(x+1)
		return possible


	def doMove(self, position, symbol):
		""" does move on a board """

		# start from the bottom up
		for row in range(-self.height,0)[::-1]:

			# if empty, place symbol
			if (self.board[row][position-1] == " "):
				
				self.board[row][position-1] = symbol
				return True
		return False

	def checkVictory(self, symbol, printing = False):
		""" checks wether victory is been made by symbol of choice """

		condition =(("'"+symbol+"', ")*4)[:-2]
		
		if (not self.checkRows(condition)):
			
			if (not self.checkColumns(condition)):
				
				if (not self.checkDiag(condition)):
		
					return False
		if (printing):
			print "WINNER : ", symbol
		return True

	def countRows(self, condition):
		""" counts all occurences in rows for a certain pattern/condition """

		counter = 0
		for row in self.board:
			counter += str(row).count(condition)
				
		return counter

	def countColumns(self, condition):
		""" counts all occurences in columns for a certain pattern/condition """

		counter = 0
		for column in zip(*self.board):
			counter += str(column).count(condition)
		return counter

	def countDiag(self, condition):
		""" counts all occurences in diagonals for a certain pattern/condition """

		counter = 0
		for x in range(5):

			# this one is a bit complicated
			listi = [r[i+x] for i, r in list(enumerate(self.board))[:8-x]] + ["_"] + [r[-i-x-1] for i, r in list(enumerate(self.board))[:8-x]] + ["_"] + [r[i-x] for i, r in list(enumerate(self.board))[x:]] + ["_"] + [r[-i+x-1] for i, r in list(enumerate(self.board))[x:]]
			counter += str(listi).count(condition)
		return counter



	def checkRows(self, condition):
		""" checks all occurences in rows for a certain pattern/condition """

		i = 0 
		for row in self.board:
			
			if (condition in str(row)):
				return True
			i += 1
		return False

	def checkColumns(self, condition):
		""" checks all occurences in columns for a certain pattern/condition """

		i = 0
		for column in zip(*self.board):

			
			if (condition in str(column)):
				return True
			i += 1
		return False

	def checkDiag(self, condition):
		""" checks all occurences in diagonals for a certain pattern/condition """

		for x in range(5):
			
			# this one is a bit complicated
			listi = [r[i+x] for i, r in list(enumerate(self.board))[:8-x]] + ["_"] + [r[-i-x-1] for i, r in list(enumerate(self.board))[:8-x]] + ["_"] + [r[i-x] for i, r in list(enumerate(self.board))[x:]] + ["_"] + [r[-i+x-1] for i, r in list(enumerate(self.board))[x:]]
			if (condition in str(listi)):
				return True
				
		return False


	def toString(self):
		""" pretty prints board """

		stri = "\n   1   2   3   4   5   6   7   8   \n"
		for y in self.board:
			stri = stri+"|"
			for x in y:
				stri = stri +"-("+x+")"
			stri = stri+"-|\n"
		print (stri)


	def countBoard(self, condition):
		""" combine 3 count functions """

		return (self.countRows(condition)+ self.countColumns(condition)+ self.countDiag(condition))

	def checkBoard(self, condition):
		""" combine 3 check functions """

		return (self.checkRows(condition)+ self.checkColumns(condition)+ self.checkDiag(condition))

		