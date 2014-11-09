
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


class FeatureExtractor:
    
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
        self.f_include_categories = []
        
        # By default, we want to include all the categories in our output.
        for i in range(CATEGORY_COUNT):
            self.f_include_categories.append(True)
        