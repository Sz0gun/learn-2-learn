# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the application code into the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server using uvicorn
CMD ["uvicorn", "chess_board", "--host", "0.0.0.0", "--port", "8000"]
