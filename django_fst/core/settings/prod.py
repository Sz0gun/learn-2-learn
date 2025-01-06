from .base import *  # Importuj wszystkie ustawienia z base.py

# Debugowanie wyłączone w środowisku produkcyjnym
DEBUG = False

# Lista dozwolonych hostów
ALLOWED_HOSTS = ['*.up.railway.app']

# Klucz tajny musi być ustawiony w środowisku produkcyjnym
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Konfiguracja bazy danych PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Pliki statyczne w produkcji
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Zabezpieczenia
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
