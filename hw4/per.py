import math
import numpy
import sys
from collections import defaultdict
from numpy import dot

collectedNum = []

def findBasicPer(training, passNum):
	wf = 0

	for _ in range(passNum):
		for item in training:
			if ((item[-1] *  numpy.sum(dot(item[0:(len(item) - 1)], wf))) <= 0):
				wf = wf + dot(item[-1],item[0:(len(item) - 1)])
				
	return wf

def errorAvePerceptron(testData, trainingVector):
	result = [0] * len(testData)

	for item in trainingVector:
		mulRes = trainingVector[item].c * trainingVector[item].w
		result = numpy.add(mulRes, result)
	collectedNum.append(result)
	dotRes = numpy.dot(result, testData)
	
	#print type(dotRes)
	
	return numpy.sign(dotRes)


def findVotedPer(training, passNum):
	res = defaultdict(wc)
	length = len(training[0])
	res[1].w = [0 for x in range(length-1)]

	m = 1

	for _ in range(passNum):
		for item in training:
			
			if int(item[-1] * numpy.sum(dot(res[m].w,item[0 : length-1]))) > 0:
				res[m].c += 1
			else:
				res[m+1].w = dot(item[-1],item[0 : length-1])
				res[m+1].w += res[m].w
				m += 1
				res[m].c = 1
				

	return res

class wc:
		w = []
		c = 1


def findPerError(testData, trainingVector, func):
	err = 0
	length = len(testData)
	res = 0
	for item in testData:
		res = func(item[0:(len(item)-1)], trainingVector)

		if (res != item[-1]):
			err += 1

	return err/float(length)



def errorVPerceptron(testData, trainingVector):
	result = 0
	for item in trainingVector:
		tempDot = numpy.dot(trainingVector[item].w,testData)
		result += numpy.sign(tempDot) * trainingVector[item].c 

	return numpy.sign(result)

def errorBPerceptron(testData, trainingVector):
	sumOfResult = numpy.dot(testData, trainingVector)
	return sumOfResult	



#====================================
def setTrainingData(training, index):
	newData = training
	for i in newData:
		if (i[-1] == index):

			i[-1] = -1
		else:
			i[-1] = 1
	return newData

def setTestingData(testing, index):
	testData = testing

	for i in testData:
		if (i[-1] == index):
			i[-1] = -1
		else:
			i[-1] = 1
	return testData

def findPerErrorForMatrix(testData, trainingVector, func, label):
	return 

def calc_confusion_matrix(training):
	matrix = [([0] * 6) for i in range(7)]

	label_counts = [0] * 6
	classifiers = []
	data =[]
	for i in range(1, 7):
		training = []
		for x in open("hw4train.txt").read().splitlines():
			training += [numpy.array(map(int, x.rstrip().split()))]

		data = setTrainingData(training, i)
		classifiers.append(findBasicPer(data, 1))
	labels = []
	index = 1

	testing = []
	for x in open("hw4test.txt").read().splitlines():
		testing += [numpy.array(map(int, x.rstrip().split()))]

	label = numpy.loadtxt("hw4test.txt",delimiter=" ",usecols=(819,)).flatten()
	findPerErrorForMatrix(testing, classifiers, errorBPerceptron,label)

	
#+===================================
def main():
	training = []
	testing = []
		
	for x in open("hw4train.txt").read().splitlines():
		training += [numpy.array(map(int, x.rstrip().split()))]

	for x in open("hw4test.txt").read().splitlines():
		testing += [numpy.array(map(int, x.rstrip().split()))]

	passNum = 1
	c = 0
	training12 = []
	testing12 = []
	for i in training:
		if(i[-1] == 1):
			training12.append(i)
		if(i[-1] == 2):
			i[-1] = -1
			training12.append(i)
	
	for i in testing:
		if(i[-1] == 1):
			testing12.append(i)
		if(i[-1] == 2):
			i[-1] = -1
			testing12.append(i)
	
	#resultVector = findBasicPer(training12, passNum)
	#result = findPerError(testing12, resultVector, errorBPerceptron)
	resultWc = findVotedPer(training12, passNum)
	result = findPerError(training12, resultWc, errorAvePerceptron)
	#print str(result * 100)
	#
	filename = open('hw4dictionary.txt', 'r').read().split()
	wordList = []
	for word in filename:
		wordList.append(word)
	#print str(len(wordList))
	large3 = []
	small3 = []
	tempArray = []
	#print collectedNum[1089]
	for i in collectedNum[1089]:
		tempArray.append(i)

	for _ in range(3):
		temp = max(tempArray)
	#	print temp
		index = tempArray.index(temp)
		tempArray[index] = 0

	
	for _ in range(3):
		temp = min(tempArray)
		index = tempArray.index(temp)
		small3.append(index)
		tempArray[index] = 0

	#for i in range(3):
	#	print wordList[small3[i]]
	print calc_confusion_matrix(training)
if __name__=="__main__":
	main()



