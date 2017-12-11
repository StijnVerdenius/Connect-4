


class bruteForceJudge:
	def __init__(self):
		pass

	def createDataEntry(self, board, dataEntry, symbol, opponent):



		a = board.countBlocks(symbol, opponent)
		b = board.countPotentials(symbol)
		c,d = board.countWinIn(2, symbol)[:-1]


		e,f,g,h = 0,0,0,0

		if(dataEntry==0):
			e,f,g,h = a,b,c,d
		else:
			e,f,g,h = (a-dataEntry[0]), (b-dataEntry[1]), (c-dataEntry[2]), (d-dataEntry[3])



		newEntry = [a,b,c,d,e,f,g,h]

		if (board.checkVictory(symbol)):
			score = 10000
		elif(board.checkVictory(opponent)):
			score= -10000
		else:
			score = self.determineScore(newEntry)

		

		return newEntry, score


	def determineScore(self, entry, scoreFunctie = [3,2,64,8,1,0.5,8,2]):


		score = 0
		for i, sc in enumerate(scoreFunctie):
			score += entry[i]*sc
		return score



