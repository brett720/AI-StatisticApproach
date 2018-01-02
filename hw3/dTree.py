import math
import numpy
import re
from scipy import stats
import sys
import operator

class Node:
	def __init__(self, data):
		self.left = None
		self.right = None
		self.label = -1
		self.threshold = -1
		self.indice = -1
		self.dataSet = data
		self.leaf = True
		self.pure = checkPureSet(self.dataSet)
		if (self.pure == True):
			self.label = data[0][-1]
			

def checkPureSet(data):
	if (data == None):
		return False
	
	check = data[0][-1]

	for vect in data:
		if (check != vect[-1]):
			return False

	return True


def checkPureNode(node):
	#if (node is not None):
	#	if (node.pure == True) and (node.leaf == True):
	#		return node
	#	l = checkPureNode(node.left)
	#	if (l != None):
	#		return l
	#	r = checkPureNode(node.right)
	#	if (r != None):
	#		return r

		
	#else:
	#	return None

	#return None
	if node is None:
		return None
	if (node.pure != True) and (node.leaf == True):
		return node

	lefty = checkPureNode(node.left)
	if not(lefty is None):
		return lefty

	righty = checkPureNode(node.right)
	if not(righty is None):
		return righty

	return None


def findEntropy(dataSet):
	count = [0,0,0,0]
	totalCount = 0.0
	result = 0.0
	for i in range(len(dataSet)):
		label = int(dataSet[i][-1])
		count[label] = count[label] + 1
		totalCount += 1.0


	for j in count:
		if (j != 0):
			result = result - (j / totalCount) * math.log(j / totalCount)
	
	return result


def findFeatureEntropy(sortedSet, feature):
	smallestEntropy = 99999999.9
	currEnt = 99999999.9
	smallestTh = 99999999.9
	currTh = 99999999.9
	index = -1
	
	for i in range(len(sortedSet)):
		if(currTh != sortedSet[i][feature]):
			currTh = sortedSet[i][feature]

			left = []
			right = []
			for data in sortedSet:
				if data[feature] <= currTh:
					left.append(data)
				else:
					right.append(data)


			leftEnt = findEntropy(left)
			rightEnt = findEntropy(right)
			currEnt = (leftEnt * float(len(left)) / float(len(sortedSet)))
			currEnt = currEnt + (rightEnt * float(len(right)) / float(len(sortedSet)))
			
			if currEnt < smallestEntropy:
				smallestEntropy = currEnt
				smallestTh = currTh
				index = i

	return (smallestTh, smallestEntropy, index)



def main():
	training = []
	validation = []
	test = []
	feature = []

	# read file to list.
	# 
	for x in open("hw3train.txt").read().splitlines():
		training += [numpy.array(map(float, x.rstrip().split()))]

	for x in open("hw3validation.txt").read().splitlines():
		validation += [numpy.array(map(float, x.rstrip().split()))]

	for x in open("hw3test.txt").read().splitlines():
		test += [numpy.array(map(float, x.rstrip().split()))]

	with open("hw3features.txt") as f:
		feature = f.read().split()

	# Create decision tree
	# 
	
	root = Node(training)
	temp = checkPureNode(root)
	left = []
	right = []
	th = 999999.9
	myEntropy = 999999.9
	index = 0
	counter = 0
	while (temp != None):
		left = []
		right = []
		# TODO range
		for i in range(1):
			tempEntro = 0.0
			tempTh = 0.0
			tempIndex = 0
			training.sort(key = operator.itemgetter(i))

			(tempTh, tempEntro, tempIndex) = findFeatureEntropy(training, i)
			if(tempEntro < myEntropy):
				myEntropy = tempEntro
				th = tempTh
				index = tempIndex


		print "th is " + str(th)
		for data in temp.dataSet:
			if data[i] <= th:
				left.append(data)
			else:
				right.append(data)
			
		temp.threshold = th
		temp.indice = index
		temp.leaf = False
		temp.left = Node(left)
		temp.right = Node(right)
		print str(len(left)) + "  " + str(len(right))
		temp = checkPureNode(root)

if __name__=="__main__":
	main()
