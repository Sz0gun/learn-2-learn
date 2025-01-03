# Learn-2-Learn (L2L)

## Overview
Learn-2-Learn is a modular, scalable platform designed to facilitate collaborative learning through tools like real-time discussions, shared AI-generated resources, and personalized learning paths powered by AI-driven assistance. The project integrates FastAPI, Django, Telethon, and modern AI tools like OpenAI models to create a seamless, interactive experience.

The goal is to create an AI-driven Telegram bot capable of understanding GIF files, extracting text when needed, and working in reverse to generate images with animated text or additional effects. This bot will primarily focus on producing social media content. Building on this foundation, the project emphasizes data storage and transmission security, with special attention to encryption and peer-to-peer communication. All components are designed to function asynchronously, integrating the speed of FastAPI with Django's robust data management capabilities.

An additional consideration involves separating the domains for FastAPI (to support Telegram Web Apps and future features) and Django REST ORM (for data management). Communication and asynchronous data transfer between these frameworks will be handled via Telegram bots.

Upon mastering the integration of these tools, the project will focus on advancing data processing and AI model training to discover practical, innovative solutions powered by AI.

## Features

- **User Management**: Custom Django user model with advanced fields like `telegram_id` and `telegram_username`.
- **Vault Integration**: Secure storage for sensitive data using HashiCorp Vault.
- **Elasticsearch Logging**: Centralized logging for enhanced traceability and debugging.
- **Telegram Bot Integration**: Manage user interactions and commands through a Telegram bot.
- **WebSocket Communication**: Real-time communication between Telegram and the backend.
- **Image Generation**: Generate AI-driven images using OpenAI API.
- **Extensibility**: Modular architecture for easy addition of new features.
- **Multi-database Support**: Integration with PostgreSQL, Redis, CouchDB, and PouchDB for optimized data handling.
- **Asynchronous Processing**: Built-in support for async operations, improving performance.
- **Dynamic Configuration**: Environment-based settings for development and production.

## Tech Stack

- **Backend**: Django, FastAPI
- **Frontend**: HTML5 (future integration with Telegram Web Apps planned) | Nginx with Apache
- **Database**: PostgreSQL, CouchDB (future)
- **Tools**: Vault, Elasticsearch, Redis, Docker Engine
- **Languages**: Python

## Project Structure

```
learn-2-learn/
├── dj_rest/                  # Django backend
│   ├── core/                 # Core app for project settings, environment configurations, and utilities.
│   ├── rest_fabric_control/  # Handles integration with Vault and Elasticsearch for secure data management and centralized logging.
│   ├── user_management/      # Custom user model and management features, including Telegram-related fields.
│   └── manage.py             # Entry point for Django's management commands.
├── tg/                       # Contains Telegram bot logic, including handlers for user interactions and commands.
├── fa/                       # FastAPI modules for additional microservices or APIs to extend functionality.
├── shared/                   # Stores shared configurations, constants, and reusable utilities used across apps.
├── Dockerfile                # Defines the containerized setup for the project.
├── run_django.sh             # A script to initialize Django, Vault, and Elasticsearch for development.
└── requirements.txt          # Specifies Python dependencies for the project.
```

## Installation

### Prerequisites

- Python 3.10+
- HashiCorp Vault
- Elasticsearch
- Telegram API Hash and Bot token

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Sz0gun/learn-2-learn.git
   cd learn-2-learn
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file based on the provided `example.env`.
   - Ensure variables like `DJANGO_SECRET_KEY`, `VAULT_TOKEN`, and `POSTGRES_*` are properly set.

4. Apply migrations:
   ```bash
   python dj_rest/manage.py makemigrations user_management
   python dj_rest/manage.py makemigrations
   python dj_rest/manage.py migrate user_management
   python dj_rest/manage.py migrate
   ```

