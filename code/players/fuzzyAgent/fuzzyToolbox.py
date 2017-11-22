import math
import numpy as np
from collections import defaultdict, Counter
import sys
import json

import fuzzyRuleMaker as ruleGenerator

import fuzzyBasics as basic


"""
Holds all the objects used in a fuzzy inference + the methods to convert a fisfile into the objects 

"""

class fuzzyTools(object):
	def __init__(self, filename, useFisFile= True):

		# hold basic reasoner information
		self.reasoner = None 
		self.inputs = None
		self.outputs = None



		# create a fuzzy logic system from a fis file
		if (useFisFile):
			f = open(filename, "r")
			self.parseFIS(f)
			f.close()


		data = [

		[1,8,64,11],
		[64,0,0,0]


		] # todo: data creation

		self.ruleGenerator = ruleGenerator.fuzzyRules(data, self.inputs, self.outputs, len(self.reasoner.rulebase.rules), self.reasoner.andMeth, self.reasoner.orMeth, filename)
		self.reasoner.rulebase.rules = self.reasoner.rulebase.rules + self.ruleGenerator.generatedRules

		





	def visualize(self):
		""" call this function to get a json with the entire system represented in in """

		def jdefault(o):
		    return o.__dict__

		print "\n\n"
		print(json.dumps(self, default=jdefault))
		print "\n\n paste this in: http://jsonviewer.stack.hu/"



	### Following are functions concerned with fisfile transform to pythonobjects



	def parseFIS(self, file):
		""" create fuzzy logic system from fis file """

		currentObject = None
		for i, line in enumerate(file):
			if (line.startswith("[")):

				# when new object is found, safe the old one
				if (not i == 0): 
					self.objectStorage(currentObject)

				# and create a new one
				currentObject = self.objectCreation(line)
			else:
				# add elements to already existing object
				self.objectEnrichment(currentObject, line)

		# store last objects
		self.objectStorage(currentObject)
		self.inputs = self.reasoner.inputs
		self.outputs = self.reasoner.outputs

	def objectStorage(self, inputOb):
		""" stores object in class """

		print "storing: ", inputOb.type, ": ", inputOb.name
		if (inputOb.type == "input"):
			self.reasoner.inputs.append(inputOb)
		elif (inputOb.type == "output"):
			self.reasoner.outputs.append(inputOb)
		elif (inputOb.type == "rulebase"):
			self.reasoner.rulebase = inputOb
		elif(inputOb.type == "system"):
			self.reasoner = inputOb
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def objectCreation(self, line):
		""" creates the proper object and returns it """

		if ("System" in line):
			return basic.Reasoner(None, None, None, None, None, None, None, None, None)
		elif ("Input"  in line):
			return basic.Input(None, None, None)
		elif ("Output"  in line):
			return basic.Output(None, None, None)
		elif ("Rules"  in line):
			self.inputs = self.reasoner.inputs
			self.outputs = self.reasoner.outputs
			return basic.Rulebase([])
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def objectEnrichment(self, inputOb, line):
		""" redirects line and object to proper enrichment function """

		if (len(line) < 2):
			return
		elif (inputOb.type == "input"):
			self.input_output_Enrichment(inputOb, line)
		elif (inputOb.type == "output"):
			self.input_output_Enrichment(inputOb, line)
		elif (inputOb.type == "rulebase"):
			i = len(inputOb.rules)
			self.rulebaseEnrichment(inputOb, line, i)
		elif(inputOb.type == "system"):
			self.systemEnrichment(inputOb, line)
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name
			print inputOb.type, line

	def input_output_Enrichment(self, inputOb, line):
		""" enriches the input- or outputobject with its settings from fis file """

		if ("Name"  in line):
			inputOb.name = line[:-1].split("'")[-2]
		elif ("Range"  in line):
			inputOb.range = tuple( int(x) for x in line.replace("[", "").replace("]", "").replace("\n", "").split("=")[-1].split(" "))
		elif ( "NumMFs"  in line):
			inputOb.mfs = int(line.split("=")[-1])*[None]
		elif ("MF"  in line):

			# creates the membership function from that line
			arguments =	[float(x) for x in [y.replace(" ", "") for y in line.replace("[", "").replace("]", "").replace("\n", "").split(",")[-1].split(" ")] ]
			name = line.split("=")[1].split(":")[0].replace("'", "")
			sort = line.split(":")[1].split(",")[0].replace("'", "")
			number = int(line.split("=")[0].split("F")[1])
			membershipOb = self.createMembershipOb(line, arguments, name, sort)
			inputOb.mfs[number-1] = membershipOb

		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def createMembershipOb(self, line, arguments, name, sort):
		""" returns the membership object belonging to the specified type """

		if(sort == "trimf"):
			return basic.TriangularMF(name, arguments[0], arguments[1], arguments[2])
		elif(sort == "trapmf"):
			return basic.TrapezoidalMF(name, arguments[0], arguments[1], arguments[2], arguments[3])
		elif(sort == "gaussmf"):
			return basic.GaussianMF(name, arguments[1], arguments[0])
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name
		

	def systemEnrichment(self, systemOb, line):
		""" enriches the systemobject with its settings from fis file """

		if ("Name"  in line):
			systemOb.name = line[:-1].split("'")[-2]
		elif ("AndMethod"  in line):
			systemOb.andMeth = line[:-1].split("'")[-2]
		elif ("OrMethod"  in line):
			systemOb.orMeth = line[:-1].split("'")[-2]
		elif ("ImpMethod"  in line):
			systemOb.impMethod = line[:-1].split("'")[-2]
		elif ("AggMethod"  in line):
			systemOb.aggMethod = line[:-1].split("'")[-2]
		elif ("DefuzzMethod"  in line):
			systemOb.defuzzification = line[:-1].split("'")[-2]
		elif ("NumInputs"  in line):
			systemOb.inputs = []
		elif ("NumOutputs"  in line):
			systemOb.outputs = []



	def rulebaseEnrichment(self, rulebaseOb, line, i):
		""" enriches the rulebaseobject with its settings from fis file """

		# Antecedent creation
		ant = self.computeAntecedent(list(line.split(",")[0].replace(" ", "")))
		
		# pick operator
		op = int(line.split(":")[1][1])
		if (op == 2):
			op = "or"
		else:
			op = "and"
		
		# Consequent creator
		cons = self.computeConsequent( [int(line.split(", ")[1].split(" (")[0])]  )

		# create and save rule
		newRule = basic.Rule(i, ant, op, cons, self.reasoner.andMeth, self.reasoner.orMeth)
		rulebaseOb.rules.append(newRule)

	def computeAntecedent(self, arguments):
		""" computes the antecendent for a rule from fis file """

		returnList = []
		for i, number in enumerate(arguments):
			number = int(number)
			if (number == 0):
				returnList.append("none")
			else:
				returnList.append(self.inputs[i].mfs[number-1].name)

		return returnList

	def computeConsequent(self, arguments):
		""" computes the concequent for a rule from fis file """

		returnList = []

		for i, number in enumerate(arguments):
			number = int(number)
			if (number == 0):
				continue
			else:
				returnList.append(self.outputs[i].mfs[number-1].name)

		return returnList[0]

def breakpoint():
	2 + "this causes a failure: aka breakpoint"
			
def test():
	filename = "LeafNodeSystem.fis"
	tools = fuzzyTools(filename)
	tools.visualize()

	datapoint = [50,0,0]

	print tools.reasoner.inference(datapoint)


# test()