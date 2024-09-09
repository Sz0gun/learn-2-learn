import os
import PyPDF2
import re
import torch
import psutil
import tempfile
import time
import torch
import functools
import io
import cv2
import gc
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
import pytesseract
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path, convert_from_bytes
from torchvision.transforms.functional import rgb_to_grayscale
from PIL import Image, ImageEnhance, ImageFilter
from realesrgan import RealESRGANer
from memory_profiler import profile  # Profilowanie pamięci

from torch import nn



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'BOOK.pdf')

OUTPUT_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'SRM_1.wav')

ESRGAN_MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'ESRGAN_SRx4_official.pth')




class ResidualDenseBlock(nn.Module):
    def __init__(self, num_feat=64, num_grow_ch=32):
        super(ResidualDenseBlock, self).__init__()
        self.conv1 = nn.Conv2d(num_feat, num_grow_ch, 3, 1, 1)
        self.conv2 = nn.Conv2d(num_feat + num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv3 = nn.Conv2d(num_feat + 2 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv4 = nn.Conv2d(num_feat + 3 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv5 = nn.Conv2d(num_feat + 4 * num_grow_ch, num_feat, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, num_feat, num_grow_ch=32):
        super(RRDB, self).__init__()
        self.rdb1 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb2 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb3 = ResidualDenseBlock(num_feat, num_grow_ch)

    def forward(self, x):
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)
        return out * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(self, num_in_ch, num_out_ch, num_feat, num_block, num_grow_ch=32, scale=4):
        super(RRDBNet, self).__init__()
        self.scale = scale
        self.conv_first = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1)
        self.RRDB_trunk = nn.Sequential(*[RRDB(num_feat, num_grow_ch) for _ in range(num_block)])
        self.trunk_conv = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.upconv1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.upconv2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_last = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)

        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        feat = self.conv_first(x)
        trunk = self.trunk_conv(self.RRDB_trunk(feat))
        feat = feat + trunk

        feat = self.lrelu(self.upconv1(torch.nn.functional.interpolate(feat, scale_factor=2, mode='nearest')))
        feat = self.lrelu(self.upconv2(torch.nn.functional.interpolate(feat, scale_factor=2, mode='nearest')))
        out = self.conv_last(feat)
        return out


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def print_memory_usage():
    if torch.cuda.is_available():
        print(f"CUDA Memory Usage: {torch.cuda.memory_allocated() / 1024 ** 2:.2f} MB")
    else:
        print("Memory usage check only works with CUDA")


