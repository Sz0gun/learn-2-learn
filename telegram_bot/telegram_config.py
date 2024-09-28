import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Konfiguracja Telegram Bota
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not all([TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN]):
    raise Exception("Missing necessary Telegram Bot environment variables")
