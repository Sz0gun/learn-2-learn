FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /project

# pliki zależności z instalacja
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały projekt do katalogu roboczego
COPY . .

# zmienna środowiskową dla portu na którym działa Django
ENV PORT=8080

# port, który zostanie użyty w Cloud Run
EXPOSE 8080

# Uruchomienie aplikacji Django
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT project.wsgi:application"]
