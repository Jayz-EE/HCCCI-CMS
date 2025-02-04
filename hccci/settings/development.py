# development.py

from .settings import *
import environ

# Override settings specific to development
DEBUG = True
ALLOWED_HOSTS = ['*']  # For local development, allow all hosts

env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': env.db(), 
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR  

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
