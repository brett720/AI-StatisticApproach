import numpy
import math
import sys


def classifier(preceptron, testPoint):
  sum = 0
  sign = 1
  for (w, c) in preceptron:
    if numpy.dot(w, testPoint) <= 0:
      sign = -1
    else:
      sign = 1
    sum = sum + (c * sign)
  if sum <= 0:
    return -1
  return 1

def perceptron (data, labels, l, reps):
  # start with a zero vector of size 819
  w = numpy.zeros(len(data[0]))
  for r in range(reps):
    for t in range(len(data)):
      dotProduct = numpy.dot(w, data[t])
      if (labels[t] == l):
        target_label = 1
      else:
        target_label = -1
      cond = target_label * dotProduct
      if cond <= 0:
        w = numpy.add(w, numpy.multiply(target_label,data[t]))
  return [(w,1)]
  
def votedPerceptron(data, labels, l, reps):
  c = 1
  w = numpy.zeros(len(data[0]))
  results = []
  for r in range(reps):
    for t in range(len(data)):
      # Get the +/- value of the label
      if (labels[t] == l):
        yt = 1
      else:
        yt = -1
      if  yt * numpy.dot(w, data[t]) <= 0:    
        #store the previous w and c
        results.append((w, c))
        # update the w and reset the c
        w = numpy.add(w, numpy.multiply(yt,data[t]))
        c = 1
      else:
        c = c + 1

  results.append((w, c))
  return results

def averagePerceptron(data, labels, l, reps):
  perceptron = votedPerceptron(data, labels, l, reps)
  sum = numpy.zeros(len(data[0]))
  for (w,c) in perceptron:
    sum = numpy.add(sum,numpy.multiply(c, w))
  return [(sum,1)]

def testError(test_data, labels, classifier, l):
  incorrect = 0
  for t in range(len(test_data)):
    if classifier(test_data[t]) == -1:
      if labels[t] == l:
        incorrect += 1
    else:
      if labels[t] != l:
        incorrect += 1
        
  return incorrect/float(len(test_data))


  
  
'''
def testError(test_data, labels, c, l):
  incorrect = 0
  for t in range(len(test_data)):
    if numpy.dot(w, test_data[t]) <= 0:
      if labels[t] == l:
        incorrect += 1
    else:
      if labels[t] != l:
        incorrect += 1
  return incorrect/float(len(test_data))
'''

def count(labels):
  dict = {}
  
  for l in labels:
    dict[l] = 0
    
  return len(dict)

def highest_lowest(perc):
  x = zip(perc, range(len(perc)))
  x.sort()
  return x[-3:]+x[:3]

def superClassifier(data, classifiers):
  label = []
  i = 1

  for c in classifiers:
    if c(data) > 0:
      label.append(i)
    i = i + 1   

  if len(label) == 1:
  	return label[0]

  return 0


def countLabels(labels):
  count = [0,0,0,0,0,0]
  for i in range(len(labels)):
  	count[int(labels[i])-1] += 1
  return count

def confusionMatrix(data, labels, classifier):
  matr = numpy.zeros((7,6), dtype = numpy.float)
  count = countLabels(labels)  

  for i in range(len(data)):
    matr[classifier(data[i])][int(labels[i]-1)] += 1
  
  for i in range(0,7):
  	for j in range(0,6):
  		matr[i][j] = matr[i][j] / float(count[j])  
  return matr

  
  

if __name__ == '__main__':

  with open("hw4dictionary.txt") as f:
    dictionary = f.readlines()

  #this is a matrix, the same index for this is used for the labels
  dataset_train = numpy.loadtxt("hw4train.txt",delimiter=" ",usecols=range(0,819))
  #this is a row vector, it contains the labels for the rows in the dataset
  labels_train = numpy.loadtxt("hw4train.txt",delimiter=" ",usecols=(819,)).flatten()

  dataset_test = numpy.loadtxt("hw4test.txt",delimiter=" ", usecols=range(0,819))
  labels_test = numpy.loadtxt("hw4test.txt",delimiter=" ",usecols=(819,)).flatten()

  dataset_newtrain = []
  labels_newtrain = []
  
  normPerc = []

  

  for i in range(1,7):
    normPerc.append(perceptron(dataset_train,labels_train, i, 1))

  normClassifier = []
  #for perc_i in range(len(normPerc)):
  normClassifier.append(lambda x: classifier(normPerc[0], x))
  normClassifier.append(lambda x: classifier(normPerc[1], x))
  normClassifier.append(lambda x: classifier(normPerc[2], x))
  normClassifier.append(lambda x: classifier(normPerc[3], x))
  normClassifier.append(lambda x: classifier(normPerc[4], x))
  normClassifier.append(lambda x: classifier(normPerc[5], x))

  print normPerc
  superClass = (lambda x: superClassifier(x, normClassifier))

  print confusionMatrix(dataset_test, labels_test, superClass)
  #print testError (dataset_train, labels_train, superClass, 1)

  #count_of_labels = countLabels(labels_train)
  #print count_of_labels

  
  for i in range(len(labels_train)):
    if labels_train[i] == 1 or labels_train[i] == 2:
      dataset_newtrain.append(dataset_train[i])
      labels_newtrain.append(labels_train[i])
      
  dataset_newtrain = numpy.array(dataset_newtrain)
  labels_newtrain = numpy.array(labels_newtrain)
  
  #create the perceptrons
  normPerc = []
  votedPerc = []
  averagePerc = []
  for i in range(1,5):
    normPerc.append(perceptron(dataset_newtrain, labels_newtrain, 1, i))
    votedPerc.append(votedPerceptron(dataset_newtrain,labels_newtrain,1, i))
    averagePerc.append(averagePerceptron(dataset_newtrain, labels_newtrain,1, i))
  
  #create the classifiers
  normClassifier = []
  votedClassifier = []
  averageClassifier = []
  for i in range(4):
    normClassifier.append(lambda x: classifier(normPerc[i], x))
    votedClassifier.append(lambda x: classifier(votedPerc[i], x))
    averageClassifier.append(lambda x: classifier(averagePerc[i], x))
    

  for i in range(4):
    print "Numtimes: %d" % (i+1)
    print testError(dataset_newtrain, labels_newtrain, normClassifier[i], 1)
    print testError(dataset_newtrain, labels_newtrain, votedClassifier[i], 1)
    print testError(dataset_newtrain, labels_newtrain, averageClassifier[i], 1)

    
  print "Highest, lowest: "
  dict_words = highest_lowest(averagePerc[2][0][0])
  
  
  dict_words = map(lambda x: dictionary[x[1]], dict_words)
  print dict_words
  