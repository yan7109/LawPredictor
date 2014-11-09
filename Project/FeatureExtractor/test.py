import feature_extractor


# To start, must create a FeatureExtractor object.
fe = feature_extractor.FeatureExtractor()

# You can pick which categories you want to include in the output.
fe.exclude_all_categories()
fe.include_category(feature_extractor.INDEX_ETHICS)
fe.include_category(feature_extractor.INDEX_PROPERTY)
fe.include_all_categories()
fe.exclude_category(feature_extractor.INDEX_CONTRACTS)

# You can also change the weight of each section.
# By default, all sections have the same weight: 1.0
# The weight goes from 0.0 to 1.0.
# For example, if you think "Facts" section is only half as important as other sections:
fe.change_section_weight(feature_extractor.INDEX_SEC_FACTS, 0.5)

# And if you think "Synopsis" is only 1/3 as important as other sections:
fe.change_section_weight(feature_extractor.INDEX_SEC_SYNOPSIS, 0.33)

# Now, exactly what does weight of section mean?
# For each word appeared in a section, we add that section's weight toward the word's weight.
# For example, assume we have two sections "SectionOne" with weight 0.5 and "SectionTwo" with weight 0.7.
# And this is their content:
# "SectionOne": I buy a new car today, I eat a cake
# "SectionTwo": I like the weather of today, today is good
# Output:
# "I"       : 0.5 + 0.5 + 0.7 = 1.7
# "buy"     : 0.5
# "today"   : 0.5 + 0.7 + 0.7 = 1.9
# "weather" : 0.7
# ... ...
# 
# Therefore, if all sections have weight of 1.0 (the default), you are simply doing a word
# count for each word from all sections.
# If a particular section has weight of 0.0, you are ignoring that section completely.

# Now, finally, to get the feature you want:
# cases_root_path is the directory containing "Administrative Law", "Business Associations", etc...
cases_root_path = 'C:\Users\Tianyi\Documents\GitHub\LawPredictor\Project\Cases'
features = fe.compute_word_weights_to_hold_result(cases_root_path)
