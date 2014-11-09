#!/usr/bin/python

import graderUtil
import util
import time
from util import *

grader = graderUtil.Grader()
submission = grader.load('submission')

############################################################
# Problem 1: warmup
############################################################


############################################################
# Problem 2: classification
############################################################

# test the classifier on a large dataset
def test2bpolarity():
    trainExamples = readCases('Cases')
    devExamples = readCases('TestCases')
    featureExtractor = submission.extractExtraCreditFeatures
    weights = submission.learnPredictor(trainExamples, devExamples, featureExtractor)
    outputWeights(weights, 'weights')
    outputErrorAnalysis(devExamples, featureExtractor, weights, 'error-analysis')  # Use this to debug
    trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    devError = evaluatePredictor(devExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print "Official: train error = %s, dev error = %s" % (trainError, devError)
    #grader.requireIsLessThan(0.08, trainError)
    #grader.requireIsLessThan(0.30, devError)

grader.addBasicPart('2b-1', test2bpolarity, maxSeconds=300)

grader.grade()
