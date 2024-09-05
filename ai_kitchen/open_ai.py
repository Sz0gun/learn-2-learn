import os
import PyPDF2
import re
import torch
import io
import cv2
import gc
import numpy as np
import unicodedata
import pytesseract
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image, ImageEnhance, ImageFilter
from torch import nn


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'BOOK.pdf')

OUTPUT_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'SRM_1.wav')

ESRGAN_MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'ESRGAN_SRx4_official.pth')

class PDFTextAndImageExtractor:
    def __init__(self, pdf_stream, tesseract_lang='pol', model_path=ESRGAN_MODEL_PATH):
        self.pdf_stream = pdf_stream.read()
        self.tesseract_lang = tesseract_lang
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_esrgan_model(model_path)

    def load_esrgan_model(self, model_path):
        """ Load the ESRGAN model """
        model = torch.load(model_path, map_location=self.device)
        model.eval()
        return model

    def preprocess_image(self, image):
        """ Convert image to tensor and normalize """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).to(self.device)
        return image

    def postprocess_image(self, tensor):
        """ Convert tensor back to image format """
        tensor = tensor.swueeze(0).cpu().permute(1, 2, 0).numpy()
        tensor = np.clip(tensor * 255.0, 0, 255).astype(np.uint8)
        tensor = cv2.cvtColor(tensor, cv2.COLOR_RGB2BGR)
        return tensor
    
    def apply_super_resolution(self, image):
        """ Apply ESRGAN Super Resolution to an image """
        input_tensor = self.preprocess_image(image)
        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        enhanced_image = self.postprocess_image(output_tensor)
        return enhanced_image

    def extract_images(self):
        """
        Extract images from the PDF file as single pages.
        """
        pdf_reader = PdfReader(io.BytesIO(self.pdf_stream))

        # > for page_number in range(len(pdf_reader.pages)):
        for page_number in range(len(pdf_reader.pages[110:120])):
            page = pdf_reader.pages[page_number]
            output_stream = io.BytesIO()
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)
            pdf_writer.write(output_stream)
            page_bytes = output_stream.getvalue()

            try:
                images = convert_from_bytes(page_bytes)
                for image in images:
                    yield image
                    image.close()
                    del images
                    gc.collect()
                output_stream.close()

            except Exception as e:
                print (f"Error extracting images from page {page_number}: {e}")

    def smooth_image(self, image):
        """
        Applies smoothing to the image using Gaussian Blur and Median Blur.
        This helps in reducing noise and preparing the image for noise removal.
        """
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(image, (1, 1), 0)
        smoothed_image = cv2.medianBlur(gaussian_blur, 1)
        return smoothed_image

    def enhance_image(self, image):
        """
        Enhances the image quality by reducing noise and improving contrast and sharpness.
        """
        # Apply bilateral filtering to reduce noise while preserving edges
        denoised_image = cv2.bilateralFilter(image, d=3, sigmaColor=25, sigmaSpace=25)

        # Apply fastNlMeansDenoisingColored to further reduce noise in the color image
        denoised_image = cv2.fastNlMeansDenoisingColored(denoised_image, None, h=3, templateWindowSize=7, searchWindowSize=21)

        # Sharpen the image
        kernel = np.array([
            [0, -0.7, 0],
            [-0.7, 4, -0.7],
            [0, -0.7, 0]
        ])
        sharpened_image = cv2.filter2D(denoised_image, -1, kernel)

        # Apply morphological closing to perserve small details
        # kernel = np.ones((1, 1), np.uint8)
        # morph_image = cv2.morphologyEx(sharpened_image, cv2.MORPH_CLOSE, kernel)

        # Adjust contrast using CLAHE
        lab = cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=0.9, tileGridSize=(8, 8))
        cl = clahe.apply(l_channel)
        limg = cv2.merge((cl, a_channel, b_channel))
        enhanced_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR) 

        return enhanced_image

    def detect_and_expand_contours(self, image, page_number, margin_step=50, max_margin=500, initial_margin=150):
        """
        Detects contours in the image, checks them for text,
        and expands the area around contours if there is no text.
        """
        print ("Embeded images start")

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 100, 200)

        # Contour detection
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Processing detected contour

        for idx, contour in enumerate(contours):                                           # <<< TEST
            print (f"Contour index: {idx}, Number of points in contour: {len(contour)}")   # <|

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Apply initial margin (70x70 pixels)
            x = max(x - initial_margin, 0)
            y = max(y - initial_margin, 0)
            w = min(w + 2 * initial_margin, image.shape[1] - x)
            h = min(h + 2 * initial_margin, image.shape[0] - y)

            roi = image[y:y + h , x:x + w]

            print(f"X={x}, Y={y}, W={w}, H={h}")                                           # <<< TEST

            # Check if the area contains text
            text = pytesseract.image_to_string(roi, lang=self.tesseract_lang)

            if text.strip():                                                               # <?
                print ("Text detected", text)
            else:
                print ("No text detected")                                                 # <|

            if len(text.strip()) == 0:
                print("Detected possible image region.")

                # Expanding the area as long as there are no new contours around
                current_margin = 0
                expand_direction = {
                    'left': True,
                    'right': True,
                    'top': True,
                    'bottom': True
                }

                while current_margin < max_margin:
                    # Only expand margins in directions where no text has been detected
                    new_x = max(x - current_margin if expand_direction['left'] else x, 0)
                    new_y = max(y - current_margin if expand_direction['top'] else y, 0)
                    new_w = min(w + 2 * current_margin if expand_direction['right'] else w, image.shape[1] - new_x)
                    new_h = min(h + 2 * current_margin if expand_direction['bottom'] else h, image.shape[0] - new_y)

                    # Crop the expanded area
                    expanded_roi = image[new_y:new_y + new_h, new_x:new_x + new_w]

                    print(f"X 1={new_x}, Y 1={new_y}, W 1={new_w}, H 1={new_h}")                                          # <<< TEST
                    print (current_margin)
                    cv2.imshow("Region of interest", expanded_roi)
                    cv2.waitKey(1000)
                    cv2.destroyAllWindows()                                                         # <|

                    # Check for text in the new boundaries
                    expanded_text = pytesseract.image_to_string(expanded_roi, lang=self.tesseract_lang)

                    if len(expanded_text.strip()) > 0:
                        print (f"Detected text during expansion at margin {current_margin}, Stoping expansion in relevant direction.")
                        # If text is detected, stop expanding in that direction
                        if new_x < x:
                            expand_direction['left'] = False
                        if new_y < y:
                            expand_direction['top'] = False
                        if new_w > w:
                            expand_direction['right'] = False
                        if new_h > h:
                            expand_direction['bottom'] = False

                        # If no direction is left to expand, break the loop
                        if not any(expand_direction.values()):
                            print ("All directions have detected contour. Stoping expansion.")
                            break
                        
                        else:
                            # Search for contours in the expanded area if no text is found
                            expanded_gray = cv2.cvtColor(expanded_roi, COLOR_BGR2GRAY)
                            expanded_edges = cv2.Canny(expanded_gray, 100, 200)
                            expanded_contours, _ = cv2.findContours(expanded_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                            if expanded_contours:
                                print (f"Expanding region at margin {current_margin} with new contours detected")
                                x, y, w, h = new_x, new_y, new_w, new_h
                            else:
                                print ("No more contours detected. Stoping expansion.")
                                break

                    # Increase the margin for the next iteration
                    current_margin += margin_step

    def remove_text_and_get_image_coords(self, image, page_number):
        """
        Drtects text area on the page, removes them, and extracts the coordinates
        of potential image areas
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to improve text detection
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Use Tesseract with custom configurations to detect text regions
        custom_config = r'--oem 3 --psm 6'
        data = pytesseract.image_to_data(image, lang=self.tesseract_lang, output_type=pytesseract.Output.DICT, config=custom_config)

        # Iterate over detected text areas and remove them from the image
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0: # Only consider text boxes with a valid confidence score
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                # Fill the area where text is detected with white (255)
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)

        cv2.imshow(f"Page {page_number} - Cleaned image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Now the image should contain only non-text elements (potential images)
        # Perform edge detection to detect remaining objects (likely images)
        edges = cv2.Canny(gray, 50, 150)

        # Detect contours of remaining objects
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        image_coords = []

        # Process the contours to get coordinates of potential images
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 50:
                image_coords.append((x, y, w, h))
                roi = image[y:y + h, x:x + w]

                cv2.imshow("Region of interest", roi)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

        return image_coords


    def process_pdf(self):
        """
        Process all PDF pages: extracts images, analyzes contours, and saves image regions.
        """
        for page_number, image_pil in enumerate(self.extract_images()):
            # Convert the PIL image to OpenCV format (Numpy array)
            image_cv = np.array(image_pil)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

            # image_cv_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)


 
            # Detect and expand contours in each page
            # self.remove_text_and_get_image_coords(image_cv, page_number)

            enh_image = self.apply_super_resolution(image_cv)




            # Display the cleaned page without artifacts
            cv2.imshow(f"Page {page_number} - Cleaned Image", enh_image)

            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()


            # Memory cleanup
            del image_cv
            gc.collect()

    def extract_text(self):
        """

        """
        print('ok3')

        extracted_text = []

        for image in self.extract_images():
            text = pytesseract.image_to_string(image, lang=self.tesseract_lang)
            extracted_text.append(text)
            # Memory release
            del text
            gc.collect()

        full_text = "\n".join(extracted_text)
        del extracted_text
        gc.collect()
        # return self.


# ==========================
def preprocess_image(image):
    # Convert to grayscale
    image = image.convert('L')
    # Enhance contrast
    image = ImageEnhance.Contrast(image).enhance(2)
    # Apply median filter
    image = image.filter(ImageFilter.MedianFilter())
    return image

def ocr_pdf(pdf_path, language='pl'):
    with tempfile.TemporaryDirectory() as tempdir:
        # Convert PDF to a list of images, stored temporarily
        images = convert_from_path(pdf_path, output_folder=tempdir)

        extracted_text = []

        for i, image in enumerate(images):
            print (F"Processing page {i+1}...")
            # Preprocess the image before OCR
            processed_image = preprocess_image(image)
            
            # Perform OCR on the processed image
            text = pytesseract.image_to_string(processed_image, lang=language)
            extracted_text.append(text)

            image.close()
            os.remove(os.path.join(tempdir, image.filename))

        with open(output_text_file, 'w', encoding='utf-8') as f:
            for i, text in enumerate(extracted_text):
                f.write(f"Text from page {i + 1}:\n")
                f.write(text)
                f.write("\n\n")
                print("Ok")
# Convert PDF to a list of image

class TextProcessor:
    @staticmethod
    def clean_text(text):
        # if isinstance(text, dict):
        # print(text['ldek'])
        # Normalize text to remove accents and special characters
        normalize_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        print ("Normalize")
        # print(normalize_text)
        text = normalize_text.lower()  # Convert to lowercase
        print ("Lower")
        
        # text = text.translate(str.maketrans('','', string.punctuation))  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Remove spaces
        print(type(text.strip()))
        return text.strip()
        # return normalize_text

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
            # print(text)
    return text

def extract_chapters(self, text):
    """Extract chapters and their contents from the text."""
    chapters = {}
    # Assuming chapters are formatted like "Rozdział X" where X is a number
    pattern = re.compile(r'Rozdział \d+\s(.*?)\s(?=Rozdział \d+|$)', re.DOTALL)
    matches = re.finditer(pattern, text)

    for match in matches:
        chapter_title = match.group(0).strip()
        chapter_content = match.group(1).strip()
        chapters[chapter_title] = chapter_content
        print(f"============={chapter_title}")
        print(f"{chapter_content}")


    return chapters
    

if __name__ == "__main__":
    # pdf_to_speech = PDFToSpeech()
    pdf_path = PDF_FILE_PATH
    language = 'pol'

    # PDFTextAndImageExtractor
    with open(pdf_path, 'rb') as f:
        # pdf_stream = io.BytesIO(f.read())
        extractor = PDFTextAndImageExtractor(f)
        print('PDF opened')


    for page_images in extractor.process_pdf():
        print(f"Wydobyto {len(page_images)} obrazów na tej stronie.")



    # text = extract_text_from_pdf(pdf_path)

    # extract = ocr_pdf(pdf_path, language=language)
    # print (extract)





    # images = convert_from_path(pdf_path)
    # for i in images:
    #     print (type(i))
    

    # text = {"srm": f"{extract_text_from_pdf(pdf_path)}"}
    # text = extract_text_from_pdf(pdf_path)
    # clean_text = TextProcessor.clean_text(text)
    # part_txt = extract_chapters(clean_text)
    # print (part_txt)

    # print(clean_text)
    # print (text['ldek'])
    # cleaned_text = TextProcessor.clean_text(text)
    # print (cleaned_text)
    # output_path = OUTPUT_FILE_PATH
    # vits_tts = VitsTTS()
    # vits_tts.text_to_speech(text, 2000)