import re


def convert_fields_to_selectors(selectors, fields):
    """
    Selectors need to convert camel-case names into '-' separated,
    lower-case values.
    """
    for attr in dir(fields):
        if '__' != attr[:2]:
            setattr(selectors, attr, re.sub(
                r'([A-Z])', '-\\1', getattr(fields, attr)).lower())
#            print getattr(selectors, attr)


class BasicProfileFields(object):
    """
    Fields that might be returned by r_basicprofile permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    API_STANDARD_PROFILE_REQUEST_HEADERS = \
        'apiStandardProfileRequest:(headers)'
    API_STANDARD_PROFILE_REQUEST_URL = 'apiStandardProfileRequest:(url)'
    CURRENT_SHARE = 'currentShare'
    DISTANCE = 'distance'
    FORMATTED_NAME = 'formattedName'
    FORMATTED_PHONETIC_NAME = 'formattedPhoneticName'
    FIRST_NAME = 'firstName'
    HEADLINE = 'headline'
    ID = 'id'
    INDUSTRY = 'industry'
    LAST_NAME = 'lastName'
    LOCATION = 'location'
    LOCATION_COUNTRY = 'location:(country:(code))'
    LOCATION_NAME = 'location:(name)'
    MAIDEN_NAME = 'maidenName'
    MAIN_ADDRESS = 'mainAddress'
    NUM_CONNECTIONS = 'numConnections'
    NUM_CONNECTIONS_CAPPED = 'numConnectionsCapped'
    PHONETIC_FIRST_NAME = 'phoneticFirstName'
    PHONETIC_LAST_NAME = 'phoneticLastName'
    PICTURE_URL = 'pictureUrl'
    POSITION = 'positions'
    PROFILE_URL = 'profileUrl'
    PROVIDER_ACCOUNT_ID = 'providerAccountId'
    PROVIDER_ACCOUNT_NAME = 'providerAccountName'
    PUBLIC_PROFILE_URL = 'publicProfileUrl'
    RELATION_TO_VIEWER = 'relationToViewer:(distance)'
    SITE_STANDARD_PROFILE_REQUEST = 'siteStandardProfileRequest'
    SPECIALTIES = 'specialties'
    SUMMARY = 'summary'
    TWITTER_ACCOUNTS = 'twitterAccounts'


class BasicProfileSelectors(object):
    """
    The selectors to fetch BasicProfileFields.
    """
    pass
convert_fields_to_selectors(BasicProfileSelectors, BasicProfileFields)


class BoundAccountTypeFields(object):
    """
    Individual certifications are structured objects returned as part
    of contact info.
    https://developer.linkedin.com/documents/profile-fields
    """
    ACCOUNT_TYPE = 'accountType'
    BINDING_STATUS = 'bindingStatus'
    IS_PRIMARY = 'isPrimary'
    PROVIDER_ACCOUNT_ID = 'providerAccountId'
    PROVIDER_ACCOUNT_NAME = 'providerAccountName'


class CertificationFields(object):
    """
    Individual certifications are structured objects returned as part
    of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    AUTHORITY_NAME = 'authority:(name)'
    END_DATE = 'endDate'
    ID = 'id'
    NAME = 'name'
    NUMBER = 'number'
    START_DATE = 'startDate'


class CompanyFields(object):
    """
    Company is a structured object returned as part of profile.
    Not used directly with people calls, but used in position calls.
    https://developer.linkedin.com/documents/profile-fields
    """
    ID = 'id'
    INDUSTRY = 'industry'
    NAME = 'name'
    SIZE = 'size'
    TICKER = 'ticker'
    TYPE = 'type'


class ConnectionFields(object):
    """
    Fields that might be returned by r_network permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    CONNECTIONS = 'connections'  # {'total': #}


class ConnectionSelectors(object):
    """
    The selectors to fetch ConnectionFields.
    """
    pass
convert_fields_to_selectors(ConnectionSelectors, ConnectionFields)


class ContactInfoFields(object):
    """
    Fields that might be returned by r_contactinfo permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    BOUND_ACCOUNT_TYPES = 'boundAccountTypes'
    IM_ACCOUNTS = 'imAccounts'
    MAIN_ADDRESS = 'mainAddress'
    PHONE_NUMBERS = 'phoneNumbers'
    PRIMARY_TWITTER_ACCOUNT = 'primaryTwitterAccount'
    TWITTER_ACCOUNTS = 'twitterAccounts'


class ContactInfoSelectors(object):
    """
    The selectors to fetch ContactInfoFields.
    """
    pass
convert_fields_to_selectors(ContactInfoSelectors, ContactInfoFields)


class CourseFields(object):
    """
    Individual courses are structured objects returned as part
    of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    ID = 'id'
    NAME = 'name'
    NUMBER = 'number'


class EmailFields(object):
    """
    Fields that might be returned by r_emailaddress permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: You must be using the new permissions dialog for this permission
        to work.
    """
    EMAIL_ADDRESS = 'emailAddress'


class EmailSelectors(object):
    """
    The selectors to fetch EmailFields.
    """
    pass
convert_fields_to_selectors(EmailSelectors, EmailFields)


class EducationFields(object):
    """
    Individual educations are structured objects returned as part
    of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    ACTIVITIES = 'activities'
    DEGREE = 'degree'
    END_DATE = 'endDate'
    FIELD_OF_STUDY = 'fieldOfStudy'
    ID = 'id'
    NOTES = 'notes'
    SCHOOL_NAME = 'schoolName'
    START_DATE = 'startDate'


