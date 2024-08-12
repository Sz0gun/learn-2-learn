import os
from pyrogram import Client, filters

# Ładowanie zmiennych środowiskowych z pliku .env
from dotenv import load_dotenv
load_dotenv()

# Inicjalizacja klienta Pyrogram
app = Client(
    "my_bot",
    api_id=os.getenv("TELEGRAM_API_ID"),
    api_hash=os.getenv("TELEGRAM_API_HASH"),
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
)

@app.on_message()
def handle_message(client, message):
    message.reply_text(f"Hello, {message.from_user.first_name}!")

# Uruchomienie bota
if __name__ == "__main__":
    app.run()
