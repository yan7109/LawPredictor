import sys
import random
sys.path.append('FeatureExtractor/')
sys.path.append('Model/')
sys.path.append('../lib/libsvm-3.19/python/')
import feature_extractor
from svmModel import *

from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt


# Set training set size
# A random sample of this size will be taken from the data
TRAINING_SET_SIZE = 5000

TESTING_SET_SIZE = 836

# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.include_all_categories()
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

cases_relative_path = 'Cases'

features = fe.compute_word_weights_to_hold_result(cases_relative_path, 20, 20)

# Shuffle works in place
random.shuffle(features)

# Check that there is enough data
if TRAINING_SET_SIZE + TESTING_SET_SIZE > len(features):
	print("ERROR: Not enough data for training and testing set sizes.")
	exit(0)

# Split into training and testing data
training = features[0 : TRAINING_SET_SIZE]
testing = features[TRAINING_SET_SIZE : TRAINING_SET_SIZE + TESTING_SET_SIZE]

# Print number of positive and negative examples in the training set
pos = 0
neg = 0
for training_example in training:
	if training_example[1] == 0:
		pos += 1
	else:
		neg += 1

print("Number of negative examples in training: %d" % neg)
print("Number of positive examples in training: %d" % pos)

pos = 0
neg = 0
for testing_example in testing:
	if testing_example[1] == 0:
		pos += 1
	else:
		neg += 1

print("Number of negative examples in testing: %d" % neg)
print("Number of positive examples in testing: %d" % pos)

# convert from dictionary to vector

# X_train, X_test, y_train, y_test = cross_validation.train_test_split(features[0], features[1], test_size=0.4, random_state=0)

# # X_train.shape
# # y_train.shape

# # X_test.shape
# # y_test.shape

# clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
# clf.score(X_test, y_test) 

a = svmModel(training, testing)
#print a.crossValidation(10)
a.train()

# Test

# Split up testing set into features and labels
test_y = [0] * len(testing)
test_x = [0] * len(testing)
for i in range(len(testing)):
	test_y[i] = testing[i][1]
	test_x[i] = testing[i][0]

pred_labels, (ACC, MSE, SCC), pred_values = a.predict(test_y, test_x)

# See how many were predicted as 0
count = 0
for y in pred_labels:
    if y == 0:
        count += 1
print("%d testing examples were predicted as 0." % count)

print("The prediction accuracy is %f" % ACC)
#print("Prediction results:")
#print pred_labels
#print("Real results:")
#print test_y

#  prob  = svm_problem(y, x)
# >>> param = svm_parameter('-t 0 -c 4 -b 1')
# >>> m = svm_train(prob, param)

# p_label, p_acc, p_val = svm_predict(y, x, m, '-b 1')
# >>> ACC, MSE, SCC = evaluations(y, p_label)

# Compute confusion matrix
cm = confusion_matrix(test_y, pred_labels)

# Display the confusion matrix
plt.matshow(cm)
plt.title('SVM confusion matrix')
plt.colorbar()
plt.ylabel('True Holding Result (0: not held, 1: held)')
plt.xlabel('Predicted Holding Result')
plt.show()
