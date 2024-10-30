FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install poetry
RUN poetry install
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0.:8000"]