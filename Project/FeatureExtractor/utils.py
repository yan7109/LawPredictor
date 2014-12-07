import feature_extractor


def category_dir_to_index(dir_name):
    if dir_name == 'Administrative Law':
        return feature_extractor.INDEX_ADMINISTRATIVE_LAW
    elif dir_name == 'Business Associations':
        return feature_extractor.INDEX_BUSINESS_ASSOCIATIONS
    elif dir_name == 'Civil Procedure':
        return feature_extractor.INDEX_CIVIL_PROCEDURE
    elif dir_name == 'Commercial Law':
        return feature_extractor.INDEX_COMMERCIAL_LAW
    elif dir_name == 'Constitutional Law':
        return feature_extractor.INDEX_CONSTITUTIONAL_LAW
    elif dir_name == 'Contracts':
        return feature_extractor.INDEX_CONTRACTS
    elif dir_name == 'Corporations':
        return feature_extractor.INDEX_CORPORATIONS
    elif dir_name == 'Criminal Law':
        return feature_extractor.INDEX_CRIMINAL_LAW
    elif dir_name == 'Criminal Procedure':
        return feature_extractor.INDEX_CRIMINAL_PROCEDURE
    elif dir_name == 'Ethics':
        return feature_extractor.INDEX_ETHICS
    elif dir_name == 'Evidence':
        return feature_extractor.INDEX_EVIDENCE
    elif dir_name == 'Family Law':
        return feature_extractor.INDEX_FAMILY_LAW
    elif dir_name == 'Health Law':
        return feature_extractor.INDEX_HEALTH_LAW
    elif dir_name == 'Income Tax':
        return feature_extractor.INDEX_INCOME_TAX
    elif dir_name == 'International Law':
        return feature_extractor.INDEX_INTERNATIONAL_LAW
    elif dir_name == 'Patent Law':
        return feature_extractor.INDEX_PATENT_LAW
    elif dir_name == 'Property':
        return feature_extractor.INDEX_PROPERTY
    elif dir_name == 'Securities Regulation':
        return feature_extractor.INDEX_SECURITIES_REGULATION
    elif dir_name == 'Torts':
        return feature_extractor.INDEX_TORTS
    elif dir_name == 'Wills, Trusts & Estates':
        return feature_extractor.INDEX_WILLS_TRUSTS_ESTATES
    else:
        return -1


def section_name_to_index(section_name):
    if section_name == 'title':
        return feature_extractor.INDEX_SEC_TITLE
    elif section_name == 'brief fact summary':
        return feature_extractor.INDEX_SEC_FACT_SUMMARY
    elif section_name == 'synopsis of rule of law':
        return feature_extractor.INDEX_SEC_SYNOPSIS
    elif section_name == 'facts':
        return feature_extractor.INDEX_SEC_FACTS
    elif section_name == 'issue':
        return feature_extractor.INDEX_SEC_ISSUE
    elif section_name == 'held':
        return feature_extractor.INDEX_SEC_HELD
    elif section_name == 'discussion':
        return feature_extractor.INDEX_SEC_DISCUSSION
    else:
        return -1


def get_holding_result(held_line):

    yes_index       = held_line.find('yes')
    affirm_index    = held_line.find('affirm')
    no_index        = held_line.find('no')
    
    yes_index = yes_index if yes_index <= affirm_index else affirm_index

    if yes_index >= 0 and no_index < 0:
        # print(held_line + " 0   \n\n\n\n\n")
        return 0
    elif no_index >= 0 and yes_index < 0:
        # print(held_line + " -1   \n\n\n\n\n")
        return -1
    elif no_index >= 0 and yes_index >= 0:
        # both appear
        # return whichever one came first
        if yes_index <= no_index:
            # print(held_line + " 0   \n\n\n\n\n")
            return 0
        else:
            # print(held_line + " -1   \n\n\n\n\n")
            return -1
    else:
        # neither appear
        # default to yes (but could remove in the future)
        # print(held_line + " 0   \n\n\n\n\n")
        return 0


def remove_stop_words(line):
    stop_words = [ ' i ', ' a ', ' about ', ' an ', 'and', ' are ', ' as ', ' at ', ' be ', \
                   ' by ', ' com ', ' for ', ' from ', ' how ', ' in ', ' is ', ' it ', \
                   ' of ', ' on ', ' or ', ' s ', ' that ', ' the ', ' this ', ' to ', ' was ', \
                   ' what ', ' when ', ' where ', ' who ', ' will ', ' with ', ' www ']
    
    for item in stop_words:
        line = line.replace(item, ' ')
    return line
