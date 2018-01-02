import numpy
from scipy import stats
import math
import sys
import operator



k = 1
errorCount = 0

f1 = open("hw2train.txt", 'r')
ltrain = [map(int, line.split(' ')) for line in f1]
f2 = open("hw2validate.txt", 'r')
lvalidate = [map(int, line.split(' ')) for line in f2]
f3 = open("hw2test.txt", 'r')
ltest = [map(int, line.split(' ')) for line in f3]
f4 = open("projection.txt", 'r')
lproj = [map(float, line.split(' ')) for line in f4]



def main():

	count = 0.0
	index = 0
	label = []
	arr = []
	newTraining = []
	finalM = [[0 for i in range(len(lproj[0]) + 1)] for j in range(len(ltrain))]
	for i in range(len(ltrain)):
		newTraining.append(ltrain[i][:-1])
		label.append(ltrain[i][-1])


	for i in range(len(newTraining)):
		for j in range(len(lproj[0])):
			for k in range(len(newTraining[0])):
				finalM[i][j] += newTraining[i][k] * lproj[k][j]
	#newTraining = numpy.dot(ltrain[:][:], lproj)
	
	#print "length : " + str(len(label)) + " " + str(len(newTraining[0]))
	
	#for i in range(len(label)):
	#	for j in range(len(newTraining[0])):
			#print "i: " + str(i) + "  j: " + str(j)
	#		finalM[i].append(newTraining[i][j])

	for i in range(len(newTraining)):
		finalM[i][-1] = label[i]



	#print "length : " + str(len(finalM)) + " " + str(finalM[500])
	
	inputFile = arr;
	arr = numpy.array(finalM)
	print "length : " + str(len(arr)) + " " + str(len(arr[0]))
	
	inputFile = arr;
	for tempdata in inputFile:
		data = tempdata[:-1]
		computedList = [(numpy.linalg.norm(data[:len(data)-1] - tar[:len(tar)-1]), tar) for tar in arr ]
		
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