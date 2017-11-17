import skfuzzy as fuzz

class fuzzyTools(object):
	def __init__(self):
		pass
		

	## placeholder functies zodat we het systeem eerst werkende kunnen krijgen

	def membershipGauss(self, x, center, sigma, _):
		return fuzz.membership.gaussmf(x, center, sigma)

	def membershipTriangle(self, x, a, b, c):
		return fuzz.membership.trimf(x, [a,b,c])

	def membershipSigmoid(self, x, offset, width, _):
		return fuzz.membership.sigmf(x, offset, width)
		
	def cutOff(self, height, resolution, function, arguments):
		pass

	def fuzzyAnd(arguments):
		return min(arguments)

	def fuzzyOr(arguments):
		return max(arguments)

	def centroid(self, weights, step):
		counterWeight = 0.0
		counterGeneral = 0.0
		i = 0
		for weight in weights:

			counterGeneral += i*step*weight
			counterWeight += weight

		return counterGeneral/counterWeight

	

