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
        Generuje obraz na podstawie opisu i wysyła go bezpośrednio do użytkownika w Telegramie.

        Args:
            prompt (str): Opis obrazu do wygenerowania.
            user_id (int): ID użytkownika w Telegramie.

        Returns:
            None

        Raises:
            Exception: Jeśli generowanie obrazu nie powiedzie się.
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
            await self.client.send_file(user_id, img_response.content, caption=f"Obraz wygenerowany na podstawie: {prompt}")
        
        except Exception as e:
            raise Exception(f"Blad pod czas generowania obrazu: {str(e)}")