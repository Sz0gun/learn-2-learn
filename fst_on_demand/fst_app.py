from fastapi import FastAPI

app = FastAPI(title="Minimal FastAPI App", version="0.1")

@app.get("/")
def root():
    return {"status": "running"}




# # /fa/fst_app.py

# from fastapi import FastAPI
# from telethon import TelegramClient

# from shared.settings import config
# from tg.check import Check
# from tg.azer0th.main import AzerothMain

# # FastAPI init ...
# app = FastAPI(
#     title=config.FASTAPI_TITLE,
#     version=config.FASTAPI_VERSION,
# )

# # Telegram and WebSocket init ...
# tg_client = TelegramClient("bot", config.TG_API_ID, config.TG_API_HASH)

# check = Check(client=tg_client)
# azeroth_main = AzerothMain(client=tg_client)

# @app.on_event("startup")
# async def startup_event():
#     await tg_client.start(bot_token=config.TG_BOT_TOKEN)
#     check.register_handlers()
#     azeroth_main.register_handlers()
#     print('Telegram client started')

# @app.on_event("shutdown")
# async def shutdown_event():
#     await tg_client.disconnect()
#     print("Telegram client disconected")

