import math
import numpy as np
from collections import defaultdict, Counter
import sys
import json

class fuzzyTools(object):
	def __init__(self, filename):

		self.reasoner = None 
		self.inputs = None
		self.outputs = None

		# create a fuzzy logic system from a fis file
		f = open(filename, "r")
		self.parseFIS(f)
		f.close()
		


	def saveObject(self, name, objectI):
		with open(name+'.pkl', 'wb') as output:
			pickle.dump(objectI, output, pickle.HIGHEST_PROTOCOL)
		return True

	def loadObject(self, name):
		with open(name+'.pkl', 'rb') as input:
			return pickle.load(input)


	def parseFIS(self, file):
		currentObject = None
		for i, line in enumerate(file):
			if (line.startswith("[")):
				if (not i == 0): 
					self.objectStorage(currentObject)
				currentObject = self.objectCreation(line)
			else:
				self.objectEnrichment(currentObject, line)
		self.objectStorage(currentObject)
		self.inputs = self.reasoner.inputs
		self.outputs = self.reasoner.outputs

	def objectStorage(self, inputOb):
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
		if ("System" in line):
			return Reasoner(None, None, None, None, None, None, None, None, None)
		elif ("Input"  in line):
			return Input(None, None, None)
		elif ("Output"  in line):
			return Output(None, None, None)
		elif ("Rules"  in line):
			self.inputs = self.reasoner.inputs
			self.outputs = self.reasoner.outputs
			return Rulebase([])
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def objectEnrichment(self, inputOb, line):

		if (len(line) < 2):
			return
		elif (inputOb.type == "input"):
			self.inputEnrichment(inputOb, line)
		elif (inputOb.type == "output"):
			self.outputEnrichment(inputOb, line)
		elif (inputOb.type == "rulebase"):
			i = len(inputOb.rules)
			self.rulebaseEnrichment(inputOb, line, i)
		elif(inputOb.type == "system"):
			self.systemEnrichment(inputOb, line)
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name
			print inputOb.type, line

	def inputEnrichment(self, inputOb, line):
		if ("Name"  in line):
			# print line[:-1].split("'")[-1]
			inputOb.name = line[:-1].split("'")[-2]

		elif ("Range"  in line):
			inputOb.range = tuple(line.split("=")[-1])
		elif ( "NumMFs"  in line):
			inputOb.mfs = int(line.split("=")[-1])*[None]
		elif ("MF"  in line):
			arguments = list(line.split(",")[-1].replace(" ", ","))
			name = line.split("=")[1].split(":")[0].replace("'", "")
			sort = line.split(":")[1].split(",")[0].replace("'", "")
			number = int(line.split("=")[0].split("F")[1])
			membershipOb = self.createMembershipOb(line, arguments, name, sort)
			inputOb.mfs[number-1] = membershipOb
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def createMembershipOb(self, line, arguments, name, sort):
		if(sort == "trapmf"):
			return TriangularMF(name, arguments[0], arguments[1], arguments[2])
		elif(sort == "trimf"):
			return TrapezoidalMF(name, arguments[0], arguments[1], arguments[2], arguments[3])
		elif(sort == "gaussmf"):
			return GaussianMF(name, arguments[1], arguments[0])
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def outputEnrichment(self, outputOb, line):
		if ("Name"  in line):
			outputOb.name = line[:-1].split("'")[-2]
		elif ("Range"  in line):
			outputOb.range = tuple(line.split("=")[-1])
		elif ( "NumMFs"  in line):
			outputOb.mfs = int(line.split("=")[-1])*[None]
		elif ("MF"  in line):
			arguments = list(line.split(",")[-1].replace(" ", ","))
			name = line.split("=")[1].split(":")[0].replace("'", "")
			sort = line.split(":")[1].split(",")[0].replace("'", "")
			number = int(line.split("=")[0].split("F")[1])
			membershipOb = self.createMembershipOb(line, arguments, name, sort)
			outputOb.mfs[number-1] = membershipOb
		else:
			print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

	def systemEnrichment(self, systemOb, line):
		if ("Name"  in line):
			systemOb.name = line[:-1].split("'")[-1]
		elif ("AndMethod"  in line):
			systemOb.andMeth = line[:-1].split("'")[-1]
		elif ("OrMethod"  in line):
			systemOb.orMeth = line[:-1].split("'")[-1]
		elif ("ImpMethod"  in line):
			systemOb.impMethod = line[:-1].split("'")[-1]
		elif ("AggMethod"  in line):
			systemOb.aggMethod = line[:-1].split("'")[-1]
		elif ("DefuzzMethod"  in line):
			systemOb.defuzzification = line[:-1].split("'")[-1]
		elif ("NumInputs"  in line):
			systemOb.inputs = []
		elif ("NumOutputs"  in line):
			systemOb.outputs = []



	def rulebaseEnrichment(self, rulebaseOb, line, i):


		ant = self.computeAntecedent(list(line.split(",")[0].replace(" ", "")))
		
		op = int(line.split(":")[1][1])
		if (op == 2):
			op = "or"
		else:
			op = "and"
		
		
		cons = self.computeConsequent( [int(line.split(", ")[1].split(" (")[0])]  )

		newRule = Rule(i, ant, op, cons)
		rulebaseOb.rules.append(newRule)

	def computeAntecedent(self, arguments):
		returnList = []
		for i, number in enumerate(arguments):
			number = int(number)
			if (number == 0):
				returnList.append("none")
			else:
				returnList.append(self.inputs[i].mfs[number-1].name)

		return returnList

	def computeConsequent(self, arguments):
		returnList = []

		for i, number in enumerate(arguments):
			number = int(number)
			if (number == 0):
				continue
			else:
				returnList.append(self.outputs[i].mfs[number-1].name)

		# print returnList
		# breakpoint()
		return returnList[0]
	

