# dj_rest/core/settings/prod.py
from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.PSQL_DB_PROD,
        'USER': config.PSQL_USER_PROD,
        'PASSWORD': config.PSQL_PASSWORD_PROD,
        'HOST': config.PSQL_HOST_PROD,
        'PORT': config.PSQL_PORT_PROD,
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
