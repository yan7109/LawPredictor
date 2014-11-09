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
