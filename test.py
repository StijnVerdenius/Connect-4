




def parseFIS(file):
	currentObject = None
	for i, line in enumerate(file):
		print type(line) , i
		if (line.startswith("[")):
			self.objectStorage(currentObject)
			currentObject = self.objectCreation(line)
		else:
			self.objectEnrichment(currentObject, line)

	self.inputs = self.reasoner.inputs
	self.outputs = self.reasoner.outputs

def objectStorage(self, inputOb):
	if (inputOb.type == "input"):
		self.reasoner.inputs.append(inputOb)
	elif (inputOb.type == "output"):
		self.reasoner.outputs.append(inputOb)
	elif (inputOb.type == "rulebase"):
		self.reasoner.rulebase = inputOb
	elif(inputOb.type == "reasoner"):
		self.reasoner = inputOb
	else:
		print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

def objectCreation(self, line):
	if (line.contains("System")):
		return self.Reasoner(None, None, None, None, None, None, None, None, None)
	elif (line.contains("Input")):
		return self.Input(None, None, None)
	elif (line.contains("Output")):
		return self.Output(None, None, None)
	elif (line.contains("Rules")):
		self.inputs = self.reasoner.inputs
		self.outputs = self.reasoner.outputs
		return self.Rulebase(None, None, None)
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
		self.rulebaseEnrichment(inputOb, line)
	elif(inputOb.type == "reasoner"):
		self.systemEnrichment(inputOb, line)
	else:
		print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

def inputEnrichment(self, inputOb, line):
	if (line.contains("Name")):
		inputOb.name = line[:-1].split("'")[-1]
	elif (line.contains("Range")):
		inputOb.range = tuple(line.split("=")[-1])
	elif (line.contains("NumMFs")):
		inputOb.mfs = int(line.split("=")[-1])*[None]
	elif (line.contains("MF")):
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
		return self.TriangularMF(name, arguments[0], arguments[1], arguments[2])
	elif(sort == "trimf"):
		return self.TrapezoidalMF(name, arguments[0], arguments[1], arguments[2], arguments[3])
	elif(sort == "gaussmf"):
		return self.GaussianMF(name, arguments[1], arguments[0])
	else:
		print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

def outputEnrichment(self, outputOb, line):
	if (line.contains("Name")):
		inputOb.name = line[:-1].split("'")[-1]
	elif (line.contains("Range")):
		inputOb.range = tuple(line.split("=")[-1])
	elif (line.contains("NumMFs")):
		inputOb.mfs = int(line.split("=")[-1])*[None]
	elif (line.contains("MF")):
		arguments = list(line.split(",")[-1].replace(" ", ","))
		name = line.split("=")[1].split(":")[0].replace("'", "")
		sort = line.split(":")[1].split(",")[0].replace("'", "")
		number = int(line.split("=")[0].split("F")[1])
		membershipOb = self.createMembershipOb(line, arguments, name, sort)
		inputOb.mfs[number-1] = membershipOb
	else:
		print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name

def systemEnrichment(self, systemOb, line):
	if (line.contains("Name")):
		systemOb.name = line[:-1].split("'")[-1]
	elif (line.contains("AndMethod")):
		systemOb.andMeth = line[:-1].split("'")[-1]
	elif (line.contains("OrMethod")):
		systemOb.orMeth = line[:-1].split("'")[-1]
	elif (line.contains("ImpMethod")):
		systemOb.impMethod = line[:-1].split("'")[-1]
	elif (line.contains("AggMethod")):
		systemOb.aggMethod = line[:-1].split("'")[-1]
	elif (line.contains("DefuzzMethod")):
		systemOb.defuzzification = line[:-1].split("'")[-1]
	elif (line.contains("NumInputs")):
		systemOb.inputs = int(line.split("=")[-1])*[None]
	elif (line.contains("NumOutputs")):
		systemOb.outputs = int(line.split("=")[-1])*[None]
	else:
		print "error: fuzzytoolbox:" + sys._getframe().f_code.co_name



def rulebaseEnrichment(self, rulebaseOb, line):

	ant = self.computeAntecedent(list("[" + line.split(",")[0].replace(" ", ",") + "]"))
	
	op = int(line.split(":")[1][1])
	if (op == 2):
		op = "or"
	else:
		op = "and"
	
	cons = self.computeConsequent(list("[" + line.split(", ")[1].split(" (")[0].replace(" ", ",") + "]"))

	newRule = self.Rule(ant, op, cons)
	rulebaseOb.rules.append(newRule)

def computeAntecedent(self, arguments):
	returnList = []
	for i, number in enumerate(arguments):
		if (number == 0):
			continue
		else:
			returnList.append(self.inputs[i].mfs[number].name)

	return returnList

def computeConsequent(self, arguments):
	returnList = []
	for i, number in enumerate(arguments):
		if (number == 0):
			continue
		else:
			returnList.append(self.inputs[i].mfs[number].name)

	return returnList[0]


filename = "try fuzzysystem1.fis"
f = open(filename, "r")
parseFIS(f)
f.close()