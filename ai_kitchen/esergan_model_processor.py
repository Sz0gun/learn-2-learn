"""
DEPENDECIES
!pip uninstall -y torch torchvision
!pip install torch==2.0.1 torchvision==0.15.2
!pip install git+https://github.com/xinntao/Real-ESRGAN.git
!pip install basicsr==1.4.2
!pip install facexlib gfpgan
!pip install pdf2image
!apt-get install poppler-utils
!git clone https://github.com/Sz0gun/learn-2-learn.git

"""

from pdf2image import convert_from_path
from PIL import Image
from realesrgan import RealESRGANer
import matplotlib.pyplot as plt
import numpy as np
import torch
import time
import os
import psutil
import logging

# Logging configuration
logging.basicConfig(filenames='resource_monitor.log', level=logging.INFO)

class RealESRGANProcessor:
    def __init__(self, bucket_name='m0dels_ai', model_blob_name='RealESRGAN_x4plus.pth', device='cuda', scale=4, dni_weight=0.8):
        """
        Initializes the RealESRGANProcessor class, downloads the model from GCS, and prepares it for use.
        """
        self.device = device
        self.model_path = f"{os.getcwd()}/{model_blob_name}"
        
        # Pobieramy model z GCS
        gcs_service = GCPService()
        gcs_service.download_file(bucket_name, model_blob_name, self.model_path)

        # Inicjalizacja modelu Real-ESRGAN
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        # Monitor resources before model initialization
        self.monitor_resources("Before model initialization")
        try:
            self.model = RealESRGANer(scale=scale, dni_weight=dni_weight, device=self.device)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise e

        # Monitor resources after model initialization
        self.monitor_resources("After model initialization")
        print("RealESRGAN model loaded and ready!")

    def enhance_image(self, image):
        """
        Enhances the input image using the Real-ESRGAN model.
        This method includes all the necessary steps: preprocessing, inference, and post-processing.

        :param image: PIL image to be enhanced.
        :return: Enhanced PIL image.
        """
        image_tensor = self.pre_process_image(image)
        processed_image = self.run_inference(image_tensor)
        enhanced_image = self.post_process_image(processed_image)
        return enhanced_image

    def pre_process_image(self, image_path):
        """Method for preprocessing the input image before inference"""
        print("Preprocessing input image...")
        self.monitor_resources("Before image preprocessing")

        try:        
            image = Image.open(image_path).convert('RGB')
            image = np.array(image)
            
            # Convert to tensor
            image_tensor = torch.from_numpy(image).float() / 255.0
            image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)  # Change dimensions to (1, C, H, W)
            image_tensor = image_tensor.to(self.device)

            self.monitor_resources("After image preprocessing")
            return image_tensor
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            raise e

    def run_inference(self, image_tensor):
        """Perform inference on the image using the model"""
        print("Running model inference...")
        self.monitor_resources("Before inference")
        try:
            start_time = time.time()
            with torch.no_grad():
                sr_image = self.model.enhance(image_tensor)
            
            end_time = time.time()
            print(f"Inference completed in {end_time - start_time:.2f} seconds.")
            self.monitor_resources("After inference")
            
            return sr_image
        except Exception as e:
            Logging.error(f"Error during interface: {e}")
            raise e

    def post_process_image(self, sr_image):
        """Return the processed image after inference"""
        print("Post-processing the result image...")
        self.monitor_resources("Before post-processing result image")

        try:
            # Convert tensor to image
            sr_image = sr_image.squeeze().permute(1, 2, 0).cpu().numpy() * 255.0
            sr_image = sr_image.clip(0, 255).astype(np.uint8)
            sr_image = Image.fromarray(sr_image)

            self.monitor_resources("After post-processing the image")
            return sr_image
        except Exception as e:
            logging.error(f"Error during post-processing: {e}")
            raise e

    def process_pdf(self, pdf_path, start_page=1, end_page=None, dpi=300):
        """
        Processes a PDF file by converting each page to an image and enhancing the pages using ESRGAN.
        
        :param pdf_path: Path to the PDF file.
        :param start_page: Starting page number to process.
        :param end_page: Last page to process.
        :param dpi: Dots per inch for image conversion.
        :return: List of enhanced PIL images for each page.
        """
        print(f"Processing PDF: {pdf_path} from page {start_page} to {end_page if end_page else 'last'}")
        try:
            images = convert_from_path(pdf_path, dpi=dpi, first_page=start_page, last_page=end_page)
            print(f"PDF conversion completed. {len(images)} pages processed.")
        except Exception as e:
            logging.error(f"Error converting PDF to images: {e}")
            raise e

        enhanced_images = []

        for idx, image in enumerate(images, start=start_page):
            try:
                image_tensor = self.pre_process_image(image)
                print(f"Processing page {idx}...")
                processed_image = self.run_inference(image_tensor)
                enhanced_image = self.post_process_image(processed_image)
                enhanced_images.append(enhanced_image)
            except Exception as e:
                logging.error(f"Error processing page {idx}: {e}")
        
        return enhanced_images

    def save_image(self, sr_image, output_path):
        """
        Saves the enhanced image to the specified file path.
        
        :param sr_image: PIL image to be saved.
        :param output_path: Path where the image will be saved.
        """
        try:
            sr_image.save(output_path)
            print(f"Image saved as: {output_path}")
            self.monitor_resources("After saving the image")
        except Exception as e:
            logging.error(f"Error saving the image: {e}")
            raise e

    def display_image(self, sr_image):
        """
        Displays the enhanced image using Matplotlib.
        
        :param sr_image: PIL image to be displayed.
        """
        plt.imshow(sr_image)
        plt.axis('off')  # Turn off axes for clean display
        plt.show()
        print("Image has been displayed.")

    def monitor_resources(self, message):
        """
        Logs system memory usage at different stages of the image processing pipeline.
        
        :param message: Custom log message to indicate the current stage of processing.
        """
        memory = psutil.virtual_memory()
        log_message = f"=== Resource Monitor: {message} ===\nMemory: {memory.percent}%\n"
        logging.info(log_message)




