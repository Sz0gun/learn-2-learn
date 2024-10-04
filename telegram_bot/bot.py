import os
from pyrogram import Client, filters
from PIL import Image
import openai
from telegram_config import  TELEGRAM_BOT_TOKEN

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Pyrogram client using the configuration from telegram_config.py
app = Client(
    "my_bot",
    bot_token=os.getenv('TELEGRAM_BOT_TOKEN')
)




@app.on_message(filters.text)
async def handle_text(client, message):
    """
    Handles incoming text messages from users by generating a
    response using the OpenAI GPT-4o model.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The received text message from the user.
    """
    user_message = message.text

    # Use OpenAI GPT-4o to generate a response based on the user's message
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=user_message,
        max_tokens=100
    )

    await message.reply_text(response.choices[0].text.strip())

if __name__ == "__main__":

    app.run()
