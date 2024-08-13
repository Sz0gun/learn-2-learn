
# Learn to Learn API - Telegram Bot API

## Project Description

The bot-api-1 project is a Telegram bot application integrated with the GPT-4 AI model. The bot is managed using the Pyrogram framework and operates in both local and production environments on the Heroku platform.

### Features

- Communication with users via Telegram.
- Use of the GPT-4 model to generate responses.
- Support for different types of communication (webhooks, long polling).
- Secure management of API keys and other sensitive information.

## Requirements

- Python 3.9+
- Heroku account (for production deployment)
- GPT-4 API Key
- Dependencies listed in `requirements.txt`

## Configuration

1. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory of the project.
   - Add the following variables to the `.env` file:
     ```plaintext
     TELEGRAM_API_KEY=<YOUR TELEGRAM API KEY>
     GPT_API_KEY=<YOUR GPT API KEY>
     SECRET_KEY=<YOUR SECRET KEY>
     DEBUG=False
     DATABASE_URL=<YOUR DATABASE URL>
     ```

2. **Install Dependencies:**
   - Run the following command to install required dependencies:
     ```bash
     pip install -r requirements.txt
     pip install pyrogram python-dotenv
     ```

3. **Run the Bot:**
   - Use the following command to run the bot locally:
     ```bash
     python telegram_bot/bot.py
     ```

4. **Deploy to Heroku:**
   - Ensure that your Heroku environment variables are set correctly.
   - Deploy the bot to Heroku and check logs to verify successful deployment.

## Project Structure

```plaintext
telegram-bot-api/
│
├── telegram_bot/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── bot.py  # main bot logic using Pyrogram
│
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
│
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── index.html
│
├── .gitignore
├── .dockerignore
├── Dockerfile
├── Procfile
├── README.md
├── manage.py
├── requirements.txt
└── .env  # Environment variables (excluded from version control)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/bot-api-1.git
    cd bot-api-1
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv botenv
    source botenv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure the `.env` file:

    Create a `.env` file in the main project directory and add the following variables:

    ```
    GPT_API_KEY=your-gpt-api-key
    TELEGRAM_API_ID=your-telegram-api-id
    TELEGRAM_API_HASH=your-telegram-api-hash
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token
    ```

5. Run the bot locally:

    ```bash
    python main.py
    ```

## Deployment on Heroku

1. Log in to Heroku and create a new application.
2. Connect the GitHub repository to Heroku.
3. Set environment variables in the Heroku dashboard (see the "Configuring the .env file" section).
4. Deploy the application to Heroku:

    ```bash
    git push heroku main
    ```

5. Run database migrations (if necessary):

    ```bash
    heroku run python manage.py migrate
    ```

## Testing

- You can test the bot locally using `ngrok` or `localtunnel` to redirect traffic to the local server.
- In the production environment on Heroku, ensure that the bot correctly handles all scenarios.

## Contributions

Bug reports and suggestions for new features are welcome. If you would like to contribute to the project, please open an issue on GitHub.

## License

The project is licensed under the ...|.

