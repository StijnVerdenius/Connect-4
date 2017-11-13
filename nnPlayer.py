from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np 
from random import choice
import pickle
from copy import deepcopy
import boardDef

class algorithm:
	def __init__(self, buildDataset = False, datasetSize = 5000):
		if(buildDataset):
			self.createDataset(datasetSize)
		self.classifier = self.loadObject("nn")
		self.scaler = self.loadObject("nnScaler")

	def decideMove(self, board, symbol, _):
		bestmove = (-100000,-100000)
		for move in board.possibleMoves():
			newBoard = deepcopy(board)
			newBoard.doMove(move, symbol)
			
			score = 0
			possible = newBoard.possibleMoves()
			for countermove in possible:
				newSymbol = "O"
				if (symbol == "O"):
					newSymbol = "X"
				newNewBoard = deepcopy(newBoard)
				newNewBoard.doMove(countermove, newSymbol)
				boardentry, _ = self.createDataEntry(newNewBoard)
				
				if (symbol == "O"):
					score -= float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0])
				else:
					score += float(self.classifier.predict(self.scaler.transform(np.array([boardentry])))[0])
				
			movescore = (score+0.0) / (len(possible)+0.1)
			print "move : " , move, "score : ", str(movescore/2.0)[:5]
			if (movescore > bestmove[1]):
				bestmove = (move, movescore)
		return bestmove

	def decideMovesInOrder(self, board, symbol, _):
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

		crossTurn = False
		scoreList = []

		while (not board.checkVictory( "O") and not board.checkVictory( "X")):
			possible = board.possibleMoves()
			if (len(possible)>0):
				move = choice(possible)
				if (crossTurn):
					board.doMove( move, "X")[0]
				else:
					board.doMove( move, "O")[0]

					
				dataEntry, score = self.createDataEntry(board)
				dataset.append(dataEntry)
				scoreList.append(score)
				
				



				crossTurn = not crossTurn
			else:
				print "couldnt find possibilities" 	
				return scoreList

			

		return scoreList

	
	def createDataEntry(self, board):
		dataEntry = []

		turnCounter = 0

		scoreCounter = 0

		
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

		for symbol in ["X", "O"]:
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
			for i in range(6):
				score = board.countBoard(conditionlist[i])*scorelist[i]
				dataEntry.append(score)
				if (symbol == "O"):
					score = -1*score
				scoreCounter += score
				
		dataEntry.append(turnCounter)
		
		return dataEntry, scoreCounter



	



	def saveObject(self, naam, objectI):
		with open(naam+'.pkl', 'wb') as output:
			pickle.dump(objectI, output, pickle.HIGHEST_PROTOCOL)
		return True

	def loadObject(self, naam):
		with open(naam+'.pkl', 'rb') as input:
			return pickle.load(input)
			






