


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

		i = board.movesMade

		newEntry = [a,b,c,d,e,f,g,h,i]

		
		score = self.determineScore(newEntry)

		if (board.checkVictory(symbol)):
			score += 200
		elif(board.checkVictory(opponent)):
			score += -200
		# else:

		

		return newEntry, score


	def determineScore(self, entry, scoreFunctie = [3,2,64,8,1,0.5,8,2,-10]):


		score = 0
		for i, sc in enumerate(scoreFunctie):
			score += entry[i]*sc
		return score



