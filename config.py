# Configuration settings for the Flask app
class Config(object):
    Testing = False
    DEBUG = False

class DevelopmentConfig(Config):
    ENV = "develoment"
    DEBUG = True

class TestingConfig(Config):
    ENV = "testing"
    DEBUG = True
