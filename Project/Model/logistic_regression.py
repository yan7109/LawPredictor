import numpy
import sys
sys.path.append('../FeatureExtractor/')
import feature_extractor
from sklearn import linear_model
import random

TRAINING_SET_SIZE = 4000
TESTING_SET_SIZE = 500


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
    

# To start, create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# If the gram size is too big, logistic regression either runs out
# of memory or takes a long time to complete.
fe.change_words_gram_size(1)
fe.include_all_categories()

cases_relative_path = 'Cases'
all_features = fe.compute_word_weights_to_hold_result(cases_relative_path)

# Get all possible words.
words = set()
for feature in all_features:
    X = feature[0]
    for key in X:
        words.add(key)
words = list(words)

# Get desired data and split into traing and testing
fe.include_all_categories()

# Dont count held section because we are predicting it
fe.change_section_weight(feature_extractor.INDEX_SEC_HELD, 0)

# Not sure what is in this but it is excluded in python section
fe.change_section_weight(feature_extractor.INDEX_SEC_DISCUSSION, 0)

feature_vectors = fe.compute_word_weights_to_hold_result(cases_relative_path)
random.shuffle(feature_vectors)

# Check that there is enough data
if(TRAINING_SET_SIZE + TESTING_SET_SIZE > len(feature_vectors)):
    print("ERROR: Not enough data for training and testing set sizes.")
    exit(0)

# Split into training and testing data
training_features = feature_vectors[0:TRAINING_SET_SIZE]

testing_features = feature_vectors[TRAINING_SET_SIZE:TRAINING_SET_SIZE + TESTING_SET_SIZE]

# Print number of positive and negative examples in the training set
pos = 0
neg = 0
for training_example in training_features:
    if(training_example[1] == 0):
        pos = pos + 1
    else:
        neg = neg + 1

print("Number of negative examples in training: " + str(neg))
print("Number of positive examples in training: " + str(pos))

pos = 0
neg = 0
for testing_example in testing_features:
    if(testing_example[1] == 0):
        pos = pos + 1
    else:
        neg = neg + 1

print("Number of negative examples in testing: " + str(neg))
print("Number of positive examples in testing: " + str(pos))

# Train:
print("Training...")
#fe.include_all_categories()
#fe.exclude_category(feature_extractor.INDEX_CONTRACTS)

#training_features = fe.compute_word_weights_to_hold_result(cases_relative_path)

(X, y) = transform_features_to_matrix(training_features, words)

logreg = linear_model.LogisticRegression()
logreg.fit(X, y)

# Compute training set error:

predicted_y = logreg.predict(X)

# Now calculate accuracy:
n_samples = len(y)
n_correct = 0
for i in range(0, n_samples):
    if y[i] == predicted_y[i]:
        n_correct += 1

print("Training set accuracy: %f%%" % (float(n_correct) / n_samples * 100.0))


# Test:
print("Testing...")
# fe.exclude_all_categories()
# fe.include_category(feature_extractor.INDEX_CONTRACTS)

# testing_features = fe.compute_word_weights_to_hold_result(cases_relative_path)

(X, actual_y) = transform_features_to_matrix(testing_features, words)

predicted_y = logreg.predict(X)

# Now calculate accuracy:
n_samples = len(actual_y)
n_correct = 0
for i in range(0, n_samples):
    if actual_y[i] == predicted_y[i]:
        n_correct += 1

print("Testing set accuracy: %f%%" % (float(n_correct) / n_samples * 100.0))

# Output: Accuracy: 75.311721%
