import numpy
import sys
sys.path.append('../FeatureExtractor/')
import feature_extractor
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import random

numpy.set_printoptions(threshold=numpy.nan)

def transform_features_to_matrix(features, words):
    
    print("Number of samples is %d" % len(features))
    print("Number of features is %d" % len(words))
    
    X = numpy.zeros((len(features), len(words)))    # n_samples X n_features
    y = []
    cur_sample_num = 0
    for feature in features:
        X_val = feature[0]
        y_val = feature[1]
        
        for key in X_val:
            index = words.index(key)
            X[cur_sample_num][index] += X_val[key]
        
        y.append(y_val)
        
        cur_sample_num += 1
    
    return (X, y)


# Set training set size
# A random sample of this size will be taken from the data
TOTAL_SET_SIZE = 5863

TRAINING_NEGATIVE_SIZE = 1900
TRAINING_POSITIVE_SIZE = 1900

TESTING_NEGATIVE_SIZE = 200
TESTING_POSITIVE_SIZE = 200

# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.include_all_categories()
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

fe.change_words_gram_size(1)

cases_relative_path = 'Cases'

features = fe.compute_word_weights_to_hold_result(cases_relative_path, 0, 0)
num_pos = 0
num_neg = 0
for feature in features:
    if feature[1] == 0:
        num_pos += 1
    else:
        num_neg += 1
print("Total number of positive examples: %d" % num_pos)
print("Total number of negative examples: %d" % num_neg)

# Build dictionary of words
words = set()
for feature in features:
    X = feature[0]
    for key in X:
        words.add(key)
words = list(words)

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

# Train:
print("Training...")
(X, y) = transform_features_to_matrix(training, words)

clf = RandomForestClassifier(n_estimators=10,max_depth=6)
clf.fit(X, y)

# Compute training set error:
predicted_y = clf.predict(X)

# Now calculate accuracy:
n_samples = len(y)
n_correct = 0
for i in range(0, n_samples):
    if y[i] == predicted_y[i]:
        n_correct += 1
print("Training set accuracy: %f%%" % (float(n_correct) / n_samples * 100.0))

# Test:
print("Testing...")
(X, actual_y) = transform_features_to_matrix(testing, words)

predicted_y = clf.predict(X)

# See how many were predicted as 0
count = 0
for y in predicted_y:
    if y == 0:
        count += 1
print("%d testing examples were predicted as 0." % count)

# Now calculate accuracy:
n_samples = len(actual_y)
n_correct = 0
for i in range(0, n_samples):
    if actual_y[i] == predicted_y[i]:
        n_correct += 1
print("Testing set accuracy: %f%%" % (float(n_correct) / n_samples * 100.0))

# Compute confusion matrix
cm = confusion_matrix(actual_y, predicted_y)
print(cm)

# Display the confusion matrix
plt.matshow(cm)
plt.title('Random Forests confusion matrix')
plt.colorbar()
plt.ylabel('True Holding Result (0: not held, 1: held)')
plt.xlabel('Predicted Holding Result')
plt.show()
