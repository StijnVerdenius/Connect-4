
import numpy as np
from copy import deepcopy
from random import choice
import bruteForceJudge
from scipy.optimize import curve_fit
import skfuzzy as fuzz
from sklearn import preprocessing

import pickle

# import sys
# sys.path.append("../..") for debugging

import boardDef


""" Class to create dataset and do calculations with it """

class dataSet(object):
	
	def __init__(self, judge, size, new=False):
		print "setting up database.."

		self.titles = ["potentials","winin1","winin2","deltapotentials","deltawinin1","deltawinin2","doubledeltapotentials","doubledeltawinin1","doubledeltawinin2","progression", "score"]
		self.centerlist = [3,4,6,3,4,6,3,4,6,4,8]

		self.size = size
		self.judge = self.importJudge(judge)
		if (new):
			self.createDataset(self.judge, size)
		self.dataSet = self.loadObject("players/fuzzyAgent/dataset")
		# self.dataSet = self.loadObject("dataset") # for dubugging
		self.shape = self.dataSet.shape
		self.normalizeY()

	### basic list functions\

	def get(self):
		return self.dataSet

	def tolist(self):
		return self.dataSet.tolist()

	def __iter__(self):
		self.current = 0 
		return self

	def __len__(self):
		return len(self.dataSet)

	def next(self): 
		if self.current >= len(self.dataSet):
			raise StopIteration
		else:
			self.current += 1
			return self.dataSet[self.current-1]

	### dataset specific functions

	def importJudge(self, judgeName):
		""" imports a scoring algorithm for the dataset. this makes it easy to change scoring algorithm """

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

		a =  np.linalg.norm(np.array(one) - np.array(two))

		# if (a == 0):
		# 	if (not (one == two).all()):
		# 		print np.array(one), np.array(two)
		# 		print np.array(one) - np.array(two)
		# 		print one-two
		# 	else:
		# 		print "false alarm"
		# 	return 1.0
	
		return a

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
			print ("iteration : " + str(max_iter))

			oldCents = deepcopy(centroids)

			# calculate the m factor
			mFactor = (2/(m-1))



			
			# recaculate membership degrees
			for j in range(0, len(centroids)):
				for i in range(0, len(dataSet)):
					temp = 0.0
					for k in range(0,len(centroids)):
						temp2 = self.distance(dataSet[i], centroids[k])
						temp3 = self.distance(dataSet[i], centroids[j])
						if (temp2 == 0):
							temp2 = 1.0
							# print "temp2 fout", dataSet[i], dataSet[k]
						if (temp3 == 0):
							temp3 = 1.0
							# print "temp3 fout", dataSet[i], dataSet[j]
						temp += ((temp3)/ (temp2)) ** mFactor
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
		""" finds all guassian parameters for all memberships functions for a single variable"""

		# _, u = self.c_means(xpts, ypts, n_centers) # my own c_means, but it is too slow to work with
		centr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
	    np.vstack((xpts,ypts)), n_centers, 2.0 , 0.05, 50, init=None)
		args = [curve_fit(function, xpts, ui, p0=[centr[i][0]]+[1.0])[0] for i, ui in enumerate(u) ]
		return args

	def createDataset(self, judge, size):
		""" creates a new dataset """

		data = []

		for i, x in enumerate(range(size)):
			print i, "/", size
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

	



	def plot_clusters(self, x, y, cntr, u):
		"""Plot clusters by assigning datapoints to the cluster
		for which the datapoint has the highest membership degree."""

		colors = ['b', 'r', 'g', 'c', "m", "y", "k", "w"]

		# Plot assigned clusters, for each data point in training set
		cluster_membership = np.argmax(u, axis=0)
		for j in range(len(cntr)):
			plt.scatter(x[cluster_membership == j],
				y[cluster_membership == j], color=colors[j], s=5)

			# Mark the center of each fuzzy cluster
			for pt in cntr:
				plt.plot(pt[0], pt[1], 'rs')


	def return_gaussians(self):
		""" calculate all the guassian parameters, for all memberships, for all variables """

		returndict = {}
		
		for i, collumn in enumerate(self.get().T[:-1]):
			print "fitting data ", i, "/", len(self.get().T[:-1])
			x = collumn
			y = self.get().T[-1]
			y = self.projectingVector(x,y)
			func= fuzz.gaussmf
			fitted = self.findMembershipFunctions(func,x,y,self.centerlist[i])
			returndict[self.titles[i]] = fitted

		return returndict

	def projectingVector(self, x, y):
		""" project a yvector onto an x vector by taking the average in the y direction """

		xdict = {}


		for ii, xi in enumerate(x):
			if not xi in xdict:
				xdict[xi] = []
			xdict[xi].append(y[ii])

		yReal = []
		for xi in x:
			yReal.append(sum(xdict[xi])/len(xdict[xi]))

			
		return np.array(yReal)

	def normalizeY(self):
		""" Normalize the y vector in the dataset to -1 to 11 """

		yvector = self.get().T[-1]

		min_max_scaler = preprocessing.MinMaxScaler()
		yvector = min_max_scaler.fit_transform(yvector)

		for i, _ in enumerate(yvector):
			yvector[i] = yvector[i]*12-1
		

		

		self.get().T[-1] = yvector

	def findMinMaxOfFeatures(self):
		""" returns the range of all variables """

		dicti = {}
		for i, column in enumerate(self.get().T):
			title = self.titles[i]
			maxi = int(max(column))
			mini = int(min(column))
			dicti[title] = tuple([mini,maxi])
		return dicti














######################## following is debug meterial:


# a = dataSet("brute", 500, new=False)
# # print len(a)

# # for x in a.findMinMaxOfFeatures():
# # 	print x,  a.findMinMaxOfFeatures()[x]
# # # print a.return_gaussians()

# # # for a in a.get().T:
# # # 	print min(a), max(a)


# # # print len(a)

# import matplotlib.pyplot as plt
# import skfuzzy as fuzz

# titles = ["potentials","winin1","winin2","deltapotentials","deltawinin1","deltawinin2","doubledeltapotentials","doubledeltawinin1","doubledeltawinin2","progression", "score"]
# centerlist = [3,4,6,3,4,6,3,4,6,4,8]


# for i, collumn in enumerate(a.get().T):
# # 	# plt.subplot(4,4, i+1)
# 	if True:#i in  [2]:

# 		for b in [2.5*4]:
# 			plt.title(titles[i] +"\t"+ str(b*0.25+0.1))
# 			x = collumn
# 			y = a.get().T[-1]

# 			print titles[i]


# 			# print len(a.get().T)


# 			# cntr, u = a.c_means(x,y,centerlist[i])

# 			xdict = {}


# 			for ii, xi in enumerate(x):
# 				if not xi in xdict:
# 					xdict[xi] = []
# 				xdict[xi].append(y[ii])

# 			yReal = []
# 			for xi in x:
# 				yReal.append(sum(xdict[xi])/len(xdict[xi]))

				
# 			yReal = np.array(yReal)



# 			cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
# 	  		  np.vstack((x,yReal)), centerlist[i], b*0.25+0.1 , 0.05, 50, init=None)

# 			# # func = fuzz.gaussmf
# 			func= fuzz.gaussmf

# 			fitted= a.findMembershipFunctions(func,x,yReal,centerlist[i])

# 			for fit in fitted:
# 				print fit
# 				out = [func(xp,fit[0], fit[1]) for xp in x]
# 				plt.scatter(x.tolist(), out)

			
# 			# plt.scatter(collumn, a.get().T[-1])
# 			# a.plot_clusters(x,y, cntr, u)
# 			plt.show()

# # # plt.show()






