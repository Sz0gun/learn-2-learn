import pdfplumber
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'LDEK.pdf')


class QuestionExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.question_list = []

    def extract_text_from_pdf(self):
        """Extracts text from the entire PDF file."""
        full_text = ''
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text()
        return full_text

    def create_list_of_questions(self):
        """Creates a list of questions from the extracted text."""
        text = self.extract_text_from_pdf()

        # Pattern to match questions
        pattern = re.compile(r'(Nr \d+\..*?)(?=Nr \d+|$)', re.DOTALL)

        # Finding all matches
        matches = re.finditer(pattern, text)

        # Append each match to the question list
        for match in matches:
            content = match.group(1).strip()
            self.question_list.append(content)

    def get_questions(self):
        """Returns the list of questions."""
        return self.question_list


extractor = QuestionExtractor(TRAINING_FILE_PATH)
extractor.create_list_of_questions()
questions = extractor.get_questions()




