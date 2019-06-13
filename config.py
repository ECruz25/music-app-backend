import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # dbname='{your_database}' user='edwin@music-app-ec-server' host='music-app-ec-server.postgres.database.azure.com’ password='{your_password}' port='5432' sslmode='true'
    SQLALCHEMY_DATABASE_URI = 'postgresql://edwin:Password123@music-app-ec-server/music_app_ec'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
