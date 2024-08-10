# Telegram Bot API

## Opis
Aplikacja do obsługi bota Telegram, która integruje się z dwoma modelami AI. Umożliwia przechowywanie danych konwersacyjnych oraz analizę odpowiedzi.

## Struktura Repozytorium
- `api/`: Aplikacja Django do obsługi API.
- `project/`: Główna konfiguracja projektu Django.
- `templates/`: Szablony HTML używane w projekcie.

## Uruchamianie
1. Skonfiguruj swoje środowisko:
   ```bash
   pip install -r requirements.txt


Oto zaktualizowana wersja pliku `README.md`, z usuniętymi danymi dotyczącymi konfiguracji lokalnej bazy danych:

---

# Bot-API - Telegram Bot API

## Opis projektu

Bot-API to aplikacja oparta na frameworku Django, która integruje się z API Telegrama, umożliwiając tworzenie i zarządzanie chatbotami. Aplikacja jest zaprojektowana do działania w środowisku produkcyjnym na Heroku.

## Struktura projektu

```
telegram-bot-api/
│
├── telegram_bot/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
│
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
│
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── index.html
│
├── .gitignore
├── .dockerignore
├── Dockerfile
├── Procfile
├── README.md
├── manage.py
└── requirements.txt
```

## Wymagania

- Python 3.9 lub nowszy
- Django 3.x lub nowszy
- PostgreSQL (w środowisku Heroku)
- Heroku CLI (jeśli wdrażasz na Heroku)
- Docker (opcjonalnie, jeśli chcesz używać kontenerów)

## Instalacja

### 1. Klonowanie repozytorium

Klonuj repozytorium z GitHub:

```bash
git clone https://github.com/username/telegram-bot-api.git
cd telegram-bot-api
```

### 2. Konfiguracja środowiska wirtualnego

Stwórz i aktywuj środowisko wirtualne:

```bash
python3 -m venv botenv
source botenv/bin/activate
```

Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

### 3. Migracje bazy danych

Przeprowadź migracje, aby utworzyć struktury tabel w bazie danych:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Uruchomienie aplikacji lokalnie

Uruchom serwer deweloperski Django:

```bash
python manage.py runserver
```

Aplikacja powinna być dostępna pod adresem `http://127.0.0.1:8000/`.

## Wdrożenie na Heroku

### 1. Utworzenie aplikacji na Heroku

Jeśli jeszcze tego nie zrobiłeś, utwórz aplikację na Heroku:

```bash
heroku create bot-api
```

### 2. Konfiguracja środowiska na Heroku

Skonfiguruj zmienne środowiskowe na Heroku:

```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='.herokuapp.com'
heroku config:set DATABASE_URL='your-database-url'
```

### 3. Wypchnięcie kodu na Heroku

Upewnij się, że wszystkie zmiany są zsynchronizowane z repozytorium GitHub, a następnie wypchnij kod na Heroku:

```bash
git push heroku main
```

### 4. Migracje na Heroku

Po wdrożeniu, przeprowadź migracje bazy danych na Heroku:

```bash
heroku run python manage.py migrate
```

### 5. Uruchomienie aplikacji na Heroku

Otwórz aplikację w przeglądarce:

```bash
heroku open
```

## Dodatkowe informacje

### Webhooki

Jeśli korzystasz z webhooków Telegrama, upewnij się, że są one poprawnie skonfigurowane i przetestowane. Możesz użyć narzędzi takich jak `ngrok`, aby tunelować lokalny serwer i testować webhooki przed wdrożeniem na produkcję.

### Konfiguracja bezpieczeństwa

W produkcji ważne jest, aby dodatkowo zabezpieczyć aplikację:
- Włącz SSL na serwerze (Heroku domyślnie korzysta z SSL).
- Sprawdź ustawienia bezpieczeństwa w `settings.py`.

### Pliki statyczne i media

Heroku domyślnie obsługuje pliki statyczne za pomocą Whitenoise. Upewnij się, że wszystkie pliki są prawidłowo serwowane.

## Problemy i wsparcie

Jeśli napotkasz problemy, sprawdź logi Heroku:

```bash
heroku logs --tail
```

W przypadku pytań lub problemów, możesz otworzyć zgłoszenie w repozytorium GitHub lub skontaktować się z autorem.

---

Plik `README.md` zawiera teraz wszystkie istotne informacje na temat konfiguracji, wdrożenia i użytkowania aplikacji `bot-api` bez odniesienia do lokalnej konfiguracji bazy danych. Jeśli będziesz potrzebował więcej informacji, jestem do dyspozycji!