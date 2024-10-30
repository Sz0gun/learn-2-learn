FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the entire application to the working directory
COPY . /app

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "chess_board:app", "--host", "0.0.0.0", "--port", "8000"]
