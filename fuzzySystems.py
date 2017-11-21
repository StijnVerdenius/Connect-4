
from fuzzyToolbox import fuzzyTools


"""
Simply summarizes the two systems we have with default filenames for fis files

"""

class fuzzySystem1(fuzzyTools):
	

	def __init__(self, filename = "LeafNodeSystem.fis"):
		fuzzyTools.__init__(self, filename)
		
	
class fuzzySystem2(fuzzyTools):
	

	def __init__(self, filename = "MiddleNodeSystem.fis"):
		fuzzyTools.__init__(self, filename)



######################
# not used yet
######################

def saveObject(self, name, objectI):
		with open(name+'.pkl', 'wb') as output:
			pickle.dump(objectI, output, pickle.HIGHEST_PROTOCOL)
		return True

def loadObject(self, name):
	with open(name+'.pkl', 'rb') as input:
		return pickle.load(input)