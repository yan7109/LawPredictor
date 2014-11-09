import feature_extractor

# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.exclude_all_categories()
fe.include_category(feature_extractor.INDEX_ETHICS)
fe.include_category(feature_extractor.INDEX_PROPERTY)
fe.include_all_categories()
fe.exclude_category(feature_extractor.INDEX_CONTRACTS)
