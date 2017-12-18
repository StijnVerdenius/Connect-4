
from fuzzyToolbox import fuzzyTools


"""
Simply summarizes the two systems we have with default filenames for fis files

"""

class fuzzySystem2(fuzzyTools):
	

	def __init__(self, filename = "players/fuzzyAgent/fuzzyAgent2_and_3.fis"):
		fuzzyTools.__init__(self, filename)
	
class fuzzySystem1(fuzzyTools):

	def __init__(self, filename = "players/fuzzyAgent/fuzzyAgent1.fis"):
		fuzzyTools.__init__(self, filename)
	




