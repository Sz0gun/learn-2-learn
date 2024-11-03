# Use Python image for backend
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the app's code
COPY . /app

# Run the FastAPI app
CMD ["uvicorn", "webenv.main:app", "--host", "0.0.0.0", "--port", "8000"]
