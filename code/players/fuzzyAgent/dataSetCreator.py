
import numpy as np
from copy import deepcopy
from random import choice
import bruteForceJudge
from scipy.optimize import curve_fit

import pickle

import sys
sys.path.append("../..")

import boardDef

class dataSet(object):
	
	def __init__(self, judge, size, new=False):

		self.size = size
		self.judge = self.importJudge(judge)
		if (new):
			self.createDataset(self.judge, size)
		self.dataSet = self.loadObject("dataset")
		self.shape = self.dataSet.shape

	def tolist(self):
		return self.dataSet.tolist()

	def __iter__(self):
		self.current = 0 
		return self

	def next(self): 
		if self.current >= len(self.dataSet):
			raise StopIteration
		else:
			self.current += 1
			return self.dataSet[self.current-1]

	def importJudge(self, judgeName):
		judge= None
		if (judgeName == "brute"):
			judge=bruteForceJudge.bruteForceJudge()

		return judge

	def saveObject(self, name, objectI):
		with open(name+'.pkl', 'wb') as output:
			pickle.dump(objectI, output, pickle.HIGHEST_PROTOCOL)
		return True

	def loadObject(self, name):
		with open(name+'.pkl', 'rb') as input:
			return pickle.load(input)

	def initialize_centers(self, xpts, ypts, n_centers):
		"""Initialize fuzzy c-means clusters."""
	
		init = []
		
		# take some random datapoints as starting configuration
		for i in range(n_centers):
			init.append([ choice(xpts), choice(ypts)])
		return init

	def distance(self, one, two):
		""" does the euclidian distance between two vectors"""
	
		return np.linalg.norm(np.array(one) - np.array(two))

	def c_means(self, xpts, ypts, n_centers, max_iter = 30, m = 1.5, threshold = 1):
		"""Fuzzy C-Means clustering algorithm."""

		centroids = self.initialize_centers(xpts, ypts, n_centers)
		
		# initiates centroids and dataset
		dataSet = []
		centroids = np.matrix(centroids)
		for i in range(len(xpts)):
			dataSet.append((xpts[i], ypts[i])) 
		dataSet = np.matrix(dataSet)
		
		# initiate u
		u = np.zeros((len(dataSet),len(centroids)))

		while(max_iter > 1):
	#		 print ("iteration : " + str(max_iter))

			oldCents = deepcopy(centroids)

			# calculate the m factor
			mFactor = (2/(m-1))
			
			# recaculate membership degrees
			for j in range(0, len(centroids)):
				for i in range(0, len(dataSet)):
					temp = 0.0
					for k in range(0,len(centroids)):
						temp += ((self.distance(dataSet[i], centroids[j]))/ (self.distance(dataSet[i], centroids[k]))) ** mFactor 
					u[i][j] = 1 / temp 
			
			# do matrix multiplication from u and dataset
			a = (u.T.dot(dataSet))
			
			# devide by sum of u rows
			for i, urow in enumerate(u.T):
				factor = sum(urow)
				for j, coord in enumerate(centroids[i]):
					
					# calculate new centroids
					centroids[i][j] = a[i][j] / factor
				
			
			max_iter -= 1

			distances = self.distance(oldCents, centroids)
			if (distances < threshold):
				break
		return np.array(centroids), np.array(u).T

	def findMembershipFunctions(self, function, xpts, ypts, n_centers):
		_, u = self.c_means(xpts, ypts, n_centers)
		args, _ = curve_fit(function, ypts, u)
		return args

	def createDataset(self, judge, size):
		data = []

		for x in range(size):
			board = boardDef.board()
			self.playGame(board, judge, data)

		self.saveObject("dataset", np.array(data))


	def playGame(self, board, judge, dataSet):
		""" plays a game with random moves and saves a dataentries in every move """

		crossTurn = False

		dataEntry = 0

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
				dataEntry, score = judge.createDataEntry(board, dataEntry, "O", "X")
				dataEntry.append(score)
				dataSet.append(dataEntry)
				
				# next player on move
				crossTurn = not crossTurn
			else:
				print "couldnt find possibilities" 	
				return scoreList











