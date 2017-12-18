
import fuzzyBasics as basic
import numpy as np

""" Class to do fuzzy rule learning via the wang and mendel method """

class fuzzyRules:
	
	def __init__(self, dataSet, inputs, outputs, counter, andMeth, orMeth, fileName):
		self.dataSet = dataSet
		self.generatedRules = []
		self.inputs = inputs
		self.outputs = outputs
		self.counter = counter
		self.andMeth = andMeth
		self.orMeth = orMeth
		self.doProcess()
		self.saveRules(fileName)

	def getRules(self):
		return self.generatedRules

	def doProcess(self):
		""" main function """

		self.generate()
		self.cleanUpRules()

	def generate(self):
		""" generates a rule and a degree for every datapoint """

		for datapoint in self.dataSet[:]:
			rule, degree = self.makeRule(datapoint)
			self.generatedRules.append((rule, degree))


	def saveRules(self, fileName):
		""" saves all remaining rules to a fis file """

		f = open(fileName, "a")
		g = open(fileName, "r")
		lineList = g.readlines()
		g.close()
		removelist = []
		for i, rule in enumerate(self.generatedRules):
			line = self.createFisEntry(rule)
			if (not line in lineList):
				f.write(line)
			else:
				removelist.append(i)
		for i in removelist[::-1]:
			self.generatedRules.pop(i)
		f.close()
		


	def createFisEntry(self, rule):
		""" transforms a python object rule to a fis file entry """

		line = ""
		for i, ant in enumerate(rule.antecedent):
			for j, mf in enumerate(self.inputs[i].mfs):
				if (mf.name == ant):
					line = line + str(j+1) + " "
		line = line[:-1] + ", "
		for i, con in enumerate([rule.consequent]):
			for j, mf in enumerate(self.outputs[i].mfs):
				if (mf.name == con):
					line = line + str(j+1)

		line = line + " (1) : 1\n"
		return line


	def makeRule(self, datapoint):
		""" creates a rule from a datapoint """
		
		ant = []
		cons = []
		membershipsFactors = []

		op = "and"

		# define antecedent
		for i, inp in enumerate(self.inputs):
			memb = inp.calculate_memberships(datapoint[:-len(self.outputs)][i])
			maxInMemb = (-1, "")
			for key in memb:
				if (memb[key] > maxInMemb[0]):
					maxInMemb = (memb[key], key)
			ant.append(maxInMemb[1])
			membershipsFactors.append(maxInMemb[0])

		# define consequent
		for i, outp in enumerate(self.outputs):
			memb = outp.calculate_memberships(datapoint[-len(self.outputs):][i])
			maxInMemb = (-1, "")
			for key in memb:
				if (memb[key] > maxInMemb[0]):
					maxInMemb = (memb[key], key)
			cons.append(maxInMemb[1])
			membershipsFactors.append(maxInMemb[0])

		# increase counter to keep track of amount of rules
		self.counter += 1

		# if (np.product(membershipsFactors) > 1.0):
		# 	print membershipsFactors, np.product(membershipsFactors) (debug)

		# return the new rule and it's degree
		return basic.Rule(self.counter, ant, op, cons[0], self.andMeth, self.orMeth), np.product(membershipsFactors)

	def cleanUpRules(self):
		""" after creating a rule for every datapoint, 
		this function compares the degrees of rules with the same antecedent and keeps the strongest only """

		# initialize
		scoreDict = {}
		newRules = {}

		# loop through rules
		for i, tup in enumerate(self.generatedRules):


			antecedent = str(tup[0].antecedent)

			# if there is no rule in the scoredictionary yet with the same antecedent, put it in both dictionaries
			if (not antecedent in scoreDict):
				newRules[antecedent] = tup[0]
				scoreDict[antecedent] = tup[1]
			else:

				# if there is, then first compare if the degree is higher before overwriting
				if (tup[1] > scoreDict[antecedent]):
					newRules[antecedent] = tup[0]
					scoreDict[antecedent] = tup[1]
				else:
					# not higher? don't overwrite
					continue

		# save rules
		self.generatedRules = []
		for key in newRules:
			self.generatedRules.append(newRules[key])

		return

			

def breakpoint():
	2 + "this causes a failure: aka breakpoint"