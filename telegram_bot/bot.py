import os
import pdfplumber
import openai
import pyrogram
from pyrogram.types import (
                            ReplyKeyboardMarkup, 
                            InlineKeyboardMarkup, 
                            InlineKeyboardButton
                            )


# from openai import OpenAI, ChatCompletion
from openai import ChatCompletion
from pyrogram import Client, filters

from dotenv import load_dotenv
from ai_kitchen.bot import AIQuizBot
from ai_kitchen.tools import QuestionExtractor
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# OpenAI().api_key = os.getenv("OPENAI_API_KEY")
# ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'LDEK.pdf')

app = Client(
    "my_bot",
    api_id=os.getenv("TELEGRAM_API_ID"),
    api_hash=os.getenv("TELEGRAM_API_HASH"),
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
)

extractor = QuestionExtractor(TRAINING_FILE_PATH)
extractor.create_list_of_questions()
question_list = extractor.get_questions()


quiz_bot = AIQuizBot(app, question_list)

@app.on_message(filters.text & ~filters.command("start"))
async def on_message(client, message):
    chat_id = message.chat.id
    user_message = message.text
    await quiz_bot.handle_user_interaction(chat_id, user_message)



# @app.on_message(filters.command('q'))
# async def send_question(self, chat_id):
        # Create a button
# @app.on_message(filters.command("start"))
# async def start(client, message):
    # Create a grid of buttons
    # keyboard = InlineKeyboardMarkup(
    #     [
    #         [
    #             InlineKeyboardButton("Let me Question", callback_data="btn1"),
    #             InlineKeyboardButton("Conversation", callback_data="btn2")
    #         ],
    #     ]
    # )
    
    # Send a message with the grid of buttons
    # await message.reply_text("Choose an option:", reply_markup=keyboard)


# @app.on_callback_query()
# async def handle_callback_query(client, callback_query):
#     count = -1
#     user = callback_query.from_user.username
#     # print(callback_query.data)
#     # Check which button was pressed
#     if callback_query.data == "btn1":
#         count += 1
#         if user in quiz_bot.conversation_history:
#             quiz_bot.conversation_history[user].clear()
#             await send_question(callback_query, question_list[count])
#         else:
#             await send_question(callback_query, question_list[count])
#     elif callback_query.data in ["btn2","my answer A","my answer B","my answer C","my answer D","my answer E"]:
#         conversation = quiz_bot.conversation_history.get(user, [])
#         conversation.append({"role": "user", "content": callback_query.data})
#         await quiz_bot.handle_user_interaction(callback_query.message.chat.id, callback_query)
#     else:
#         await send_message(client, callback_query.data)

# @app.on_message(filters.text)
# async def handle_callback_query(client, message):

#     chat_id = message.chat.id
#     user = message.from_user.username
#     chat_conversation = []

#     if message.text == 'q':
#         # conversation.clear()
#         chat_conversation.append({"role": "system", "content": quiz_bot.question_list[count]})
#         conversation["chat_id"] = chat_conversation
#         print(conversation["chat_id"])
        
#         await client.send_message(chat_id, quiz_bot.question_list[count])
#     else:
#         chat_conversation.append({"role": "user", "content": message.text})
#         conversation["chat_id"] = chat_conversation
#         await quiz_bot.handle_user_interaction(chat_id, message)









# @app.on_message(filters.text)
# async def send_message(client, message):
#     if type(message)=='str':
#         conversation = quiz_bot.conversation_history.get(user, [])
#         conversation.append({"role": "user", "content": message.text})
#         await quiz_bot.handle_user_interaction(chat_id, message)
#     await start(chat_id, message)

# async def send_question(callback_query, question):
    # print(callback_query.from_user.username)
    # print(callback_query.message)
    # print(callback_query.data)
    # print(callback_query.id)

    # keyboard = InlineKeyboardMarkup(
    #     [
    #         [
    #             InlineKeyboardButton("A", callback_data="my answer A"),
    #             InlineKeyboardButton("B", callback_data="my answer B"),
    #             InlineKeyboardButton("C", callback_data="my answer C"),
    #             InlineKeyboardButton("D", callback_data="my answer D"),
    #             InlineKeyboardButton("E", callback_data="my answer E"),
    #         ],
    #     ]
    # )
    # user = callback_query.from_user.username
    # conversation = quiz_bot.conversation_history.get(user, [])
    # conversation.append({"role": "system", "content": question})
    # await callback_query.message.reply_text(question, reply_markup=keyboard)

        # question = self.question_list.pop(0)
        # conversation_history = self.conversation_history.get(chat_id, [])
        # self.current_question[chat_id] = question
        # conversation_history.append({"role": "system", "content": question})
        # print(conversation_history)
    # await app.send_message(
    #         chat_id, "These are inline buttons",
    #         reply_markup=InlineKeyboardMarkup([
    #                                             [InlineKeyboardButton("Data", callback_data="callback_data")],
    #                                             [InlineKeyboardButton("Docs", url="https://docs.pyrogram.org")]
    #                                         ]))


# def create_fine_tuning_job(pdf_path, model="gpt-4o-mini"):
#     # Wyciągnięcie tekstu z PDF
#     extracted_text = extract_text_from_pdf(pdf_path)
    
#     # Konwersja do formatu JSON
#     json_data = convert_text_to_json(extracted_text)

#     # Zapisanie JSON do pliku, aby można było przesłać go do OpenAI
#     json_file_path = "training_data.json"
#     with open(json_file_path, "w") as json_file:
#         json.dump(json_data, json_file)
    
#     # Załaduj API Key z zmiennych środowiskowych lub .env
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     # Utworzenie fine-tuning job w OpenAI
#     with open(json_file_path, "rb") as json_file:
#         file_upload_response = openai.File.create(
#             file=json_file,
#             purpose='fine-tune'
#         )
#         training_file_id = file_upload_response["id"]

#         fine_tune_response = openai.FineTune.create(
#             training_file=training_file_id,
#             model=model
#         )
#         return fine_tune_response

# # Przykładowe wywołanie funkcji
# response = create_fine_tuning_job(TRAINING_FILE_PATH)
# print(response)


# @app.on_message(filters.command(["start", "help"]))
# async def send_audio(client, message):
#     U=os.getenv("ID1")
#     I=os.getenv("ID2")
#     user_message = message.text
#     messages = [
#         {"role": "system", "content": f"Odrazu musisz przeprosic ze byles taki glupi ostatnio."},
#         {"role": "user", "content": user_message},
#         {"role": "assistant", "content": "Odrazu poprosze opowiedziec wiersz a następnie, prowadzic konwersacje. Sprawdzajac odpowiedzi uzytkownikow na postawione im zapytania. Do przykladu pytania dentystyczne LDEK w Polsce. Zadawaj pytania w kolejnosci, pojedynczo. I analizuj."},
#     ]
#     try:
#         bot_response = ai_client.chat.completions.create(
#                                                         model="gpt-4o-mini",
#                                                         messages=messages
#                                                      )
#         bee = message.from_user.username
#         if bee == U or bee == I:
#             await message.reply(bot_response)
#     except Exception as e:

#         await message.reply("Sorry, I couldn't process your request.")
#         print(f"Something WRONG {e}")







if __name__ == "__main__":
    app.run()