5. Run the development server:
   Before running the server, ensure the `DJANGO_ENV` variable is set to either `prod` or `dev`:
   ```bash
   export DJANGO_ENV=dev  # or 'prod' depending on your environment
   ./run_django.sh
   ```

   After the server starts successfully:
   - You should see logs indicating the server is running, such as `Starting development server at http://127.0.0.1:8000/`.
   - Open your browser and navigate to `http://127.0.0.1:8000/admin` to access the admin panel.
   - To verify Vault is running, check its logs in the terminal or visit the Vault API health endpoint:
     ```bash
     curl http://127.0.0.1:8200/v1/sys/health
     ```
     Expected output includes `"sealed":false`, indicating Vault is unsealed and operational.
   - To verify Elasticsearch, visit its status endpoint in your browser:
     ```
     http://localhost:9200
     ```
     You should see a JSON response with cluster details and `"status":"green"`.

6. Start Vault and Elasticsearch using `run_django.sh`:
   The `run_django.sh` script automatically starts Vault in development mode and Elasticsearch if required.

7. (Optional) Configure additional services for advanced logging or external integrations.

## Config

- Access the Django Admin panel at `http://127.0.0.1:8000/admin`.
  - First, set the superuser account by running:
    ```bash
    python dj_rest/manage.py createsuperuser
    ```
  - Log in to the admin panel and set up your Vault keys under the `VaultKey` model.
- Use the Telegram bot for user interaction and management.

## Usage

### Telegram Bot
- Send `/menu` to the bot to access the main menu.
- Use buttons for actions like image generation and AI-assisted chat.

### Development
- Add new features by extending the `tg`, `fa`, or `dj_rest` modules:
  - **tg (Telegram)**: Add custom handlers for Telegram bot commands and actions. For example, you can create a new handler to process custom user inputs:
    ```python
    from telethon import events

    @bot.on(events.NewMessage(pattern='/custom'))
    async def custom_handler(event):
        await event.reply('This is a custom Telegram bot command!')
    ```
  - **fa (FastAPI)**: Add new routes or services in the `fa` module. For example, create an endpoint to fetch user data:
    ```python
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/user/{user_id}")
    async def get_user(user_id: int):
        return {"user_id": user_id, "status": "active"}
    ```
  - **dj_rest**: Add new models, views, or utilities to extend Django's functionality. For instance, add a new model to manage custom notifications:
    ```python
    from django.db import models

    class Notification(models.Model):
        title = models.CharField(max_length=255)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
    ```

- Use shared configurations from the `shared` directory for consistency.

## Contribution

Contributions are welcome! Please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a Pull Request for review.

## Acknowledgments

- **OpenAI**: For their amazing GPT and DALL-E APIs.
- **Telegram**: For their robust bot platform.
- **FastAPI**: For a fast and efficient web framework.

---

### Contacts
For any inquiries or issues, please contact:
- **Project Maintainer**: Beaver (Telegram: @b3av3r)



### Kubernetes and Ansible implementation plan for API management in the Learn-2-Learn project

---

#### **1. Implementation goals**
-**API Management Automation**: Use Kubernetes for application orchestration (Django, FastAPI) and Ansible for configuration automation.
-**Security**: Secrets management using HashiCorp Vault with Kubernetes integration.
-**Flexibility**: Dynamic configuration and scaling of applications in different environments (dev, prod).
-**Configuration centralization**: Creation of a unified mechanism for managing settings at the level of the entire project.

---

#### **2. Organization of project files**

Creating new folders and files in the main project directory:

```
learn-2-learn/
├── ansible/
│ ├── README.md # Ansible playbook documentation
│ ├── playbooks/
│ │ ├── init_vault_secrets.yaml # Playbook for initializing Vault secrets
│ │ ├── deploy_k8s.yaml # Kubernetes deployment playbook
│ │ ├── deploy_api.yaml # API deployment playbook
│ │ ├── manage_secrets.yaml # Playbook for managing secrets
│ └── inventory/
│ ├── hosts.yaml # Inventory for Kubernetes clusters
│
├── k8s/
│   ├── manifests/
│   │   ├── django-deployment.yaml  # Deployment Django
│   │   ├── fastapi-deployment.yaml # Deployment FastAPI
│   │   ├── vault-secret.yaml       # Vault secrets
│   │   ├── ingress.yaml            # Ingress API
│   │   ├── vault-secretprovider.yaml # SecretProviderClass config
│   └── configmaps/
│       ├── django-config.yaml
│       ├── fastapi-config.yaml
```

