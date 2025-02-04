import os
from django.core.wsgi import get_wsgi_application

# Use production settings in production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hccci.settings.production')

application = get_wsgi_application()
