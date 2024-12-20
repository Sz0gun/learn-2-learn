# tg/check.py

from telethon import TelegramClient, events
from shared.settings import config

class Check:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def forward_to_telegram(self, command: str):

        try:
            await self.client.send_message(config.TG_CHANNEL, f"Command: {command}")
            return f"Command '{command}' sent via Telethon."
        except Exception as e:
            return f"Telethon error: {str(e)}"

            
    def register_handlers(self):
        """
        Rejestruje eventy obslugivane przez klienta Telegrama.
        """
        @self.client.on(events.NewMessage(pattern="/ping"))
        async def handle_ping(event):
            """
            Obsluguje polecenie '/ping' w Telegramie.
            """
            response = await self.forward_to_telegram("ping")
            await event.respond(f"Odpowiedz WS: {response}")
        
        @self.client.on(events.NewMessage(pattern="/status"))
        async def handle_status(event):
            """
            Obsluguje polecenie '/status' w Telegramie.
            """
            await event.respond("Bot jest gotowy do pracy!")