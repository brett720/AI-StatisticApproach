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

training = []
test = []
p = 5
testIndex = 0

for x in open("hw5train.txt").read().splitlines():
    training += [numpy.array(map(str, x.rstrip().split()))]
for x in open("hw5test.txt").read().splitlines():
    test += [numpy.array(map(str, x.rstrip().split()))]


def build_substring_matrix(data, length):

    return [[num_common_substr(data[x][0],data[y][0],length) for y in 
      xrange(len(data))] for x in xrange(len(data))]

def num_common_substr(str_1, str_2, length):

    sub_list = set()
    for idx in xrange(len(str_1)-(length-1)):
        if str_1[idx:idx+length] in str_2:
            if (str_1[idx:idx+length] not in sub_list):
                sub_list.add(str_1[idx:idx+length])

    print sub_list
    return len(sub_list)



def build_basic_perceptron(data, substr_len, sim_matrix, sought_class=1):
    w = [(0,0,0)]
    for idx, (protien, classification) in enumerate(data):
        dotio = reduce(lambda acc,(pro,clas,row):acc+clas*sim_matrix[row][idx],w,0)
        if int(classification) * dotio <= 0:
            w += [(protien, int(classification), idx)]
    return w

def classify_basic_perceptron(datum, train_data, w, k):
    x = reduce(lambda acc,(pro,clas,row):
      acc+clas*num_common_substr(data_training_a[row][0],datum, k),w,0)

    return numpy.sign(x)

def classify_perceptron_set(data, classifier, function, num, sought_class=1):
    error_count = 0

    for feature in data:
        res = function(feature[0],data,classifier, num)
        if res != int(feature[-1]):
            error_count += 1

    return str((error_count/float(len(data))) * 100) + "%"


def main():

    sim_matrix = build_substring_matrix(training, p)
    print sim_matrix
    bp = build_basic_perceptron(training, p, sim_matrix)
    print bp
    result = classify_perceptron_set(training, bp, 
          classify_basic_perceptron, p)

    print result
if __name__=="__main__":
    main()
    
