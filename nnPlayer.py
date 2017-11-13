from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np 
from random import choice
import pickle
from copy import deepcopy
import boardDef

class algorithm:
	def __init__(self, buildDataset = False, datasetSize = 5000):

		# initialization
		if(buildDataset):
			self.createDataset(datasetSize)
		self.classifier = self.loadObject("nn")
		self.scaler = self.loadObject("nnScaler")

	def decideMove(self, board, symbol, _):
		""" decides best move """

		# lazy depthfirst of 2 steps deep

		# initialization
		bestmove = (-100000,-100000)
		for move in board.possibleMoves():

			# copy board and do move
			newBoard = deepcopy(board)
			newBoard.doMove(move, symbol)
			
			# second recursion step
			score = 0
			possible = newBoard.possibleMoves()
			for countermove in possible:
				newSymbol = "O"
				if (symbol == "O"):
					newSymbol = "X"

				# copy board and do move
				newNewBoard = deepcopy(newBoard)
				newNewBoard.doMove(countermove, newSymbol)

				# make a dataentry for nearal network check
				boardentry, _ = self.createDataEntry(newNewBoard)
				
				# add score for first layer deep
				if (symbol == "O"):
					score -= float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0])
				else:
					score += float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0])
			
			# take average of score
			movescore = (score+0.0) / (len(possible)+0.1)

			print "move : " , move, "score : ", str(movescore/2.0)[:5]

			# save if better than before
			if (movescore > bestmove[1]):
				bestmove = (move, movescore)
		return bestmove

	def decideMovesInOrder(self, board, symbol, _):
		""" decides moves in order of score """

		moves = []
		for move in board.possibleMoves():
			newBoard = deepcopy(board)
			newBoard.doMove(move, symbol)
			score = 0
			possible = newBoard.possibleMoves()
			for countermove in possible:
				newSymbol = "O"
				if (symbol == "O"):
					newSymbol = "X"


				newNewBoard = self.doMove(deepcopy(newBoard), countermove, newSymbol)[0]
				newNewBoard = deepcopy(newBoard)
				newNewBoard.doMove(countermove, newSymbol)
				boardentry, _ = self.createDataEntry(newNewBoard)

				if (symbol == "O"):
					score -= float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0])
				else:
					score += float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0]) #.reshape(-1,1)
			movescore = (score+0.0) / (len(possible)+0.1)
			moves.append(movescore)
		return moves



	def createDataset(self, games):
		""" create a dataset for neural network """

		dataset = []
		scores = []
		scalerLocale = StandardScaler()
		for x in range(games):
			print "game : ", x
			board = boardDef.board()
			scores = scores + self.playGame(board, dataset)


		scalerLocale.fit(dataset)
		X = scalerLocale.transform(dataset)
		y = scores

		neural = MLPClassifier(hidden_layer_sizes = (10,10))
		neural.fit(X, y)
		self.saveObject("nn", neural)
		self.saveObject("nnScaler", scalerLocale)
		print "saved"



	def playGame(self, board, dataset):
		""" plays a game with random moves and saves a dataentries in every move """

		crossTurn = False
		scoreList = []

		# continue untill end
		while (not board.checkVictory( "O") and not board.checkVictory( "X")):

			# choose random move
			possible = board.possibleMoves()
			if (len(possible)>0):
				move = choice(possible)

				# make the move
				if (crossTurn):
					board.doMove( move, "X")
				else:
					board.doMove( move, "O")

				# get and save dataentry
				dataEntry, score = self.createDataEntry(board)
				dataset.append(dataEntry)
				scoreList.append(score)
				
				# next player on move
				crossTurn = not crossTurn
			else:
				print "couldnt find possibilities" 	
				return scoreList

		return scoreList

	
	def createDataEntry(self, board):
		""" creates a data entry for board to fit or train """

		dataEntry = []

		turnCounter = 0

		scoreCounter = 0

		# save board
		for y in board.board:
			for x in y:
				if (x=="X"):
					dataEntry.append(1)
					turnCounter += 1
				elif(x=="O"):
					dataEntry.append(-1)
					turnCounter += 1
				else:
					dataEntry.append(0)

		# count for both players
		for symbol in ["X", "O"]:

			# initialize patterns
			symbolelement = ("'"+symbol+"', ")
			emptyslot = "' ', "
			condition1 = (emptyslot+symbolelement*2+emptyslot)[:-2]
			condition2 = (symbolelement*2+emptyslot+symbolelement)[:-2]
			condition3 = (symbolelement+emptyslot+symbolelement*2)[:-2]
			condition4 = (emptyslot+symbolelement*3)[:-2]
			condition5 = (symbolelement*3+emptyslot)[:-2]
			condition6 = (symbolelement*4)[:-2]
			conditionlist = [condition1,condition2,condition3,condition4,condition5,condition6]
			scorelist = [5,20,20,20,20,200]

			# count for patterns and assign score out of scorelist
			for i in range(len(scorelist)):
				score = board.countBoard(conditionlist[i])*scorelist[i]
				dataEntry.append(score)
				if (symbol == "O"):
					score = -1*score
				scoreCounter += score
				
		dataEntry.append(turnCounter)
		
		return dataEntry, scoreCounter


	def saveObject(self, name, objectI):
		with open(name+'.pkl', 'wb') as output:
			pickle.dump(objectI, output, pickle.HIGHEST_PROTOCOL)
		return True

	def loadObject(self, name):
		with open(name+'.pkl', 'rb') as input:
			return pickle.load(input)
			






