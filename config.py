import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    DEBUG = False
    TESTING = False
    WEB3_PROVIDER = os.environ.get('WEB3_PROVIDER')

class DevelopmentConfig(Config):
    """Configuration for Development."""
    DEBUG = True
    FLASK_ENV = 'development'
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///dev.db'

class TestingConfig(Config):
    """Configuration for Testing."""
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///test.db'

class ProductionConfig(Config):
    """Configuration for Production."""
    FLASK_ENV = 'production'
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or 'sqlite:///prod.db'

config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}
