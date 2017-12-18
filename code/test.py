from random import choice
from copy import deepcopy

moveList = [55,55,55,55]

oldMax = max(moveList)
secondMoveList = deepcopy(moveList)
bestmoves = []
while (len(secondMoveList) > 0 and max(secondMoveList) == oldMax):
	oldMax = max(secondMoveList)
	ind1 = moveList.index(oldMax)
	moveList[ind1] = -11000000
	ind2 = secondMoveList.index(oldMax)
	secondMoveList.pop(ind2)
	bestmoves.append(ind1+1)
print bestmoves
print choice(bestmoves)