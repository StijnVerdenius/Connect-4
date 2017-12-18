

import boardDef
import players.MonteCarlos.monteCarlos as monteCarlos
import players.fuzzyAgent.fuzzyPlayer as fuzzyPlayer

def pcMove(board, opponent, arguments, symbol):
	""" doing a move for a ai player """
	
	moveResult = False
	while (not moveResult):
		move = opponent.decideMove(board, symbol, arguments)

		print "Chosen Move: ", move[0]
		moveResult = board.doMove(move[0], symbol)


FUZZ_ARGUMENTS = [-0.1]
M_CARLOS_ARGUMENTS = [0.8]
monte = monteCarlos.algorithm()
fuzz = fuzzyPlayer.algorithm()


f  = open("score.csv", "a")

minuten = 60
monteeers = False

argumentsX = FUZZ_ARGUMENTS
argumentsO = M_CARLOS_ARGUMENTS
playerO = monte
playerX = fuzz
if (not monteeers):
	argumentsO = FUZZ_ARGUMENTS
	argumentsX = M_CARLOS_ARGUMENTS
	playerO = fuzz
	playerX = monte

for x in range(int(minuten/5.5)):
	krossOnMove = False
	stri = ""
	board = boardDef.board()
	while (  not board.checkVictory("O") and not board.checkVictory("X") and board.movesMade < 64 ):
		print "current board in game "+ str(x)+"/"+str(int(minuten/7.5))+":"
		board.toString()
		print "move is on : "
		if (krossOnMove):
			print "X"
		else:
			print "O"

		if (krossOnMove):
			pcMove(board, playerX, argumentsX, "X")
		else:
			pcMove(board, playerO, argumentsO, "O")

		
		krossOnMove = not krossOnMove

	if (board.anyVictory() == "O"):
		stri = "1,0,"+str(board.movesMade)
	elif (board.anyVictory() == "X"):
		stri = "0,1,"+str(board.movesMade) 
	else:
		stri = "0,0,64"

	stri = stri + "\n"

	f.write(stri)



