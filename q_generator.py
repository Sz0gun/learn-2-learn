# import PyPDF2
import re
import os
import django
from django.conf import settings

import pdfplumber
from pathlib import Path
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

BASE_DIR = settings.BASE_DIR
TRAINING_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'LDEK.pdf')
print(TRAINING_FILE_PATH)


pattern = re.compile(r'(Nr \d+\..*?)(?=Nr \d+|$)', re.DOTALL)


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text

question_list = []


def create_list_of_questions(text):
    t1 = extract_text_from_pdf("LDEK.pdf")
    matches = re.finditer(pattern, t1)
    for match in matches:
        content = match.group(1).strip()
        question_list.append(content)

# Compile a regex pattern to match each question block


# Function to parse the content of a PDF and organize it into a dictionary
def parse_pdf(path):
    with pdfplumber.open(path) as file:
        # print (file)
#         reader = PyPDF2.PdfReader(file)
        full_text = ''
        for page in file.pages:
            full_text += page.extract_text() + "\n"
        # print(full_text)
        # Regex pattern to match questions, answers, and correct answers
        pattern = re.split(r'(Nr\.\s*(\d+)\.\s*(.*?)\n([A-E])\.\s*(.*?)\n([A-E])\.\s*(.*?)\n([A-E])\.\s*(.*?)\n([A-E])\.\s*(.*?)\nPrawidłowa odpowiedź to:\s*([A-E])\.)', full_text.strip())
        # pattern = r'Nr\.\s*(\d+)\.\s*(.*?)\.'
        # print(pattern)

        # pattern = r'Nr\.\s*(\d+)\.\s*(.*?)\s*([A-E])\.\s*(.*?)\s*([A-E])\.\s*(.*?)\s*([A-E])\.\s*(.*?)\s*([A-E])\.\s*(.*?)\s*Prawidłowa odpowiedź to:\s*([A-E])\.'
        # Find all matches
        # matches = re.findall(pattern, full_text)
        # print(matches)
        # Building the dictionary
        result = {}
        # for patt in pattern:
            # print (patt)
        #     question_number = match[0]
        #     print(question_number)
        #     question = match[1]
        #     answers = {match[2]: match[3], match[4]: match[5], match[6]: match[7], match[8]: match[9]}
        #     correct_answer = match[10]
            
        #     result[f"Nr. {question_number}"] = {
        #         "question": question,
        #         "answers": answers,
        #         "correct_answer": correct_answer
        #     }
        # return result

# Path to the PDF file
pdf_path = "LDEK.pdf"
# Parse the PDF
parsed_data = parse_pdf(pdf_path)
print(parsed_data)

