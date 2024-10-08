# Use an official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-root

# Now copy the rest of your application code into the container
COPY . /app/

# Expose the application port (for FastAPI)
EXPOSE 8000

# Command to run your FastAPI application
CMD ["poetry", "run", "uvicorn", "fapi_main:app", "--host", "0.0.0.0", "--port", "8000"]
