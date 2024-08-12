import os
import openai

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

@app.on_message(filters.text)
async def handle_message(client, message):
    user_message = message.reply_text

    # Query OpenAI API
    response = openai.Completion.create(
        engine="gpt-4",  # Use the appropriate engine
        prompt=user_message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    bot_response = response.choices[0].text.strip()
    await message.reply(bot_response)

# Uruchomienie bota
if __name__ == "__main__":
    app.run()
