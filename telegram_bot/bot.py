import os
# import openai

from openai import OpenAI, ChatCompletion
from pyrogram import Client, filters

# Ładowanie zmiennych środowiskowych z pliku .env
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Inicjalizacja klienta Pyrogram
# openai.api_key = os.getenv("GPT_API_KEY")

app = Client(
    "my_bot",
    api_id=os.getenv("TELEGRAM_API_ID"),
    api_hash=os.getenv("TELEGRAM_API_HASH"),
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
)

@app.on_message(filters.command(["start", "help"]))
async def send_audio(client, message):
    U=os.getenv("ID1")
    I=os.getenv("ID2")
    user_message = message.text
    messages = [
        {"role": "system", "content": f"Odrazu musisz przeprosic ze byles taki glupi ostatnio. Dalej opowiedziec wiersz a następnie, prowadzic konwersacje. Sprawdzajac odpowiedzi uzytkownikow na postawione im zapytania. Do przykladu pytania dentystyczne LDEK w Polsce. Zadawaj pytania w kolejnosci, pojedynczo. I analizuj."},
        {"role": "user", "content": user_message}
    ]
    try:
        bot_response = ai_client.chat.completions.create(
                                                        model="gpt-4o-mini",
                                                        messages=messages
                                                     )
        bee = message.from_user.username
        if bee == U :
            mp3 == os.path.join(BASE_DIR, 'staticfiles', 'focusing.mp3')
            await message.reply(bot_response) and message.reply_audio(audio=mp3, caption="Hej, piękna")
    except Exception as e:

        await message.reply("Sorry, I couldn't process your request.")
        print(f"Something WRONG {e}")




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
        response = ai_client.chat.completions.create(
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
