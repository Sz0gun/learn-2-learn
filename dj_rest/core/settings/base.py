# dj_rest/core/settings/base.py

from pathlib import Path
from shared.settings import config

# from rest_fabric_control.utils import validate_vault_connection

# # Check the connection with Vault
# vault_client = validate_vault_connection()

# # Download secrets
# secrets = vault_client.secrets.kv.v2.read_secret_version(path='learn-2-learn')

# SECRET_KEY = secrets['data']['data']['SECRET_KEY']

SECRET_KEY = config.DJANGO_SECRET_KEY
DEBUG = config.DJANGO_DEBUG
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ALLOWED_HOSTS = config.ALLOWED_HOSTS

INSTALLED_APPS = [
    'user_management',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_fabric_control',
]

AUTH_USER_MODEL = 'user_management.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = config.CORS_ALLOWED_ORIGINS

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

