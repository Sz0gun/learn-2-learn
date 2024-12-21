import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module depending on the environment variable
django_env = os.getenv('DJANGO_ENV', 'prod').lower()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{django_env}')

application = get_wsgi_application()
