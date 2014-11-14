import sys
sys.path.append('../FeatureExtractor/')
import feature_extractor
from sklearn import linear_model


def transform_features_to_matrix(features):
    for feature in features:
        X = feature[0]
        y = feature[1]
    

# To start, create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()
fe.include_all_categories()
fe.exclude_category(feature_extractor.INDEX_CONTRACTS)

cases_relative_path = 'Cases'
features = fe.compute_word_weights_to_hold_result(cases_relative_path)

(X, y) = transform_features_to_matrix(features)

logreg = linear_model.LogisticRegression()
logreg.fit(X, y)
