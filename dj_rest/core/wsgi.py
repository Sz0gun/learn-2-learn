import os
from django.core.wsgi import get_wsgi_application

# Default to production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')

# Dynamically adjust based on an environment variable
django_env = os.getenv('DJANGO_ENV', 'prod').lower()
if django_env == 'dev':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.dev'

application = get_wsgi_application()
