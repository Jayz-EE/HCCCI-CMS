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

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = None  

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
