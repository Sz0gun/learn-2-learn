# Learn-2-Learn (L2L)

## Overview
Learn-2-Learn (L2L) is a modular, scalable platform designed to facilitate collaborative learning and AI-driven assistance. The project integrates FastAPI, Django, Telethon, and modern AI tools like OpenAI models to create a seamless, interactive experience.

## Features

- **Telegram Bot Integration**: Manage user interactions and commands through a Telegram bot.
- **WebSocket Communication**: Real-time communication between Telegram and the backend.
- **Image Generation**: Generate AI-driven images using OpenAI API.
- **Extensibility**: Modular architecture for easy addition of new features.
- **Multi-database Support**: Integration with PostgreSQL, Redis, CouchDB, and PouchDB for optimized data handling.
- **Asynchronous Processing**: Built-in support for async operations, improving performance.

---

## Project Structure

```plaintext
learn-2-learn/
├── dj_rest/                # Django application for RESTful API
│   ├── core/               # Core settings and configurations
│   ├── manage.py           # Django management script
├── fa/                     # FastAPI application
│   ├── routes/             # FastAPI route definitions
│   ├── fst_app.py          # FastAPI app entry point
├── tg/                     # Telegram bot-related logic
│   ├── m0dern/             # Core logic for m0dern bot
│   ├── azer0th/            # Main menu and interaction logic
│   ├── cmd/                # Command handlers
│   ├── check.py            # Connectivity and validation functions
├── shared/                 # Shared configurations and utilities
├── docker-compose.yml      # Docker configuration for multi-service setup
├── requirements.txt        # Python dependencies
```

---

## Installation

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- Redis, PostgreSQL, CouchDB (if applicable)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Sz0gun/learn-2-learn.git
   cd learn-2-learn
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file:
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   FASTAPI_TITLE=Learn2Learn API
   FASTAPI_VERSION=1.0.0
   TG_API_ID=your-telegram-api-id
   TG_API_HASH=your-telegram-api-hash
   TG_BOT_TOKEN=your-telegram-bot-token
   TG_CHANNEL=your-telegram-channel-url
   OPENAI_API=your-openai-api-key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```
4. Run the application using Docker:
   ```bash
   docker-compose up --build
   ```
5. Access services:
   - Django Admin: [http://localhost:8000/admin](http://localhost:8000/admin)
   - FastAPI Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## Usage

### Telegram Bot
- Send `/menu` to the bot to access the main menu.
- Use buttons for actions like image generation and AI-assisted chat.

### Development
- Add new features by extending the `tg`, `fa`, or `dj_rest` modules.
- Use shared configurations from the `shared` directory for consistency.

---

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- **OpenAI**: For their amazing GPT and DALL-E APIs.
- **Telegram**: For their robust bot platform.
- **FastAPI**: For a fast and efficient web framework.

---

### Contacts
For any inquiries or issues, please contact:
- **Project Maintainer**: Beaver (Telegram: @b3av3r)
