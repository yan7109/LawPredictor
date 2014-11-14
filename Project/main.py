import json
import os
import sys
import random
sys.path.append('FeatureExtractor/')
sys.path.append('Model/')
sys.path.append('../lib/libsvm-3.19/python/')
import feature_extractor
from svmModel import *

# Set training set size
# A random sample of this size will be taken from the data
TRAINING_SET_SIZE = 500

# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.include_all_categories()
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

cases_relative_path = 'Cases'
features = fe.compute_word_weights_to_hold_result(cases_relative_path)

feature_vectors_sample = [ features[i] for i in sorted(random.sample(xrange(len(features)), TRAINING_SET_SIZE)) ]

# Print number of positive and negative examples in the training set
pos = 0
neg = 0
for example in feature_vectors_sample:
	if(example[1] == 0):
		pos = pos + 1
	else:
		neg = neg + 1

print("Number of negative examples: " + str(neg))
print("Number of positive examples: " + str(pos))


a = svmModel(feature_vectors_sample)
print a.crossValidation(10)

#10-fold Cross Validation Accuracy = 95.1337%
