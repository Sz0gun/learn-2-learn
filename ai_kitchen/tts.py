import os
import PyPDF2
import re
import unicodedata
import torch
import string
from torch.utils.data import DataLoader, Dataset
from TTS.api import TTS
from TTS.utils.manage import ModelManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'SRM.pdf')
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'SRM_1.wav')


class TextProcessor:
    @staticmethod
    def clean_text(text):
        # if isinstance(text, dict):
        # print(text['ldek'])
        # Normalize text to remove accents and special characters
        normalize_text = unicodedata.normalize('NFKD', text['srm']).encode('ASCII', 'ignore').decode('ASCII')
        # print(normalize_text)
        text['srm'] = normalize_text.lower()  # Convert to lowercase
        text = text['srm'].translate(str.maketrans('','', string.punctuation))  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Remove spaces
        return text.strip()


class TextDataset(Dataset):
    def __init__(self, text, max_length):
        self.text_chunks = self.split_text(text, max_length)

    def split_text(self, text, max_length):
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

    def __len__(self):
        return len(self.text_chunks)

    def __getitem__(self, idx):
        return self.text_chunks[idx]


class VitsTTS:
    def __init__(self, model_name="tts_models/pl/mai_female/vits"):
        device = 'cuda' if torch.cuda.is_available() else "cpu"
        self.tts_model = TTS(model_name=model_name, gpu=(device=="cuda"))
        self.device = device

    def text_to_speech(self, text, max_length=100):
        clean_text = TextProcessor.clean_text(text)
        dataset = TextDataset(clean_text, max_length)
        dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

        for i, chunk in enumerate(dataloader):
            chunk = chunk[0]
            self.tts_model.tts_to_file(text=chunk, file_path=f"{OUTPUT_FILE_PATH}_{i}.wav")
        

# class PDFToSpeech:
#     def __init__(self):
#         # Ładowanie modelu TTS dla języka polskiego
def convert_to_speech(text, output_path):
    
    tts_model = TTS(model_name="tts_models/pl/mai_female/vits")
    tts_model.tts_to_file(text=text, file_path=output_path)



def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
            # print(text)
    return text

def basic_text_correction(text):
    # Podstawowe poprawki, np. zastępowanie błędów OCR
    corrections = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "—": "-",
        "“": "\"",
        "”": "\"",
        "‘": "'",
        "’": "'"
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def filter_and_correct_text(text):
    # Podstawowa filtracja: usuwanie stopki, nagłówków i przypisów
    filtered_text = re.sub(r'(\n\d+\s+|Page\s+\d+)', '', text)  # Usuwa numery stron, podstawowe wzorce
    corrected_text = basic_text_correction(filtered_text)
    print("=====================")
    # print(corrected_text)
    return corrected_text


if __name__ == "__main__":
    # pdf_to_speech = PDFToSpeech()
    pdf_path = PDF_FILE_PATH
    text = {"srm": f"{extract_text_from_pdf(pdf_path)}"}
    # print (text['ldek'])
    # cleaned_text = TextProcessor.clean_text(text)
    # print (cleaned_text)
    # output_path = OUTPUT_FILE_PATH
    vits_tts = VitsTTS()
    vits_tts.text_to_speech(text, 2000)

    # filter_txt = filter_and_correct_text(text)
    # convert_to_speech(cleaned_text, output_path)