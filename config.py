import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'din-hemmelige-nøkkel-her'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/sample_tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test_tasks.db'

class ProductionConfig(Config):
    pass