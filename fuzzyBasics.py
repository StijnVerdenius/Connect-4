import math
import numpy as np
from collections import defaultdict, Counter
import sys
import json



"""

Holds all the basic fuzzy logic classes and methods

TODO: 
- make multiple outputs possible
- create implicationmethod 

"""

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
    def __init__(self, n, antecedent, operator, consequent, andMeth, orMeth):
        self.number = n
        self.antecedent = antecedent
        self.operator = operator
        self.consequent = consequent
        self.firing_strength = 0
        self.andMeth = andMeth
        self.orMeth = orMeth

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

            # also check for and method
            if (self.andMeth == "prod"):
                self.firing_strength = np.product(base)
            else:
                self.firing_strength = min(base)
        elif (self.operator == "or"):

            # also check for or method
            if (self.andMeth == "probor"):
                self.firing_strength = 1-np.product([1-x for x in base])
            else:
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
        self.outputs = output
        self.discretize = 201#n_points
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
        fired = self.rulebase.calculate_firing_strengths(datapoint, self.inputs)
        
        # add variables to firing_strengths
        for linguisticVar in self.outputs[0].mfs:
            if linguisticVar.name in fired:
                firing_strengths[linguisticVar.name] = fired[linguisticVar.name]
            else:
                # if they did not fire, add zero nontheless
                firing_strengths[linguisticVar.name] = 0.0
        
        ## 2. Aggragate and discretize
        input_value_pairs, begin, stepSize = self.aggregate(firing_strengths)

        # 3. Defuzzify
        crisp_output = self.defuzzify(input_value_pairs, begin, stepSize)
        
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
        for linguisticVar in self.outputs[0].mfs:
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
            for linguisticVar in self.outputs[0].mfs:
                memb = linguisticVar.calculate_membership(i)
                
                # don't add them if they exceed the firing strength (Cut function)
                if (memb > firing_strengths[linguisticVar.name]):
                    memb = firing_strengths[linguisticVar.name]
                mfElement.append(memb)
            
            # take the max of the mfelement and put that as a bin element
            binElement = []
            if (self.aggMethod == "max"):
            	binElement=(i, max(mfElement))
            elif (self.aggMethod == "sum"):
            	binElement=(i, np.mean(mfElement))
            elif (self.aggMethod == "prod"):
            	binElement = (i, np.product(mfElement))
            else:
            	print "error: fuzzybasics:" + sys._getframe().f_code.co_name


            
            
            # add bin element as input value pair
            input_value_pairs.append(binElement)
        
        return input_value_pairs, begin, stepSize

    def defuzzify(self, input_value_pairs, stepSize, begin):
        """ defuzzifies crisp input"""

        # create a list of values only
        listOfValues = [x[1] for x in input_value_pairs]
        
        crisp_value = 0
        if (self.defuzzification == "som"):
            
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
			counterGeneral = 0.0
			i = begin
			
			for pair in input_value_pairs:

				counterGeneral += pair[0]*pair[1]
				counterWeight += pair[1]

			crisp_value = counterGeneral/counterWeight

        return crisp_value