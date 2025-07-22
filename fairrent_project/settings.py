# fairrent_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv # For environment variables
import dj_database_url # New import for PostgreSQL

# Load environment variables from .env file (if it exists)
# This should be at the very top to ensure env vars are loaded before used.
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings - crucial for production
# Load SECRET_KEY from environment variable for production
# DO NOT hardcode your SECRET_KEY in production.
# Render will provide DJANGO_SECRET_KEY as an environment variable.
# FOR THIS PUSH, WE ARE REMOVING THE DEFAULT VALUE TO AVOID ANY SECRET SCANNING ISSUES.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True' # Load DEBUG from env, default to False

ALLOWED_HOSTS = ['.onrender.com', 'roomto.live', 'www.roomto.live'] # Add your production domain(s) when deployed
# If you also want to access via IP for some reason:
# ALLOWED_HOSTS += os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic', # Removed for production. WhiteNoise middleware is enough.
    'django.contrib.staticfiles',
    'django.contrib.humanize', # Optional: for human-readable formatting

    # Third-party apps
    'crispy_forms', # For better form rendering
    'storages', # Added for S3 storage for media files

    # Your app
    'fairrent_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise middleware should be placed here, right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fairrent_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'fairrent_app.context_processors.site_settings', # Uncomment if you have this custom context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'fairrent_project.wsgi.application'

# Database
# Use dj_database_url to parse the DATABASE_URL environment variable
# Render provides DATABASE_URL automatically for PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # For production
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configure WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (user uploaded content) - Recommended for persistent storage on Render
# Install django-storages and boto3 if you use this:
# pip install django-storages boto3
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 settings for media files (Optional but highly recommended for production)
# Make sure to set these environment variables on Render
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME') # e.g., 'us-east-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read' # Be careful with this, consider 'private' and serving via signed URLs
AWS_S3_VERIFY = True # Ensure SSL verification
AWS_QUERYSTRING_AUTH = False # Avoid query parameters in URLs

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    # MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/' # This would serve media directly from S3

ALLOWED_HOSTS = ['.onrender.com', 'roomto.live', 'www.roomto.live']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings (aligned with fairrent_app urls.py)
LOGIN_REDIRECT_URL = 'fairrent_app:profile'
LOGOUT_REDIRECT_URL = 'fairrent_app:index'
LOGIN_URL = 'fairrent_app:login'

# Email settings (for password reset)
# For production, ensure these are loaded from environment variables
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost') # Your sender email


# Security settings for production (only active when DEBUG is False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    # Add this for Render: Render acts as a proxy, so Django needs to know it's behind SSL
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # <--- ADD THIS LINE
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
    # Recommended for production to prevent exposing your internal IP
    # ALLOWED_HOSTS = ['yourproject.onrender.com', 'roomto.live', 'www.roomto.live']


# API Keys (loaded strictly from environment variables)
# You MUST set these as environment variables on Render.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# Django Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4' # If using Bootstrap

# Custom user model (if you have one)
# AUTH_USER_MODEL = 'fairrent_app.CustomUser'

# Session settings
SESSION_COOKIE_AGE = 1209600 # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True

# Cache settings (for production, using LocMemCache for development)
# For Render, consider using Redis for production caching via a Render Redis service
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fairrent-connect-cache', # Unique name for the cache
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple', # Use simple formatter for console
        },
        # You can add file handlers for production logging
        # Render's logging typically goes to console, which is then captured by Render's logs.
        # 'file': {
        #    'class': 'logging.handlers.RotatingFileHandler',
        #    'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        #    'maxBytes': 1024 * 1024 * 5, # 5 MB
        #    'backupCount': 5,
        #    'formatter': 'verbose',
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO', # Log INFO level and above for Django
            'propagate': False,
        },
        'fairrent_app': { # Logger for your specific app
            'handlers': ['console'],
            'level': 'DEBUG', # Log DEBUG level and above for your app
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING', # Default level for any other loggers
    },
}
