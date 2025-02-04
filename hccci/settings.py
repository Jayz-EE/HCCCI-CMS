"""
Django settings for hccci project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lj6)ij9zd-vmkvubd5j)l4clh3^pb-^jrbd^(=*x4jeon*s2-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Confirm that you're using Django CMS version 4
CMS_CONFIRM_VERSION4 = True

SITE_ID = 1

# Language and locale settings
LANGUAGE_CODE = 'en-us'

# List of languages supported by the CMS, including 'en-us'
LANGUAGES = [
    ('en-us', 'English (US)'),  # Use 'en-us' explicitly
]

# CMS-specific language configuration
CMS_LANGUAGES = {
    1: [  # Replace '1' with your site ID if different
        {
            'code': 'en-us',
            'name': 'English (US)',
            'fallbacks': ['en'],  # Fallback to 'en' if needed
            'hide_untranslated': False,  # Show untranslated content
        },
    ],
    'default': {
        'fallbacks': ['en'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #created APPS
    'website',

    #cors 
     'corsheaders',

]

MIDDLEWARE = [
    #cors 
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hccci.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Add the sekizai context processor here
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'hccci.wsgi.application'

CMS_TEMPLATES = [
    ('base.html', 'Default Template'),
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    parsed_db_url = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': parsed_db_url.path[1:],  # remove the leading '/'
            'USER': parsed_db_url.username,
            'PASSWORD': parsed_db_url.password,
            'HOST': parsed_db_url.hostname,
            'PORT': parsed_db_url.port,
        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hcccicms',  
#         'USER': 'hcccicms',  
#         'PASSWORD': '!Manila12#',  
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'cms_hccci',
#         'USER': 'postgres',  
#         'PASSWORD': '@Classify24#',  
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow all domains to make requests
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://172.16.0.61:8001",
    "http://127.0.0.1:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://172.16.0.61:8001",
    "http://127.0.0.1:8000",
    "http://testweb.hccci.edu.ph",
    "https://testweb.hccci.edu.ph",
]

CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = 'website.CustomUser'

LOGIN_URL = '/cms/login/'

SESSION_COOKIE_AGE = 7200  # Session will expire after 2 hours (7200 seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expires when the browser is closed

