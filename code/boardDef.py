
import numpy as np
from copy import deepcopy

class board:
	def __init__(self, n=8, m=8):

		# initiation
		self.length = n
		self.height = m
		self.board = []
		self.movesMade = 0
		self.onMove = "O"
		for _ in range(m):
			newline = []
			for _ in range(n):
				newline.append(" ")
			self.board.append(newline)

	def toggleMove(self):
		if (self.onMove == "O"):
			self.onMove = "X"
		if (self.onMove == "X"):
			self.onMove = "O"

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
				self.movesMade += 1
				self.toggleMove()
				return True
		return False

	# todo: cache functie mogelijkheid bedenken
	def checkVictory(self, symbol, printing = False):
		""" checks wether victory is been made by symbol of choice """

		condition =(("'"+symbol+"', ")*4)[:-2]
		
		# check for appearance in order of computational complexity
		if (not self.checkRows(condition)):
			
			if (not self.checkColumns(condition)):
				
				if (not self.checkDiag(condition)):

					# if its not in rows, columns or diagonals return false
					return False


				
		if (printing):
			print "WINNER : ", symbol
		return True

	def anyVictory(self):
		a = self.checkVictory("X")
		b = self.checkVictory("O")
		if (a):
			return "X"
		elif(b):
			return "O"
		else:
			return False

	def countRows(self, condition):
		""" counts all occurences in rows for a certain pattern/condition """

		counter = 0
		for row in self.board:
			counter += str(row).count(condition)
				
		return counter

	def countColumns(self, condition):
		""" counts all occurences in columns for a certain pattern/condition """

		counter = 0

		# the zip is a transpose
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

		# the zip is a transpose
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

	# todo: cache functie mogelijkheid bedenken
	def checkBoard(self, condition):
		""" combine 3 check functions """

		return (self.checkRows(condition) or self.checkColumns(condition) or self.checkDiag(condition))

	def evaluateBoard(self, symbol):
		""" evaluates board on winning, near winning etc.. positions """

		winInOne, winInTwo, winInThree = self.countWinIn(3, symbol)
		certainWin = (winInOne>1)
		return winInOne, winInTwo, winInThree, certainWin

	def countWinIn(self, number, symbol):
		""" Counts winin1 winin2 winin3 """

		one = 0
		two = 0
		three = 0
		symbolelement = ("'"+symbol+"', ")
		emptyslot = "' ', "

		# win in 1
		for move in self.possibleMoves():
			newBoard = deepcopy(self)
			newBoard.doMove(move, symbol)
			if (newBoard.checkVictory(symbol)):
				one += 1

			# win in 2
			if (number < 2):
				continue
			else:
				for move2 in newBoard.possibleMoves():
					newNewBoard = deepcopy(newBoard)
					newNewBoard.doMove(move2, symbol)
					if (newNewBoard.checkVictory(symbol)):
						two += 1

					# win in 3
					if (number < 3):
						continue
						# pattern1 = emptyslot*2+symbolelement
					else:
						for move3 in newNewBoard.possibleMoves():
							newNewNewBoard = deepcopy(newNewBoard)
							newNewNewBoard.doMove(move3, symbol)
							if (newNewNewBoard.checkVictory(symbol)):
								three += 1

		return one, two, three

	def countBlocks(self, symbol, opponentSymbol):
		symbolelement = "'"+symbol+"', "
		opponentEelement = "'"+opponentSymbol+"', "

		pattern1 = (opponentEelement*3+symbolelement)[:-2]
		pattern2 = (opponentEelement*2+symbolelement+opponentEelement)[:-2]
		pattern3 = (opponentEelement+symbolelement+opponentEelement*2)[:-2]
		pattern4 = (symbolelement+opponentEelement*3)[:-2]

		patternList = [pattern1, pattern2, pattern3, pattern4]

		blocks =0

		for pat in patternList:
			blocks += self.countBoard(pat)
		return blocks


	def countPotentials(self, symbol):
		symbolelement = "'"+symbol+"', "
		emptyslot = "' ', "

		pattern1 = (emptyslot*3+symbolelement)[:-2]
		pattern2 = (emptyslot*2+symbolelement+emptyslot)[:-2]
		pattern3 = (emptyslot+symbolelement+emptyslot*2)[:-2]
		pattern4 = (symbolelement+emptyslot*3)[:-2]

		patternList = [pattern1, pattern2, pattern3, pattern4]

		potentials = 0

		for pat in patternList:
			potentials += self.countBoard(pat)
		return potentials

		