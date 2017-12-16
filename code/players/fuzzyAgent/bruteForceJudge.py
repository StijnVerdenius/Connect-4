


class bruteForceJudge:
	def __init__(self):
		pass

	def createDataEntry(self, board, dataEntry, symbol, opponent):



		
		a = board.countPotentials(symbol)
		b,c = board.countWinIn(2, symbol)[:-1]

		# delta one
		d,e,f = 0,0,0

		# delta two
		g,h,i = 0,0,0

		if(dataEntry==0):
			d,e,f = a,b,c
			g,h,i = a,b,c
		else:
			d,e,f = (a-dataEntry[0]), (b-dataEntry[1]), (c-dataEntry[2])
			g,h,i = (a-dataEntry[3]), (b-dataEntry[4]), (c-dataEntry[5])

		j = board.movesMade

		newEntry = [a,b,c,d,e,f,g,h,i,j]

		
		score = self.determineScore(newEntry)

		if (board.checkVictory(symbol)):
			score += 200
		elif(board.checkVictory(opponent)):
			score += -200

		

		return newEntry, score


	def determineScore(self, entry, scoreFunctie = [2,64,8,1,16,4,0.25,5,1,-20]):


		score = 0
		for i, sc in enumerate(scoreFunctie):
			score += entry[i]*sc
		return score



