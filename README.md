Oto zaktualizowana treść pliku `README.md` dla projektu `bot-api-1`:

---

# Bot API - Telegram Bot API

## Opis projektu

Bot API to aplikacja Django, która umożliwia obsługę bota Telegrama. Projekt jest zintegrowany z usługą Heroku, gdzie jest hostowany oraz przetwarza dane za pomocą webhooków.

## Spis treści

- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Konfiguracja lokalna](#konfiguracja-lokalna)
- [Konfiguracja na Heroku](#konfiguracja-na-heroku)
- [Wdrożenie na Heroku](#wdrożenie-na-heroku)
- [Użytkowanie](#użytkowanie)
- [Testowanie](#testowanie)
- [Dodatkowe informacje](#dodatkowe-informacje)

## Wymagania

- Python 3.12
- Django 4.2
- Heroku CLI
- PostgreSQL (lokalnie lub na Heroku)

## Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/your-username/telegram-bot-api.git
   cd telegram-bot-api
   ```

2. Utwórz i aktywuj wirtualne środowisko:

   ```bash
   python3 -m venv botenv
   source botenv/bin/activate
   ```

3. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

4. Utwórz plik `.env` na podstawie pliku `.env.example` i dodaj klucz `SECRET_KEY`.

## Konfiguracja lokalna

1. Skonfiguruj lokalną bazę danych PostgreSQL:

   W pliku `project/settings.py`, skonfiguruj lokalną bazę danych PostgreSQL:

   ```python
   if 'DATABASE_URL' in os.environ:
       DATABASES = {
           'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
       }
   else:
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': 'your_local_db_name',
               'USER': 'your_local_db_user',
               'PASSWORD': 'your_local_db_password',
               'HOST': 'localhost',
               'PORT': '5432',
           }
       }
   ```

2. Uruchom migracje:

   ```bash
   python manage.py migrate
   ```

3. Uruchom lokalny serwer:

   ```bash
   python manage.py runserver
   ```

## Konfiguracja na Heroku

1. Zaloguj się do Heroku:

   ```bash
   heroku login
   ```

2. Utwórz nową aplikację na Heroku:

   ```bash
   heroku create your-app-name
   ```

3. Skonfiguruj zmienne środowiskowe:

   W zakładce **Settings** na Heroku dodaj następujące zmienne środowiskowe:

   - `SECRET_KEY`: Twój klucz tajny Django
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `['.herokuapp.com']`
   - `DATABASE_URL`: automatycznie konfigurowane przez Heroku przy dodaniu dodatku Postgres

4. Skonfiguruj buildpacki:

   Upewnij się, że buildpacki są prawidłowo ustawione:

   ```bash
   heroku buildpacks:set heroku/python
   ```

## Wdrożenie na Heroku

1. Dodaj zmiany do repozytorium:

   ```bash
   git add .
   git commit -m "Wdrożenie na Heroku"
   ```

2. Wypchnij zmiany na Heroku:

   ```bash
   git push heroku main
   ```

3. Wykonaj migracje na Heroku:

   ```bash
   heroku run python manage.py migrate
   ```

4. Utwórz superużytkownika dla panelu admina:

   ```bash
   heroku run python manage.py createsuperuser
   ```

## Użytkowanie

1. Wejdź na stronę swojego bota na Heroku, aby go przetestować.
2. Skonfiguruj webhooki dla bota Telegrama:

   ```bash
   curl -F "url=https://your-heroku-app.herokuapp.com/telegram/webhook/" https://api.telegram.org/bot<YourBOTToken>/setWebhook
   ```

## Testowanie

1. Sprawdź logi aplikacji na Heroku:

   ```bash
   heroku logs --tail
   ```

2. Testuj lokalnie za pomocą narzędzi takich jak `ngrok` lub `localtunnel`.

## Dodatkowe informacje

- Aplikacja korzysta z frameworka Django do obsługi bota Telegrama.
- W aplikacji używane są technologie takie jak Docker i Gunicorn.
- Dla lepszej optymalizacji zaleca się przeanalizowanie konfiguracji `Procfile` oraz plików statycznych.

---

Tę treść można dodać do pliku `README.md` w projekcie `bot-api-1`.