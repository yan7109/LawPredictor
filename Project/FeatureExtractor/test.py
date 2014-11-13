import feature_extractor

import json
import os


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
cases_relative_path = 'Cases'
features = fe.compute_word_weights_to_hold_result(cases_relative_path)

# Now you can feed 'features' into your ML algorithm.
# Beware of massive output:
f = open('features', 'w')
f.write(json.dumps(features))
f.close()

# This is part of the content of 'features' so you know what format it is in:
#[({'represent': 1.0, 'negligence': 0.5, 'september': 0.5, 'caused': 0.5, ... ... 'the': 15.66, 'order': 1.0, 'affirmed': 1.0}, 0),
# ({'holds': 1.0, 'particularly': 1.0, 'money': 0.5, ... ... 'affirmed': 1.0, 'pay': 0.5, 'the': 17.83, 'corporate': 7.33, 'grossly': 1.0}, -1),
# ... ...
# ... ...
# ({'limited': 1.0, 'innocuous': 1.0, 'office': 2.0, ... ... 'the': 21.65, 'furthermore': 1.0, 'violation': 1.0}, 0)]
#
# Basically 'features' is an array of tuple, each tuple represents a case.
# The first element of the tuple is a dictionary from word to word's weight.
# The second element of the tuple is the holding result: 0 for positively held, -1 for negatively held.
