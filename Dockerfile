# Use an official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry==1.3.1

# Install dependencies using Poetry, excluding optional dependencies
RUN poetry install --no-root --only

# Copy the rest of your application code into the container
COPY . /app/

# Expose the application port (for web apps)
EXPOSE 8000

# Command to run your application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
