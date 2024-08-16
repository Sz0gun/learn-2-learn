import openai
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import (
                            ReplyKeyboardMarkup, 
                            InlineKeyboardMarkup, 
                            InlineKeyboardButton
                            )
# from openai import OpenAI
import os

load_dotenv()


# OpenAI().api_key = os.getenv("OPENAI_API_KEY")
# api_key=os.getenv("OPENAI_API_KEY")
# ai_client = OpenAI()
openai.api_key = os.getenv('OPENAI_API_KEY')

class AIQuizBot:

    def __init__(self, client, question_list):
        self.client = client
        self.question_list = question_list
        self.current_question = {}
        self.conversation_history = {}

    async def send_question(self, chat_id):
        if self.question_list:
            question = self.question_list.pop(0)
            self.current_question[chat_id] = question
            conversation_history = self.conversation_history.get(chat_id, [])
            await self.client.send_message(chat_id, question)
            conversation_history.append({"role": "system", "content": question})
            self.conversation_history[chat_id] = conversation_history
        else:
            await self.client.send_message(chat_id, "No more questions available.")

    async def analyze_callback(self, chat_id, message):

        conversation_history = self.conversation_history.get(chat_id, [])
        conversation_history.append({"role": "user", "content": message})
        prompt = [
                {"role": "assistant", "content": "You are an AI assistant that maintains conversation history.You will need to verify the correctness of my answers. If the answer is correct, simply confirm it by adding 1-3 informational sentences for better understanding. In case of an incorrect answer, make one attempt to guide the user to the correct answer by providing a concise and relevant example, with a maximum of 7 sentences that could lead to the correct answer. After the user's second attempt, confirm or provide the correct answer. Always give the correct answer if the user asks for it."}
            ]
        prompt.extend(conversation_history)
        response = openai.ChatCompletion.create(
                                                    model="gpt-4o",
                                                    messages=prompt
                                                )

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=prompt
            )

        bot_response = response.choices[0].message['content']
        await self.client.send_message(chat_id, bot_response)

        conversation_history.append({"role": "assistant", "content": bot_response})
        self.conversation_history[chat_id] = conversation_history



    async def handle_user_interaction(self, chat_id, message):
        if message == 'q':
            if chat_id in self.conversation_history:
                del self.conversation_history[chat_id]
                await self.send_question(chat_id)
        else:
            await self.analyze_callback(chat_id, message)
        # del self.current_question[chat_id]  # Reset for the next question

    # def clear_all_conversations(self):
    # self.conversation_history.clear()

    # def clear_conversation(self, chat_id):
    # if chat_id in self.conversation_history:
    #     del self.conversation_history[chat_id]
# app = Client("my_bot")
# quiz_bot = AIQuizBot(app, question_list)
