# backend/app/config.py
import os

class Config:
    """Base configuration."""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Fix the path to point to the data directory in your project structure
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Database configuration
    AC_DB_URI = os.environ.get('AC_DB_CONNECTION_STRING', 
                              f"sqlite:///{os.path.join(DATA_DIR, 'ac_data.db')}")
    GSE_DB_URI = os.environ.get('GSE_DB_CONNECTION_STRING', 
                               f"sqlite:///{os.path.join(DATA_DIR, 'gse_data.db')}")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Use in-memory databases for faster testing
    AC_DB_URI = "sqlite:///:memory:"
    GSE_DB_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DEVELOPMENT = False
    # In production, prioritize environment variables
    AC_DB_URI = os.environ.get('AC_DB_CONNECTION_STRING', 
                              f"sqlite:///{os.path.join(Config.DATA_DIR, 'ac_data.db')}")
    GSE_DB_URI = os.environ.get('GSE_DB_CONNECTION_STRING', 
                               f"sqlite:///{os.path.join(Config.DATA_DIR, 'gse_data.db')}")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}