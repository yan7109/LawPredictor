import utils

import fnmatch
import os
import string


# Global constant values.
CATEGORY_COUNT              = 20
INDEX_ADMINISTRATIVE_LAW    = 0
INDEX_CIVIL_PROCEDURE       = 1
INDEX_COMMERCIAL_LAW        = 2
INDEX_CONSTITUTIONAL_LAW    = 3
INDEX_CONTRACTS             = 4
INDEX_CORPORATIONS          = 5
INDEX_CRIMINAL_LAW          = 6
INDEX_CRIMINAL_PROCEDURE    = 7
INDEX_ETHICS                = 8
INDEX_EVIDENCE              = 9
INDEX_FAMILY_LAW            = 10
INDEX_INCOME_TAX            = 11
INDEX_PROPERTY              = 12
INDEX_TORTS                 = 13
INDEX_WILLS_TRUSTS_ESTATES  = 14
INDEX_INTERNATIONAL_LAW     = 15
INDEX_SECURITIES_REGULATION = 16
INDEX_BUSINESS_ASSOCIATIONS = 17
INDEX_PATENT_LAW            = 18
INDEX_HEALTH_LAW            = 19


SECTION_COUNT           = 7
INDEX_SEC_TITLE         = 0
INDEX_SEC_FACT_SUMMARY  = 1
INDEX_SEC_SYNOPSIS      = 2
INDEX_SEC_FACTS         = 3
INDEX_SEC_ISSUE         = 4
INDEX_SEC_HELD          = 5
INDEX_SEC_DISCUSSION    = 6

SECTION_WEIGHT_MAX = 1.0
SECTION_WEIGHT_MIN = 0.0


class FeatureExtractor:
    
    def compute_word_weights_to_hold_result_helper(self, file_path):
        word_to_weight = {}
        holding_result = 0
        
        with open(file_path) as f:
            cur_section_index = -1
            
            for line in f:
                line = line.strip().lower()
                if len(line) == 0:
                    continue
                
                if cur_section_index != -1:
                    for c in string.punctuation:
                        line = line.replace(c, ' ')
                        
                    if cur_section_index == INDEX_SEC_HELD:
                        # Special case, we need to find out the holding result.
                        holding_result = utils.get_holding_result(line)
                        
                    word_weight = self.section_weights[cur_section_index]
                    
                    words = line.split()
                    for word in words:
                        if word in word_to_weight:
                            word_to_weight[word] += word_weight
                        else:
                            word_to_weight[word] = word_weight
                    
                    cur_section_index = -1
                    continue
                
                cur_section_index = utils.section_name_to_index(line)
                
        return (word_to_weight, holding_result)
        
    def compute_word_weights_to_hold_result(self, cases_relative_path):
        result = []
        cases_full_path = os.path.join(os.path.dirname(__file__), cases_relative_path)
        categories_dir = os.listdir(cases_full_path)
        
        for category_dir in categories_dir:
            category_index = utils.category_dir_to_index(category_dir)
            
            # Check if we are ignoring this category.
            if not self.f_include_categories[category_index]:
                continue
            
            category_path = os.path.join(cases_full_path, category_dir)
            for root, dirnames, filenames in os.walk(category_path):
                for filename in fnmatch.filter(filenames, '*.txt'):
                    file_path = os.path.join(root, filename)
                    
                    cur_result = self.compute_word_weights_to_hold_result_helper(file_path)
                    result.append(cur_result)
                    
        return result
    
    def change_section_weight(self, section_index, weight):
        if weight < SECTION_WEIGHT_MIN:
            weight = SECTION_WEIGHT_MIN
        if weight > SECTION_WEIGHT_MAX:
            weight = SECTION_WEIGHT_MAX
        
        self.section_weights[section_index] = weight
    
    
    def include_category(self, category_index):
        self.f_include_categories[category_index] = True
    
    def exclude_category(self, category_index):
        self.f_include_categories[category_index] = False
    
    def include_all_categories(self):
        for i in range(CATEGORY_COUNT):
            self.f_include_categories[i] = True
    
    def exclude_all_categories(self):
        for i in range(CATEGORY_COUNT):
            self.f_include_categories[i] = False
    
    
    # Constructor.
    def __init__(self):
        
        # Instance variables.
        self.f_include_categories   = []
        self.section_weights        = []
        
        # By default, we want to include all the categories in our output.
        for i in range(CATEGORY_COUNT):
            self.f_include_categories.append(True)
        
        # By default, all sections have equal weight.
        for i in range(SECTION_COUNT):
            self.section_weights.append(SECTION_WEIGHT_MAX)
        
