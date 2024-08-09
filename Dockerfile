FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Run the aplication with Gunicorn, binding to the correct port
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "project.wsgi"]

