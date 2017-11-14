
import numpy as np
import monteCarlos
import fuzzyPlayer
import nnPlayer
import boardDef




def interface():

	# initialization
	monte = monteCarlos.algorithm()
	nn = nnPlayer.algorithm(buildDataset = False)
	started = False
	chosenOpponent1 = False
	chosenOpponent2 = False
	playerX = None
	playerO = None
	krossOnMove = False
	board = boardDef.board()

	# choosing oponents
	while(not started):
		choice1 = ""
		choice2 = ""
		if (not chosenOpponent1):
			choice1 = raw_input('select player O: [Human, monteCarlos, NN] ')
		if (not chosenOpponent2):
			choice2 = raw_input('select player X: [Human, monteCarlos, NN] ')
		
		if (choice1 in ["Human", "monteCarlos", "NN"]): 
			if(choice1 == "monteCarlos"):
				playerO = monte
				argumentsO = [0.8]
			
			elif(choice1 == "NN"):
				playerO = nn
				argumentsO = [None]
			else:
				playerO = choice1
			chosenOpponent1 = True
		if (choice2 in ["Human", "monteCarlos", "NN"]):
			
			if(choice2 == "monteCarlos"):
				playerX = monte
				argumentsX = [0.8]
			elif(choice2 == "NN"):
				playerX = nn
				argumentsX = [None]
			else:
				playerX = choice2
			chosenOpponent2 = True

		if (chosenOpponent1 and chosenOpponent2):
			started = True


	# play game
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
				pcMove(board, playerX, argumentsX, "X")
		else:
			if (playerO == "Human"):
				playerMove(board, krossOnMove)
			else:
				pcMove(board, playerO, argumentsO, "O")

			
		krossOnMove = not krossOnMove
	
	# show winner
	aftermath(board)


def playerMove(board, krossOnMove):
	""" doing a move for a player """

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


def pcMove(board, opponent, arguments, symbol):
	""" doing a move for a ai player """
	
	moveResult = False
	while (not moveResult):
		move = opponent.decideMove(board, symbol, arguments)

		print "Chosen Move: ", move[0]
		moveResult = board.doMove(move[0], symbol)

def aftermath(board):
	""" final game aftermath """

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