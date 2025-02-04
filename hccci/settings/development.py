# development.py

from .settings import *

# Override settings specific to development
DEBUG = True
ALLOWED_HOSTS = ['*']  # For local development, allow all hosts

# Database settings for development (local PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hccci_dev',
        'USER': 'devuser',
        'PASSWORD': 'devpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files setup for development
STATIC_URL = '/static/'

# Any other settings you wish to customize for development
