
# Learn-2-Learn API - Telegram Bot

## Project Overview

The **Learn-2-Learn** project has successfully configured key components such as **FastAPI**, **Redis**, and the deployment of the application in **Docker containers**. The project also integrates with **GitHub Container Registry (GHCR)** for managing container images. 

### Key Milestones:
- **FastAPI and Redis Integration**: FastAPI serves as the primary API framework for handling asynchronous requests, while Redis provides caching and session management.
- **Docker & CI/CD**: The application is containerized using Docker, and a CI/CD pipeline is established using GitHub Actions to automate testing and deployment processes.
- **GitHub Container Registry**: Integrated GHCR for efficient Docker image management and deployment.

### Current Objectives:
The next phase of development focuses on:
1. **Extending Application Functionality**: New features are planned for improved performance and expanded use cases.
2. **Integration with Vicuna Model**: AI model integration for advanced interactions.
3. **Kubernetes Deployment**: The system will be deployed on Kubernetes for better scalability and resource management.
4. **Background Task Optimization with Celery**: Celery will handle background tasks, improving efficiency and responsiveness.
5. **Monitoring and Analysis**: Tools such as Prometheus and Grafana will be introduced to monitor system performance and ensure reliability.

### Upcoming Features: 
- **Alleycat Event Bot**: A specialized bot is being developed to support the Alleycat event. The bot will manage user interactions, event details, and facilitate real-time communication and updates.

## Project Structure

```plaintext
learn-2-learn/
├── .github/             # GitHub Actions CI/CD workflows
├── fastapi_app/         # FastAPI application folder
├── telegram_bot/        # Telegram bot logic and handlers
├── Dockerfile           # Docker configuration for containerization
├── docker-compose.yml   # Docker Compose file to run the services
├── pyproject.toml       # Poetry configuration for managing dependencies
├── Redis/               # Redis cache setup
├── main.py              # Entry point for the application
└── README.md            # Project documentation (this file)
```

## How to Run

### Using Docker Compose:

To run the application locally using Docker Compose, execute the following commands:

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project folder
cd learn-2-learn

# Build and run the services (FastAPI, Redis, etc.)
docker-compose up --build
```

This will launch the FastAPI app, Redis, and other necessary services.

### Running Tests

Tests are included for various parts of the system. To run the tests:

```bash
# Using Poetry
poetry run pytest
```

## Environment Variables

Make sure to set the following environment variables in your `.env` file:

```plaintext
TELEGRAM_TOKEN=<your-telegram-bot-token>
POSTGRES_DB=<your-database>
POSTGRES_USER=<your-user>
POSTGRES_PASSWORD=<your-password>
```

## Future Plans

- **Kubernetes Deployment**: The system will be migrated to Kubernetes to enable scaling.
- **Monitoring**: Integration with Prometheus and Grafana for real-time monitoring and analytics.
- **Alleycat Bot Development**: The next stage involves building a bot to manage the Alleycat event, ensuring smooth operation and interaction with participants.

## Contributing

Feel free to contribute to this project by submitting pull requests or reporting issues.

## License

This project is licensed under the MIT License.
