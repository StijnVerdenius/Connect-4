
import numpy as np


import players.MonteCarlos.monteCarlos as monteCarlos
import players.fuzzyAgent.fuzzyPlayer as fuzzyPlayer
import players.Neural.nnPlayer as nnPlayer
import players.BruteForce.dumbplayer as dumbplayer
import boardDef

FUZZ_ARGUMENTS = [-0.1]
M_CARLOS_ARGUMENTS = [0.8]
EMPTY_ARGUMENTS = [None]

def interface():

	# initialization
	monte = monteCarlos.algorithm()
	nn = nnPlayer.algorithm(buildDataset = False)
	fuzz = fuzzyPlayer.algorithm()
	brute = dumbplayer.algorithm()
	started = False
	chosenOpponent1 = False
	chosenOpponent2 = False
	playerX = None
	playerO = None
	krossOnMove = False
	board = boardDef.board()
	argumentsO = None
	argumentsX = None

	# choosing oponents
	while(not started):

		# getting input
		choice1 = ""
		choice2 = ""
		if (not chosenOpponent1):
			choice1 = raw_input('select player O: [Human, MonteCarlos, NN, Fuzzy, Brute] ')
		if (not chosenOpponent2):
			choice2 = raw_input('select player X: [Human, MonteCarlos, NN, Fuzzy, Brute] ')
		

		# evaluate input
		if (choice1 in ["Human", "MonteCarlos", "NN", "Fuzzy", "Brute"]): 
			if(choice1 == "MonteCarlos"):
				playerO = monte
				argumentsO = M_CARLOS_ARGUMENTS
			elif(choice1 == "Brute"):
				playerO = brute
				argumentsO = EMPTY_ARGUMENTS
			elif(choice1 == "NN"):
				playerO = nn
				argumentsO = EMPTY_ARGUMENTS
			elif(choice1 == "Fuzzy"):
				playerO = fuzz
				argumentsO = FUZZ_ARGUMENTS
			else:
				playerO = choice1
				argumentsO = EMPTY_ARGUMENTS
			chosenOpponent1 = True
		if (choice2 in ["Human", "MonteCarlos", "NN", "Fuzzy", "Brute"]):
			
			if(choice2 == "MonteCarlos"):
				playerX = monte
				argumentsX = M_CARLOS_ARGUMENTS
			elif(choice2 == "Brute"):
				playerX = brute
				argumentsX = EMPTY_ARGUMENTS
			elif(choice2 == "NN"):
				playerX = nn
				argumentsX = EMPTY_ARGUMENTS
			elif(choice2 == "Fuzzy"):
				playerX = fuzz
				argumentsX = FUZZ_ARGUMENTS
			else:
				playerX = choice2
				argumentsX = EMPTY_ARGUMENTS
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
				playerMove(board, krossOnMove, argumentsX)
			else:
				pcMove(board, playerX, argumentsX, "X")
		else:
			if (playerO == "Human"):
				playerMove(board, krossOnMove, argumentsO)
			else:
				pcMove(board, playerO, argumentsO, "O")

		
		krossOnMove = not krossOnMove
		# # print "O", board.evaluateBoard("O")
		# import cProfile, pstats, StringIO
		# pr = cProfile.Profile()
		# pr.enable()

		# for x in range(a):
		# print "O",  board.evaluateBoard("O")
		# print "X",  board.evaluateBoard("X")

		# pr.disable()
		# print a
		# s = StringIO.StringIO()
		# sortby = 'cumulative'
		# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		# ps.print_stats() 
		# print s.getvalue()
		# return
		
	
	# show winner
	afterMath(board)


def playerMove(board, krossOnMove, arguments):
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

def afterMath(board):
	""" final game afterMath """

	board.toString()
	board.checkVictory("O", printing = True)
	board.checkVictory("X", printing = True)
	return True

def breakpoint():
	2 + "this causes a failure: aka breakpoint"



interface()

# fuzz = fuzzyPlayer.algorithm()

# # print fuzz.one.reasoner.inputs

# # for x in range(6,7):
# # 	for iinp in fuzz.one.reasoner.inputs:
# # 		print iinp.name, iinp.calculate_memberships(6)

# # for center, sigma in [[0.40900298369, 15.57906409119],
# # [33.8130835241, 5.82874647569],
# # [21.0191560734, 3.75449046552],
# # [64.0, 15.18721932131]]:

# # 	print np.exp(-((6 - center) ** 2.) / float(sigma) ** 2.)


# one  = fuzz.one.reasoner.inference([10, 0, 1, 10, 0, 1, 10, 0, 1, 6])
# # 		# if (np.isnan(one)):
# # 		# 	print x

# print one

###### time measurement tool

# import cProfile, pstats, StringIO
# pr = cProfile.Profile()
# pr.enable()

	# place function here

# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats() 
# print s.getvalue()