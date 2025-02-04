# hccci/settings/development.py

from . import settings

# Override settings for development
DEBUG = True
ALLOWED_HOSTS = []

# Database configurations for local development (SQLite for dev)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
}