import os
import openai
import pdfplumber
# import openai

from openai import OpenAI, ChatCompletion
from pyrogram import Client, filters

# Ładowanie zmiennych środowiskowych z pliku .env
from dotenv import load_dotenv
load_dotenv()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# TRAINING_FILE_PATH = os.path.join(BASE_DIR, 'LDEK.pdf')
file_path = os.path.join(settings.STATICFILES_DIRS[0], 'LDEK.pdf')
print(TRAINING_FILE_PATH)
# TRAINING_json_PATH = os.path.join(BASE_DIR, 'staticfiles', '')


# Inicjalizacja klienta Pyrogram
openai.api_key = os.getenv("GPT_API_KEY")

app = Client(
    "my_bot",
    api_id=os.getenv("TELEGRAM_API_ID"),
    api_hash=os.getenv("TELEGRAM_API_HASH"),
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN")
)


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
            print(full_text)
    return full_text

extract_text_from_pdf(file_path)

def convert_text_to_json(text):
    # Możesz tu dodać dodatkową logikę do przetwarzania tekstu, jeżeli jest to potrzebne.
    json_data = {"content": text}
    return json_data

def create_fine_tuning_job(pdf_path, model="gpt-4o-mini"):
    # Wyciągnięcie tekstu z PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Konwersja do formatu JSON
    json_data = convert_text_to_json(extracted_text)

    # Zapisanie JSON do pliku, aby można było przesłać go do OpenAI
    json_file_path = "training_data.json"
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file)
    
    # Załaduj API Key z zmiennych środowiskowych lub .env
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Utworzenie fine-tuning job w OpenAI
    with open(json_file_path, "rb") as json_file:
        file_upload_response = openai.File.create(
            file=json_file,
            purpose='fine-tune'
        )
        training_file_id = file_upload_response["id"]

        fine_tune_response = openai.FineTune.create(
            training_file=training_file_id,
            model=model
        )
        return fine_tune_response

# Przykładowe wywołanie funkcji
# response = create_fine_tuning_job(TRAINING_json_PATH)
# print(response)
if __name__ == "__main__":
    app.run()
