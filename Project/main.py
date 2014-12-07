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
TOTAL_SET_SIZE = 5863

TRAINING_NEGATIVE_SIZE = 1900
TRAINING_POSITIVE_SIZE = 1900

TESTING_NEGATIVE_SIZE = 199
TESTING_POSITIVE_SIZE = 199

# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.include_all_categories()
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

cases_relative_path = 'Cases'

features = fe.compute_word_weights_to_hold_result(cases_relative_path, 20, 20)
num_pos = 0
num_neg = 0
for feature in features:
	if feature[1] == 0:
		num_pos += 1
	else:
		num_neg += 1
print("Total number of positive examples: %d" % num_pos)
print("Total number of negative examples: %d" % num_neg)

# Shuffle works in place
random.shuffle(features)

# Split into training and testing data
training = features
testing = []

# Impose TRAINING_POSITIVE_SIZE and TRAINING_NEGATIVE_SIZE
cur_num_train_pos = 0
cur_num_train_neg = 0
real_training = []
counter = 0
while counter < len(training):
	cur_train = training[counter]
	counter += 1
	if cur_train[1] == 0 and cur_num_train_pos != TRAINING_POSITIVE_SIZE:
		real_training.append(cur_train)
		cur_num_train_pos += 1
	elif cur_train[1] == -1 and cur_num_train_neg != TRAINING_NEGATIVE_SIZE:
		real_training.append(cur_train)
		cur_num_train_neg += 1
	else:
		# This example is not used in training, put it in testing
		testing.append(cur_train)
training = real_training

# Impose TESTING_POSITIVE_SIZE and TESTING_NEGATIVE_SIZE
cur_num_test_pos = 0
cur_num_test_neg = 0
real_testing = []
counter = 0
while (cur_num_test_pos != TESTING_POSITIVE_SIZE or cur_num_test_neg != TESTING_NEGATIVE_SIZE) and counter < len(testing):
	cur_test = testing[counter]
	counter += 1
	if cur_test[1] == 0 and cur_num_test_pos != TESTING_POSITIVE_SIZE:
		real_testing.append(cur_test)
		cur_num_test_pos += 1
	if cur_test[1] == -1 and cur_num_test_neg != TESTING_NEGATIVE_SIZE:
		real_testing.append(cur_test)
		cur_num_test_neg += 1
testing = real_testing

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

a = svmModel(training)
#print a.crossValidation(10)
a.train('-g 0.05')

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
print(cm)

# Display the confusion matrix
plt.matshow(cm)
plt.title('SVM confusion matrix')
plt.colorbar()
plt.ylabel('True Holding Result (0: not held, 1: held)')
plt.xlabel('Predicted Holding Result')
plt.show()
