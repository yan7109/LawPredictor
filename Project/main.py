import json
import os
import sys
sys.path.append('FeatureExtractor/')
sys.path.append('Model/')
sys.path.append('../lib/libsvm-3.19/python/')
import feature_extractor
from svmModel import *


# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.include_all_categories()
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

cases_relative_path = 'Cases'
features = fe.compute_word_weights_to_hold_result(cases_relative_path)

a = svmModel(features)
print a.crossValidation(10)

#10-fold Cross Validation Accuracy = 95.1337%
