import os
from pathlib import Path

# Ścieżka do katalogu głównego projektu
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Klucz tajny (upewnij się, że ten klucz jest przechowywany w zmiennej środowiskowej w produkcji)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')

# Debugowanie (domyślnie wyłączone, wymaga ręcznego ustawienia dla developmentu)
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# Domyślne dozwolone hosty
ALLOWED_HOSTS = []

# Aplikacje Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Twoje aplikacje
    'rest_framework',
    'rest_fabric_control',
    'user_manager',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Główny adres URL
ROOT_URLCONF = 'core.urls'

# Szablony
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
            ],
        },
    },
]

# Silnik WSGI
WSGI_APPLICATION = 'core.wsgi.application'

# Baza danych (domyślna SQLite dla developmentu)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Walidacja haseł
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

# Międzynarodowość
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Pliki statyczne
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
