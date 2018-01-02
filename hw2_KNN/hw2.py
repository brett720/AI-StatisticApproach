"""
Tianyi Li 
A12002286
Section B 
"""
import numpy
from scipy import stats
import math
import sys
import operator

k = 1
test = []

def main():

	count = 0.0
	index = 0
	training = []
	validation = []
	test =[]

	for x in open("hw2train.txt").read().splitlines():
		training += [numpy.array(map(int, x.rstrip().split()))]
	for x in open("hw2validate.txt").read().splitlines():
		validation += [numpy.array(map(int, x.rstrip().split()))]
	for x in open("hw2test.txt").read().splitlines():
		test += [numpy.array(map(int, x.rstrip().split()))]
	for x in open("projection.txt").read().splitlines():
		proj += [numpy.array(map(float, x.rstrip().split()))]

	for data in inputFile:

		computedList = [(numpy.linalg.norm(data[:len(data)-1] - tar[:len(tar)-1]), tar) for tar in training ]

		computedList.sort(key=operator.itemgetter(0))
		res = computedList[:k]
		
		pred = [(z[-1]) for (x,z) in res]
		prediction = stats.mode(pred)[0][0]
		
		if prediction != data[-1]:
			count += 1.0
		index += 1

	print "count : " + str(count)
	print "error p% = " + str((count/len(inputFile)))
	print ""

if __name__=="__main__":
	main()