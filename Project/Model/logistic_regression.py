import numpy
import sys
sys.path.append('../FeatureExtractor/')
import feature_extractor
from sklearn import linear_model


def transform_features_to_matrix(features, words):
    
<<<<<<< Updated upstream
    print("Number of samples is %d" % len(features))
    print("Number of features is %d" % len(words))
=======
    words = list(words)
>>>>>>> Stashed changes
    
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

# Train:
print("Training...")
fe.include_all_categories()

training_features = fe.compute_word_weights_to_hold_result(cases_relative_path)

(X, y) = transform_features_to_matrix(training_features, words)

logreg = linear_model.LogisticRegression()
logreg.fit(X, y)

# Test:
print("Testing...")
fe.exclude_all_categories()
fe.include_category(feature_extractor.INDEX_CONTRACTS)

testing_features = fe.compute_word_weights_to_hold_result(cases_relative_path)

(X, actual_y) = transform_features_to_matrix(testing_features, words)

predicted_y = logreg.predict(X)

# Now calculate accuracy:
n_samples = len(actual_y)
n_correct = 0
for i in range(0, n_samples):
    if actual_y[i] == predicted_y[i]:
        n_correct += 1

print("Accuracy: %f%%" % (float(n_correct) / n_samples * 100.0))