class PDFImageExtractor:
    
    def __init__(self, pdf_stream, tesseract_lang='eng', model_path=ESRGAN_MODEL_PATH):
        print("Initializing PDFImageExtractor...")

        if not isinstance(pdf_stream, io.BytesIO):
            raise TypeError("PDF stream must be of type io.BytesIO")

        try:
            self.pdf_stream = pdf_stream.read()
            print(f"PDF stream size: {len(self.pdf_stream)} bytes")
        except Exception as e:
            raise Exception(f"Error reading PDF stream: {e}")

        self.tesseract_lang = tesseract_lang

        if torch.cuda.is_available():
            try:
                self.device = torch.device('cuda')
                print("Using CUDA GPU")
            except RuntimeError as e:
                print(f"Error with CUDA: {e}. Falling back to CPU.")
                self.device = torch.device('cpu')
        elif torch.backends.mps.is_available():
            try:
                self.device = torch.device('mps')
                print("Using Apple MPS (Metal Performance Shaders)")
            except RuntimeError as e:
                print(f"Error with MPS: {e}. Falling back to CPU.")
                self.device = torch.device('cpu')
        else:
            self.device = torch.device('cpu')
            print("Using CPU")

        self.model_path = model_path
        self.model = self.load_esrgan_model(self.model_path)
        if self.model is None:
            print("Failed to load the model.")
        else:
            print("Model loaded successfully.")
        print_memory_usage()

        self.stop_processing = False
        print("Initialization complete.")
        print_memory_usage()

    def load_esrgan_model(self, model_path):
        try:
            if not os.path.exists(model_path):
                print(f"Model file not found: {model_path}. Please check the path.")
                return None

            print(f"Loading model from: {model_path}")
            loadnet = torch.load(model_path, map_location=torch.device('cpu'))
            if 'params' in loadnet:
                model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
                model.load_state_dict(loadnet['params'], strict=False)
                model.half()  # For faster computations
                model = model.to(self.device)
                print("Model załadowany pomyślnie!")
                return model
            else:
                print("Klucz 'params' nie został znaleziony w modelu.")
                return None
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def display_image(self, image):
        try:
            cv2.imshow("Processed Image", image)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()

            if key == ord('n'):
                self.stop_processing = True
                print("Processing stopped by user.")
        except Exception as e:
            print(f"Error displaying image: {e}")

    @timing_decorator
    def apply_super_resolution(self, image):
        try:
            if self.model is None:
                print("Error: No model loaded. Skipping super resolution.")
                return image

            print("Applying super resolution...")
            self.model = self.model.to(self.device)
            image_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).half().to(self.device)

            with torch.no_grad():
                enhanced_image_tensor = self.model(image_tensor).squeeze(0).permute(1, 2, 0).cpu().numpy()

            enhanced_image = (enhanced_image_tensor * 255).astype(np.uint8)

            del image_tensor, enhanced_image_tensor
            gc.collect()
            print_memory_usage()

            self.model = self.model.to('cpu')
            print("Super resolution applied successfully.")
            return enhanced_image
        except Exception as e:
            print(f"Error applying super resolution: {e}")
            return image

    @timing_decorator
    def process_pdf(self, start_page=0, end_page=None):
        try:
            pdf_reader = PdfReader(io.BytesIO(self.pdf_stream))
            total_pages = len(pdf_reader.pages)

            if end_page is None or end_page > total_pages:
                end_page = total_pages

            if start_page >= end_page:
                raise ValueError("Start page must be less than end page.")

            print(f"Processing PDF from page {start_page} to {end_page} (total: {end_page - start_page})")

            for batch_start in range(start_page, end_page):
                print(f"Processing page {batch_start}...")
                for image_cv in self.extract_images(batch_start, batch_start + 1):
                    enhanced_image = self.process_patches(image_cv, patch_size=32)
                    self.display_image(enhanced_image)
                    if self.stop_processing:
                        break
                gc.collect()
                print_memory_usage()
                if self.stop_processing:
                    break
        except Exception as e:
            print(f"Error processing PDF: {e}")
            raise

    def extract_images(self, start_page=0, end_page=None):
        try:
            print("Extracting images from PDF...")
            pdf_reader = PdfReader(io.BytesIO(self.pdf_stream))
            total_pages = len(pdf_reader.pages)

            for page_number in range(start_page, min(end_page, total_pages)):
                print(f"Processing page {page_number + 1}...")
                page = pdf_reader.pages[page_number]
                with io.BytesIO() as output_stream:
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(page)
                    pdf_writer.write(output_stream)
                    page_bytes = output_stream.getvalue()

                images = convert_from_bytes(page_bytes)
                for image in images:
                    open_cv_image = np.array(image)
                    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

                    enhanced_image = self.apply_super_resolution(open_cv_image)
                    yield enhanced_image
                    print_memory_usage()
                    if self.stop_processing:
                        return
        except Exception as e:
            print(f"Error extracting images: {e}")
            raise

    @timing_decorator
    def process_patches(self, image, patch_size=128):
        try:
            if self.model is None:
                print("Error: No model loaded. Skipping patch processing.")
                return image

            print(f"Processing image in patches (size: {patch_size}x{patch_size})...")
            h, w, _ = image.shape
            enhanced_image = np.zeros_like(image)

            for i in range(0, h, patch_size):
                for j in range(0, w, patch_size):
                    patch = image[i:i + patch_size, j:j + patch_size]
                    patch_tensor = torch.from_numpy(patch).permute(2, 0, 1).unsqueeze(0).half().to(self.device)

                    with torch.no_grad():
                        enhanced_patch_tensor = self.model(patch_tensor).squeeze(0).permute(1, 2, 0).cpu().numpy()

                    enhanced_image[i:i + patch_size, j:j + patch_size] = (enhanced_patch_tensor * 255).astype(np.uint8)

                    del patch_tensor, enhanced_patch_tensor
                    torch.cuda.empty_cache()
                    gc.collect()
                    print_memory_usage()
                    if self.stop_processing:
                        break

            print("Patches processed successfully.")
            return enhanced_image
        except Exception as e:
            print(f"Error processing patches: {e}")
            return image

    # def smooth_image(self, image):
        """
        Applies smoothing to the image using Gaussian Blur and Median Blur.
        This helps in reducing noise and preparing the image for noise removal.
        """
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(image, (1, 1), 0)
        smoothed_image = cv2.medianBlur(gaussian_blur, 1)
        return smoothed_image

    # def enhance_image(self, image):
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

    # def detect_and_expand_contours(self, image, page_number, margin_step=50, max_margin=500, initial_margin=150):
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

    # def remove_text_and_get_image_coords(self, image, page_number):
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

    # def check_model_file(self, model_path):
        """ Sprawdza, czy plik modelu zawiera odpowiednie klucze """
        try:
            model_data = torch.load(model_path, map_location=torch.device('cpu'))
            
            # Sprawdzenie, czy załadowany obiekt to słownik
            if isinstance(model_data, dict):
                print(f"Klucze w modelu: {model_data.keys()}")
                
                # Sprawdzenie, czy model zawiera klucz 'params_ema'
                if 'params_ema' in model_data:
                    print("Model zawiera 'params_ema'. Jest to prawidłowy klucz wag modelu.")
                    return True
                else:
                    print("Model nie zawiera klucza 'params_ema'.")
                    return False
            else:
                print("Plik modelu nie jest słownikiem.")
                return False
        except Exception as e:
            print(f"Błąd podczas ładowania pliku modelu: {e}")
            return False





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
    language = 'eng'

    # PDFTextAndImageExtractor
    with open(pdf_path, 'rb') as pdf_stream:
        content = pdf_stream.read()  # Odczytaj zawartość pliku
        print(f"Read PDF content: {type(content)}, size: {len(content)} bytes")  # Dodajmy informację o rozmiarze i typie
        extractor = PDFImageExtractor(io.BytesIO(content))  # Upewnij się, że strumień jest przekazany jako bytes
        extractor.process_pdf(start_page=1, end_page=50)


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