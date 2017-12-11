
import fuzzyBasics as basic
import numpy as np

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
		self.generate()
		self.cleanUpRules()

	def generate(self):

		for datapoint in self.dataSet[:]:
			rule, degree = self.makeRule(datapoint)
			self.generatedRules.append((rule, degree))


	def saveRules(self, fileName):
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
		
		ant = []
		cons = []
		membershipsFactors = []

		op = "and"

		# define ant

		for i, inp in enumerate(self.inputs):
			memb = inp.calculate_memberships(datapoint[:-len(self.outputs)][i])
			maxInMemb = (-1, "")
			for key in memb:
				if (memb[key] > maxInMemb[0]):
					maxInMemb = (memb[key], key)
			ant.append(maxInMemb[1])
			membershipsFactors.append(maxInMemb[0])

		# define cons

		for i, outp in enumerate(self.outputs):
			memb = outp.calculate_memberships(datapoint[-len(self.outputs):][i])
			maxInMemb = (-1, "")
			for key in memb:
				if (memb[key] > maxInMemb[0]):
					maxInMemb = (memb[key], key)
			cons.append(maxInMemb[1])
			membershipsFactors.append(maxInMemb[0])

		self.counter += 1
		return basic.Rule(self.counter, ant, op, cons[0], self.andMeth, self.orMeth), np.product(membershipsFactors)

	def cleanUpRules(self):
		pass


	def manualDatasetCreator(self):
		amount = int(raw_input("number of datapoints"))
		dataset = []
		for x in range(amount):
			dataEntry = []
			




	def automaticDatasetCreator(self):
		pass

def breakpoint():
	2 + "this causes a failure: aka breakpoint"