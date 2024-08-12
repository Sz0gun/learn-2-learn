
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

The project is licensed under the MIT License.

