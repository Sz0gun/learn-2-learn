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

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app/

# Set the path for Google Cloud credentials (optional)
# This assumes the credentials will be passed as a GitHub Secret in GitHub Actions
ARG GOOGLE_APPLICATION_CREDENTIALS=/app/gcs_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}

# Expose the application port (for web apps)
EXPOSE 8000

# Command to run your application (replace with your app's run command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
