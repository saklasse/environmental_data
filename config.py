
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SUPPORTED_LANGUAGES = {'no': 'Norwegian', 'en': 'English'}
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    
class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True    