import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_NAME = os.getenv('DB_NAME', 'biblioteca')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))

    # URL base
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')

    # Seguridad
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB_NAME = 'biblioteca_test'

# Seleccionar configuración según ambiente
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
if ENVIRONMENT == 'production':
    config = ProductionConfig
elif ENVIRONMENT == 'testing':
    config = TestingConfig
else:
    config = DevelopmentConfig

# Exports backwards compatibility
HOST = config.DB_HOST
USER = config.DB_USER
PASS = config.DB_PASS
DB = config.DB_NAME
DB_PORT = config.DB_PORT
BASE_URL = config.BASE_URL
SECRET_KEY = config.SECRET_KEY
