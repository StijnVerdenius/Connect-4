
import numpy as np
import monteCarlos
import fuzzyPlayer
import nnPlayer
import boardDef




def interface():
	monte = monteCarlos.algorithm()
	nn = nnPlayer.algorithm(buildDataset = False)
	begonnen = False
	tegenstanderGekozen1 = False
	tegenstanderGekozen2 = False
	playerX = None
	playerO = None
	krossOnMove = False
	board = boardDef.board()
	while(not begonnen):
		choice1 = ""
		choice2 = ""
		if (not tegenstanderGekozen1):
			choice1 = raw_input('select player O: [Human, monteCarlos, NN] ')
		if (not tegenstanderGekozen2):
			choice2 = raw_input('select player X: [Human, monteCarlos, NN] ')
		
		if (choice1 in ["Human", "monteCarlos", "NN"]): 
			if(choice1 == "monteCarlos"):
				playerO = monte
			
			elif(choice1 == "NN"):
				playerO = nn
			else:
				playerO = choice1
			tegenstanderGekozen1 = True
		if (choice2 in ["Human", "monteCarlos", "NN"]):
			
			if(choice2 == "monteCarlos"):
				playerX = monte
			
			elif(choice2 == "NN"):
				playerX = nn
			else:
				playerX = choice2
			tegenstanderGekozen2 = True

		if (tegenstanderGekozen1 and tegenstanderGekozen2):
			begonnen = True


		
	
	while (not board.checkVictory("O") and not board.checkVictory("X")):
		print "current board :"
		board.toString()
		print "move is on : "
		if (krossOnMove):
			print "X"
		else:
			print "O"

		if (krossOnMove):
			if (playerX == "Human"):
				playerMove(board, krossOnMove)
			else:
				pcMove(board, playerX, 0.8, "X")
		else:
			if (playerO == "Human"):
				playerMove(board, krossOnMove)
			else:
				pcMove(board, playerO, 0.8, "O")

			
		krossOnMove = not krossOnMove
	
	board.toString()
	board.checkVictory("O", printing = True)
	board.checkVictory("X", printing = True)


def playerMove(board, krossOnMove):
	yourmove = -1
	correctMove = False
	while (yourmove < 1 or yourmove > 8 or not correctMove):
		yourmove = int(raw_input('\n\n place your move: '))
		moveResult = False
		if (krossOnMove):
			moveResult = board.doMove(yourmove, "X")
		else:
			moveResult = board.doMove(yourmove, "O")
		if (moveResult):
			correctMove = True


def pcMove(board, opponent, time, symbol):
	
	moveResult = False
	while (not moveResult):
		move = opponent.decideMove(board, symbol, time)

		print "Chosen Move: ", move[0]
		moveResult = board.doMove(move[0], symbol)

def aftermath(board):
	board.toString()
	board.checkVictory("O", printing = True)
	board.checkVictory("X", printing = True)
	return True


	


interface()


###### time measurement

# import cProfile, pstats, StringIO
# pr = cProfile.Profile()
# pr.enable()

	# place function here

# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats() # TODO
# print s.getvalue()