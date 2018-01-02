import numpy
from scipy import stats
import math
import sys
import operator

class cont:
	label = 0
	alpha = -1
	error = 0.0
	calculatedResult = 0
	feature = -1
	tempList = []

	def __init__(self, lab, alp, fea):
		self.tempList = []
		self.label = lab
		self.alpha = alp
		self. calculatedResult = 0
		self.error = 0.0
		self.feature = fea

	def changeError(self, err):
		self.error = err
	def recResult(self, res):
		self.calculatedResult = res


def boostAlg(weight, train):
	err = 99999999
	fea = -1
	label = 0
	

	for i in range(len(train[0]) - 1):

		cur_err = 0
		for j in range(len(train)):
			if(train[j][i] > 0):
				te = 1 
			else:
				te = -1
			if(te != train[j][-1]):
				cur_err += weight[j]

		if (cur_err <= err):
			fea = i
			err = cur_err
			label = 1

		if (err >= 1.0 - cur_err):
			label = -1
			fea = i
			err = 1.0 - cur_err
			

	diffErr = 1.0 - err
	temp = numpy.log(((diffErr)/err))/2.0

	for i in range(len(train)):
		if (label == 1):
			if (train[i][fea] == 1):
				tempNum = 1
			else:
				tempNum = -1
		else:
			if(train[i][fea] == -1):
				tempNum = 1
			else:
				tempNum = -1

		tempNum = checkPositive(train[i][fea]) if label > 0 else \
          checkPositive(not train[i][fea])
		tempNum1 = numpy.exp(-tempNum * train[i][-1] * tempNum)
		weight[i] = numpy.exp(-(numpy.log(((diffErr)/err))/2.0)  * tempNum * train[i][-1]) * weight[i]
	
	weight = map(lambda elm: elm/sum(weight), weight)

	retData = cont(label, temp, fea)
	return (retData, weight)

def checkPositive(val): return -1 if val != 1 else 1

def main():

	training = []
	testing = []
	dictionary = []

	t = 4
	result = []
	for x in open("hw6train.txt").read().splitlines():
		training += [numpy.array(map(int, x.rstrip().split()))]

	for x in open("hw6test.txt").read().splitlines():
		testing += [numpy.array(map(int, x.rstrip().split()))]
	dictionary = open("hw6dictionary.txt").read().splitlines()

	size = len(training)

	weight = [1.0/size] * size
	classifierRes = []
	allData = [training, testing]

	for i in range(t):
		(rec, weight) = boostAlg(weight, training)
		# for test in weight:
		# 	print test
		
		classifierRes.append(rec)
		

	for i,data in enumerate(allData):
		count = 0
		for eachData in data:
			
			tempResult = numpy.sign(sum(checkPositive(not eachData[co.feature]) * co.alpha) if co.label != 1 else co.alpha * checkPositive(eachData[co.feature]) for co in classifierRes)
			if tempResult != eachData[-1]:
				count += 1
		#print count/float(len(data))

	for c in classifierRes:
		if (c.label > 0):
			print dictionary[c.feature]
	print "--------------------"
	for c in classifierRes:
		if (c.label < 0):
			print dictionary[c.feature]
if __name__=="__main__":
	main()