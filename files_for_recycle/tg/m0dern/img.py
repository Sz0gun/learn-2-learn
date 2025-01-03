import openai
import aiofiles
import httpx
from shared.settings import config

class ImageGenerator:
    def __init__(self, client):
        self.api_key = config.OPENAI_API
        openai.api_key = self.api_key
        self.client = client

    async def generate_image(self, prompt: str, user_id: int):
        """
        It generates an image based on the description and sends it directly to the user on Telegram.

        Args:
            prompt (str): Description of the image to generate.
            user_id (int): Telegram user ID.

        Returns:
            None

        Raises:
            Exception: If image generation fails.
        """
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            image_url = response['data'][0]['url']

            # Pobieranie obrazu z URL
            async with httpx.AsyncClient() as client:
                img_response = await client.get(image_url)

            # Wyslanie obrazu do uzytkownika w Telegramie
            await self.client.send_file(user_id, img_response.content, caption=f"Image generated from: {prompt}")
        
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")