def breakpoint():
	2 + "a"


class TriangularMF:
    """Triangular fuzzy logic membership function class."""
    
    def __init__(self, name, start, top, end):
        self.name = name
        self.start = start
        self.top = top
        self.end = end

    def calculate_membership(self, x):
        """Calculate membership of crisp value"""
        
        # if it is in the top, return 1.0, else calculate membership
        if (x == self.top):
            return 1.0
        elif(x < self.top and x > self.start):
            return ((x - self.start)+0.0)/((self.top-self.start)+0.0)
        elif(x > self.top and x < self.end):
            return ((self.end-x)+0.0)/((self.end-self.top)+0.0)
        else:
            
            # when outside bounds, return 0
            return 0.0
        
class TrapezoidalMF:
    """Trapezoidal fuzzy logic membership function class."""
    
    def __init__(self, name, start, left_top, right_top, end):
        self.name = name
        self.start = start
        self.left_top = left_top
        self.right_top = right_top
        self.end = end

    def calculate_membership(self, x):
        """Calculate membership of crisp value"""

        # if it is in the top region, return 1.0, else calculate membership
        if (x >= self.left_top and x <= self.right_top):
            return 1.0
        elif(x < self.left_top and x > self.start):
            return ((x - self.start)+0.0)/((self.left_top-self.start)+0.0)
        elif(x > self.right_top and x < self.end):
            return ((self.end-x)+0.0)/((self.end-self.right_top)+0.0)
        else:
            
            # when outside bounds, return 0
            return 0.0

class GaussianMF:
    """Gaussian fuzzy logic membership function class."""
    
    def __init__(self, name, center, sigma):
        self.name = name
        self.center = center
        self.sigma = sigma

    def calculate_membership(self, x):
        """Calculate membership of crisp value"""

        # if it is the center, return 1.0 else, calculate gaussian
        if (x == self.center):
            return 1.0
        else:
            try:
                return math.exp(-0.5*((x-self.center)/self.sigma))
            except:
                return 0.0

class Variable:
    """General class for variables in an FLS."""
    def __init__(self, name, range, mfs):
        self.name = name
        self.range = range
        self.mfs = mfs

    def calculate_memberships(self, x):
        """Test function to check whether
        you put together the right mfs in your variables."""
        
        return {
            mf.name : mf.calculate_membership(x)
            for mf in self.mfs
        }

    def get_mf_by_name(self, name):
        for mf in self.mfs:
            if mf.name == name:
                return mf

class Input(Variable):
    """Class for input variables, inherits 
    variables and functions from superclass Variable."""
    def __init__(self, name, range, mfs):
        try:
            super().__init__(name, range, mfs)
        except:
            # for python 2.7
            Variable.__init__(self, name, range, mfs)
        self.type = "input"

class Output(Variable):
    """Class for output variables, inherits 
    variables and functions from superclass Variable."""
    def __init__(self, name, range, mfs):
        try:
            super().__init__(name, range, mfs)
        except:
            # for python 2.7
            Variable.__init__(self, name, range, mfs)
        self.type = "output"

class Rule:
    """Fuzzy rule class, initialized with an antecedent (list of strings),
    operator (string) and consequent (string)."""
    def __init__(self, n, antecedent, operator, consequent):
        self.number = n
        self.antecedent = antecedent
        self.operator = operator
        self.consequent = consequent
        self.firing_strength = 0

    def calculate_firing_strength(self, datapoint, inputs):
        """ Calculates firing strength of the rule given a certain input """
        
        # store all the resulting firing strengths from datapoint in a base
        base = []
        for i in range(len(datapoint)):
            
            # calculate the memberships
            memberDictionary = inputs[i].calculate_memberships(datapoint[i])
            
            # add them to the base if theyre in the antecendent
            for key in memberDictionary:
                if key in self.antecedent:
                    base.append(memberDictionary[key])
        
        # if the operation is and, take min, if the operation is or, take the max
        if (self.operator == "and"):
            self.firing_strength = min(base)
        elif (self.operator == "or"):
            self.firing_strength = max(base)
        return self.firing_strength

