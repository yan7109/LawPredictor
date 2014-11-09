#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *

############################################################
# Problem 2: binary classification
############################################################

############################################################
# Problem 2a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    features = collections.Counter();
    for word in x.split():
	features[word] += 1
    return features
    # END_YOUR_CODE

############################################################
# Problem 2b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (around 15 lines of code expected)

    numIters, eta = 19, 0.01
    for t in range(numIters):
        for example in trainExamples:
            phi = featureExtractor(example[0])
            if (dotProduct(phi, weights)*example[1] < 1):
                for key, value in phi.iteritems():
                    if (key not in weights):
                        weights[key] = 0
                    weights[key] = weights[key] - eta*(-value*example[1])
        trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        devError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        print "For iteration %s: train error = %s, test error = %s" % (t, trainError, devError)

    # END_YOUR_CODE
    return weights

############################################################
# Problem 2c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) can be anything (randomize!) with a nonzero score under the given weight vector
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        phi = collections.Counter()
        for key, val in weights.iteritems():
            phi[key] = random.randrange(-100, 100, 1)
        y = 1 if dotProduct(phi, weights) >= 0 else -1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 2f: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        output = collections.Counter()
        sentence = x.replace(' ','')
        for i in range (len(sentence) - n + 1):
            output[sentence[i:i+n]]+=1
        return output
        # END_YOUR_CODE
    return extract

############################################################
# Problem 2h: extra credit features

def extractExtraCreditFeatures(x):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    output = collections.Counter()
    sentence = ((''.join(c for c in x if x not in ('!','.',',','?','\\','-','\'','\"'))).lower()).split()
    for index, val in enumerate(sentence):
        for newIndex in xrange(index, index+2):
            output[''.join(sentence[index:newIndex+1])]+=1
    return output
    # END_YOUR_CODE

############################################################
# Problem 3: k-means
############################################################


def kmeans(examples, K, maxIters):
    
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (around 35 lines of code expected)

    centroids = []
    centroidCounts = [] #used to find mu, as how many examples are assigned to each centroid
    assignments = {}
    loss = 0
    for i in range(K): # initialize centroids
        centroids.append((examples[random.randrange(0,len(examples)-1, 1)]).copy())
        centroidCounts.append(0)
    for i in range(maxIters):
        for exampleIndex, example in enumerate(examples): #calculate k
            argmin = sys.maxint
            for centroidIndex, centroid in enumerate(centroids):
                sum = 0
                for key, val in example.iteritems():
                    sum += (val - centroid[key])**2
                if sum < argmin:
                    argmin = sum
                    assignments[exampleIndex] = centroidIndex

        for centroidIndex, centroid in enumerate(centroids): #update centroids
            for key, val in centroid.iteritems():
                centroid[key] = 0
        for exampleIndex, example in enumerate(examples):
            centroidIndex = assignments[exampleIndex]
            for key, val in (centroids[centroidIndex]).iteritems():
                centroids[centroidIndex][key] += example[key]
            centroidCounts[centroidIndex] +=1
        for centroidIndex, centroid in enumerate(centroids):
            for key, val in centroid.iteritems():
                centroid[key] = centroid[key] * 1.0 / centroidCounts[centroidIndex]
            centroidCounts[centroidIndex] = 0
    for exampleIndex, example in enumerate(examples):
        centroidIndex = assignments[exampleIndex]
        for key, val in (centroids[centroidIndex].iteritems()):
            loss += (example[key]-centroids[centroidIndex][key])**2

    return (centroids, assignments, loss)
    # END_YOUR_CODE
