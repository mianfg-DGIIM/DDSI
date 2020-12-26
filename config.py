import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_USER   = 'postgres'
POSTGRES_PW     = 'postgres'
POSTGRES_URL    = 'localhost'
POSTGRES_DB     = 'pharmagiim'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '83IO4HG1O5GH245H158H134G384TGH'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB) # os.environ['SQLALCHEMY_DATABASE_URI']
    SESSION_COOKIE_SECURE = False

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
