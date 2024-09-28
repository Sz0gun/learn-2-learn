import os
from pyrogram import Client, filters
from PIL import Image
from gcs_auth import GCPService
from esrgan_model_processor import ESRGANProcessor
import openai
from telegram_config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN

# Set the OpenAI API key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Pyrogram client using the configuration from telegram_config.py
app = Client(
    "my_bot",
    api_id=TELEGRAM_API_ID,          # Telegram API ID for the bot
    api_hash=TELEGRAM_API_HASH,      # Telegram API Hash for the bot
    bot_token=TELEGRAM_BOT_TOKEN     # Telegram bot token
)

# Initialize GCS service and ESRGAN processor
gcs_service = GCPService()
esrgan_processor = ESRGANProcessor()

def enhance_and_upload_image(photo_path, user_id):
    """
    Function to enhance an image using the ESRGAN processor
    and upload it to Google Cloud Storage (GCS).

    Args:
        photo_path (str): Path to the downloaded photo.
        user_id (int): Telegram user ID.

    Returns:
        str: URL of the uploaded image in GCS.
    """
    # Enhance the image using ESRGAN
    enhanced_image = esrgan_processor.enhance_image(photo_path)
    
    # Define the output path for the enhanced image
    output_path = f"{user_id}_enhanced.jpg"
    
    # Save the enhanced image
    enhanced_image.save(output_path)
    
    # Upload the enhanced image to GCS and return the URL
    url = gcs_service.upload_to_gcs(output_path, user_id)
    return url

@app.on_message(filters.photo)
async def handle_image(client, message):
    """
    Handles incoming photo messages from users.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The received message containing a photo.
    """
    # Download the photo sent by the user
    photo_path = message.download()
    
    # Enhance and upload the image, then get the URL
    url = enhance_and_upload_image(photo_path, message.from_user.id)
    
    # Reply to the user with the URL of the enhanced image
    await message.reply_text(f"Here is the enhanced image: {url}")

@app.on_message(filters.text)
async def handle_text(client, message):
    """
    Handles incoming text messages from users by generating a
    response using the OpenAI GPT-4o model.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The received text message from the user.
    """
    # Extract the user's message text
    user_message = message.text

    # Use OpenAI GPT-4o to generate a response based on the user's message
    response = openai.Completion.create(
        model="gpt-4o",       # Model to use for text completion
        prompt=user_message,  # User's input message
        max_tokens=100        # Limit the number of tokens in the response
    )

    # Reply to the user with the generated response
    await message.reply_text(response.choices[0].text.strip())

if __name__ == "__main__":
    # Run the Telegram bot
    app.run()
