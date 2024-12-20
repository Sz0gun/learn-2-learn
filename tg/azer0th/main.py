from telethon import TelegramClient, events, Button

from shared.settings import config
from tg.m0dern.img import ImageGenerator

class AzerothMain:
    def __init__(self, client):
        self.client = client
        self.image_generator = ImageGenerator(client)
    
    async def send_menu(self, user_id):
        await self.client.send_message(
            user_id,
            "Witaj w Azeroth! W jakim celu zawiales?",
            buttons=[
                [Button.inline("🖼️ Generate Image", b"generate_image")],
                [Button.url("🤖 AI Assistant Chat", config.m0dern)],
            ]
    )
    
    def register_handlers(self):
        """
        Rejestruje eventy obslugiwane przez glowne menu Azeroth.
        """
        @self.client.on(events.ChatAction) # Rejestruje na akcje w kanale
        async def handle_user_join(event):
            """
            Obsluguje wejscie uzytkownika do kanalu.
            """
            if event.user_added or event.user_joined:
                await self.send_menu(event.user_id)

        @self.client.on(events.CallbackQuery(data=b"generate_image"))
        async def handle_generate_image(event):
            await event.edit(
                text="Podaj opis obrazu, który chcesz wygenerować:",
                buttons=[[Button.inline("🔙 Powrót do menu głównego", b"back_to_menu")]]
            )

            @self.client.on(events.NewMessage(pattern=".*"))
            async def handle_prompt(message_event):
                prompt = message_event.message.message
                await message_event.respond("Generuje obraz, prosze czekac...")
                try:
                    await self.image_generator.generate_image(prompt=prompt, user_id=message_event.sender_id)
                    await message_event.respond("Obraz zostal wygenerowany i wyslany!")
                except Exception as e:
                    await message_event.respond(f"Wystapil blad: {str(e)}")

        @self.client.on(events.CallbackQuery(data=b"back_to_menu"))
        async def handle_back_to_menu(event):
            await self.send_menu(event.sender_id)

        @self.client.on(events.NewMessage(pattern='/menu'))
        async def handle_menu_command(event):
            await self.send_menu(event.sender_id)


# Klient Telegram uruchamiamy przez FastAPI