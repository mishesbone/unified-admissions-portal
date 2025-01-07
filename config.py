import os


class Config:
    """Base configuration class."""
    
    # Secret key for session management (keep this safe and change for production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    
    # Database configuration (change based on your database setup)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///site.db'  # Default to SQLite for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
    
    # CORS configuration
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Email configuration (if using Flask-Mail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Set through environment variables
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Set through environment variables
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@yourdomain.com'
    
    # Application-specific configuration (you can extend this as needed)
    ITEMS_PER_PAGE = 10  # Pagination setting for listing items
    
class DevelopmentConfig(Config):
    """Development configuration settings."""
    
    # Turn on debugging in development
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_site.db'

class TestingConfig(Config):
    """Testing configuration settings."""
    
    # Testing environment
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test_site.db'

class ProductionConfig(Config):
    """Production configuration settings."""
    
    # Production settings
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/dbname'
    # Can add additional security settings or production-specific configurations here