class Rulebase:
    """The fuzzy rulebase collects all rules for the FLS, can
    calculate the firing strengths of its rules."""
    def __init__(self, rules):
        self.rules = rules
        self.type = "rulebase"
        self.name = "rulebase"

    def calculate_firing_strengths(self, datapoint, inputs):
        result = Counter()
        for i, rule in enumerate(self.rules):
            fs = rule.calculate_firing_strength(datapoint, inputs)
            consequent = rule.consequent
            if fs > result[consequent]:
                result[consequent] = fs
        return result

class Reasoner:
    def __init__(self, rulebase, inputs, output, n_points, andMeth, orMeth, impMethod, aggMethod, defuzzification):
        self.rulebase = rulebase
        self.inputs = inputs
        self.output = output
        self.discretize = n_points
        self.andMeth = andMeth
        self.orMeth = orMeth
        self.impMethod = impMethod
        self.aggMethod = aggMethod
        self.defuzzification = defuzzification
        self.type = "system"
        self.name = "fuzzylogicsystem"

    def inference(self, datapoint):
        """ Does the inference three step process """
        
        ## 1. Calculate the highest firing strength found in the rules per 
        # membership function of the output variable
        firing_strengths = {}
        
        # get rules that actually fired
        fired = self.rulebase.calculate_firing_strengths(datapoint, inputs)
        
        # add variables to firing_strengths
        for linguisticVar in self.output.mfs:
            if linguisticVar.name in fired:
                firing_strengths[linguisticVar.name] = fired[linguisticVar.name]
            else:
                # if they did not fire, add zero nontheless
                firing_strengths[linguisticVar.name] = 0.0
        
        ## 2. Aggragate and discretize
        input_value_pairs = self.aggregate(firing_strengths)

        # 3. Defuzzify
        crisp_output = self.defuzzify(input_value_pairs)
        
        return crisp_output
    
    def frange(self, strt, stp, stepSize):
        """ range function for float values """
        
        while strt < stp:
            yield strt
            strt += stepSize

    def aggregate(self, firing_strengths ):
        """ aggregates functions given output and firing strength """
        
        # define output
        input_value_pairs = []
        
        # determine amount of bins
        bins=self.discretize-1.0
        
        # set begin and end of span on impossible values
        try:
            begin = math.inf
            end = -1*math.inf
        except:
            
            # for python 2.7
            begin = float("inf")
            end = -1*float("inf")
        
        # First find where the aggrageted area starts and ends
        for linguisticVar in self.output.mfs:
            if (linguisticVar.start < begin):
                begin = linguisticVar.start
            if (linguisticVar.end > end):
                end = linguisticVar.end
        
        # define span
        span = end-begin
        
        # Second discretize this area and aggragate
        stepSize = (span/bins)
        
        # build combined window
        for i in self.frange(begin, end, stepSize):
            
            # membership function element consists of all the linguistic variables values at that bin
            mfElement = []
            
            # find al elements for in a bin
            for linguisticVar in self.output.mfs:
                memb = linguisticVar.calculate_membership(i)
                
                # don't add them if they exceed the firing strength (Cut function)
                if (memb > firing_strengths[linguisticVar.name]):
                    memb = firing_strengths[linguisticVar.name]
                mfElement.append(memb)
            
            # take the max of the mfelement and put that as a bin element
            binElement=(i, max(mfElement))
            
            # add bin element as input value pair
            input_value_pairs.append(binElement)
        
        return input_value_pairs

    def defuzzify(self, input_value_pairs):
        """ defuzzifies crisp input"""
        
        crisp_value = 0
        if (self.defuzzification == "som"):
            
            # create a list of values only
            listOfValues = [x[1] for x in input_value_pairs]
            
            # find index of the first max value
            index = listOfValues.index(max(listOfValues))
            
            # look for the fitting crisp output
            crisp_value = input_value_pairs[index][0]
            
        elif(self.defuzzification == "lom"):
            
            # simply reverse the list and do  the same as above here
            inverse_input_value_pairs = input_value_pairs[::-1]
            
            # create a (reversed) list of values only
            listOfValues = [x[1] for x in inverse_input_value_pairs]
            
             # find index of the first max value (in reversed list)
            index = listOfValues.index(max(listOfValues))
            
            # look for the fitting crisp output
            crisp_value = inverse_input_value_pairs[index][0]

        elif(self.defuzzification == "centroid"):
			counterWeight = 0.0
			countRerGeneral = 0.0
			i = 0
			for weight in weights:
				counterGeneral += i*step*weight
				counterWeight += weight

			crisp_value = counterGeneral/counterWeight
        return crisp_value
			

filename = "try fuzzysystem1.fis"
tools = fuzzyTools(filename)

def jdefault(o):
    return o.__dict__
print(json.dumps(tools, default=jdefault))
# s = json.dumps(tools.__dict__)