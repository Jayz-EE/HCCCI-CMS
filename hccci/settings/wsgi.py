import os
from django.core.wsgi import get_wsgi_application

# Use the correct settings module for development or production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hccci.settings.development')

application = get_wsgi_application()