class FullProfileFields(object):
    """
    Fields that might be returned by r_fullprofile permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    ASSOCIATIONS = 'associations'
    COURSES = 'courses'
    CERTIFICATIONS = 'certifications'
    DATE_OF_BIRTH = 'dateOfBirth'
    EDUCATIONS = 'educations'
    FOLLOWING = 'following'
    HONORS = 'honors'
    INTERESTS = 'interests'
    JOB_BOOKMARKS = 'jobBookmarks'
    LAST_MODIFIED_TIMESTAMP = 'lastModifiedTimestamp'
    LANGUAGES = 'languages'
    MEMBER_URL_RESOURCES = 'memberUrlResources'  # [{'url': '', 'name': ''}]
    MFEED_RSS_URL = 'mfeedRssUrl'
    NUM_RECOMMENDERS = 'numRecommenders'
    PATENTS = 'patents'
    PROPOSAL_COMMENTS = 'proposalComments'
    PUBLICATIONS = 'publications'
    RECOMMENDATIONS_RECEIVED = 'recommendationsReceived'
    RELATED_PROFILE_VIEWS = 'relatedProfileViews'
    SKILLS = 'skills'
    SUGGESTIONS = 'suggestions'
    THREE_CURRENT_POSITIONS = 'threeCurrentPositions'
    THREE_PAST_POSITIONS = 'threePastPositions'
    VOLUNTEER = 'volunteer'


class FullProfileSelectors(object):
    """
    The selectors to fetch FullProfileFields.
    """
    pass
convert_fields_to_selectors(FullProfileSelectors, FullProfileFields)


class GroupMembershipFields(object):
    """
    Fields that might be returned by rw_groups permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    GROUP_MEMBERSHIPS = 'groupMemberships'


class LanguagesFields(object):
    """
    Individual languages are structured objects returned as part of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    ID = 'id'
    LANGUAGE_NAME = 'language:(name)'
    PROFICIENCY_LEVEL = 'proficiency:(level)'
    PROFICIENCY_NAME = 'proficiency:(name)'


class NetworkUpdateFields(object):
    """
    Fields that might be returned by rw_nus permission.
    https://developer.linkedin.com/documents/profile-fields
    Note: Most of these fields are available with a legacy API key.
    """
    NETWORK = 'network'


class NetworkUpdateSelectors(object):
    """
    The selectors to fetch NetworkUpdateFields.
    """
    pass
convert_fields_to_selectors(NetworkUpdateSelectors, NetworkUpdateFields)


class PatentsFields(object):
    """
    Individual patents are structured objects returned as part of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    DATE = 'date'
    ID = 'id'
    OFFICE_NAME = 'office:(name)'
    INVENTORS_ID = 'inventors:(id)'
    INVENTORS_NAME = 'inventors:(name)'
    INVENTORS_PERSON = 'inventors:(person)'
    STATUS_ID = 'status:(id)'
    STATUS_NAME = 'status:(name)'
    SUMMARY = 'summary'
    TITLE = 'title'
    URL = 'url'


class PositionFields(object):
    """
    Positions are structured objects returned as part of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    COMPANY = 'company'
    END_DATE = 'endDate'
    ID = 'id'
    IS_CURRENT = 'isCurrent'
    START_DATE = 'startDate'
    SUMMARY = 'summary'
    TITLE = 'title'


class PublicationFields(object):
    """
    Individual publications are structured objects returned as part of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    AUTHORS_ID = 'authors:(id)'
    AUTHORS_NAME = 'authors:(name)'
    AUTHORS_PERSON = 'authors:(person)'
    DATE = 'date'
    ID = 'id'
    PUBLISHER_NAME = 'publisher:(name)'
    SUMMARY = 'summary'
    TITLE = 'title'
    URL = 'url'


class RecommendationFields(object):
    """
    Individual recommendations are structured objects returned as part
    of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    ID = 'id'
    RECOMMENDATION_TEXT = 'recommendation-text'
    RECOMMENDATION_TYPE = 'recommendation-type'
    RECOMMENDER = 'recommender'


class SkillsFields(object):
    """
    Individual skills are structured objects returned as part of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    ID = 'id'
    PROFICIENCY_LEVEL = 'proficiency:(level)'
    PROFICIENCY_NAME = 'proficiency:(name)'
    SKILL_NAME = 'skill:(name)'
    YEARS_ID = 'years:(id)'
    YEARS_NAME = 'years:(name)'


class VolunteerExperienceFields(object):
    """
    Individual volunteer experiences are structured objects returned as part
    of profile.
    https://developer.linkedin.com/documents/profile-fields
    """
    CAUSE_NAME = 'cause:(name)'
    ID = 'id'
    ORGANIZATION_NAME = 'organization:(name)'
    ROLE = 'role'


class LinkedInScope(object):
    """
    Permission scopes. You will need an updated API key or these will
    be ignored.
    """
    BASIC_PROFILE = 'r_basicprofile'
    CONTACT_INFO = 'r_contactinfo'
    CONNECTIONS = 'r_network'
    EMAIL_ADDRESS = 'r_emailaddress'
    FULL_PROFILE = 'r_fullprofile'
    GROUPS = 'rw_groups'
    MESSAGES = 'w_messages'
    NETWORK_UPDATES = 'rw_nus'