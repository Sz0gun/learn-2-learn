import os
import openai

from openai import OpenAI, ChatCompletion
from pyrogram import Client, filters

# Ładowanie zmiennych środowiskowych z pliku .env
from dotenv import load_dotenv

client = OpenAI(api_key=os.getenv("GPT_API_KEY"))
load_dotenv()

# Inicjalizacja klienta Pyrogram
# openai.api_key = os.getenv("GPT_API_KEY")

app = Client(
    "my_bot",
    api_id=os.getenv("TELEGRAM_API_ID"),
    api_hash=os.getenv("TELEGRAM_API_HASH"),
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
)

@app.on_message(filters.text)
async def handle(client, message):
    # Odbierz treść wiadomości użytkownika
    user_message = message.text

    # Przygotuj dane do wysłania do modelu AI
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    try:
        # Wyślij wiadomość do modelu OpenAI i odbierz odpowiedź
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Odbierz odpowiedź modelu AI
        bot_response = response.choices[0].message.content

        # Prześlij odpowiedź modelu AI do użytkownika w czacie
        await message.reply(bot_response)

    except Exception as e:
        # W razie błędu, przekaż informację do użytkownika
        await message.reply("Sorry, I couldn't process your request.")
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run()
