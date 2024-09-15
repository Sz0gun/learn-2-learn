"""
DEPENDECIES
!pip uninstall -y torch torchvision
!pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
!pip install git+https://github.com/xinntao/Real-ESRGAN.git
!pip install basicsr==1.4.2
!pip install facexlib gfpgan
!pip install pdf2image
!apt-get install poppler-utils
!git clone https://github.com/Sz0gun/learn-2-learn.git

"""

from pdf2image import convert_from_path
from PIL import Image
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
    def __init__(self, model_path, device='cuda', scale=4, dni_weight=0.8):
        """Initialize the RealESRGANProcessor class"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")

        # Monitor resources before model initialization
        self.monitor_resources("Before model initialization")
        try:
            # Load the RealESRGAN model
            self.model = RealESRGANer(
                scale=scale, 
                model_path=model_path, 
                dni_weight=dni_weight, 
                device=self.device
            )
            self.model.load_weights()
            self.model.to(self.device)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise e

        # Monitor resources after model initialization
        self.monitor_resources("After model initialization")
        print("RealESRGAN model loaded and ready!")

    def monitor_resources(self, message):
        """Function to monitor system resources"""
        memory = psutil.virtual_memory()
        log_message = f"=== Resource Monitoring ({message}) ===\n"
        log_message += f"Total RAM: {memory.total / (1024 ** 3):.2f} GB\n"
        log_message += f"Available RAM: {memory.available / (1024 ** 3):.2f} GB\n"
        log_message += f"Used RAM: {memory.used / (1024 ** 3):.2f} GB\n"
        log_message += f"Memory usage percentage: {memory.percent}%\n"
        
        if torch.cuda.is_available():
            log_message += f"GPU memory usage: {torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB\n"
            log_message += f"Available GPU memory: {torch.cuda.memory_reserved() / (1024 ** 3):.2f} GB\n"
        
        logging.info(log_message)

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

    def process_image(self, image):
        """
        Process a single image, enhance it using ESRGAN, and return the enhanced image.

        Parameters:
        - image (PIL.image): The input image to be processed.

        Returns:
        - Enhanced image (PIL.Image) in-memory.
        """
        print(f"Processing a single image...")

        try:
            # Pre-process the image
            image_tensor = self.pre_process_image(image)

            # Run inference
            processed_image = self.run_inference(image_tensor)

            # Post-process the result
            enhanced_image = self.post_process_image(processed_image)

            return enhanced_iamge # Return in-memory image

        except Exception as e:
            logging.error(f"Error processing image: {e}")
            raise e
            
    async def process_pdf(self, pdf_path, output_dir, start_page=1, end_page=None, dpi=150):
        """
        Process each page of a PDF as an image and enhance it using ESRGAN.

        Parameters:
        - pdf_path (str): Path to the input PDF file.
        - start_page (int): The first page to process (1-based index).
        - end_page (int or None): The last page to process. If None, process to the end of the PDF.
        - dpi (int): The resolution of the converted images (default is 150).

        Returns:
        - List of enhanced images (PIL.Image) in-memory.
        """
        print(f"Processing PDF: {pdf_path} from page {start_page} to {end_page if end_page else 'last'}")
        # Convert the specified range of PDF pages to images
        try:
            images = convert_from_path(pdf_path, dpi=dpi, first_page=start_page, last_page=end_page)
            print(f"PDF conversion completed. {len(images)} pages processed.")
        except Exception as e:
            logging.error(f"Error converting PDF to images: {e}")
            raise e

        enhanced_images = []

        # Process each image (each page in the range)
        for idx, image in enumerate(images, start=start_page):
            try:
                # Convert PIL image to the tensor for ESRGAN processing
                image_tensor = self.pre_process_image(image)

                # Process the image using the existing pipeline
                print(f"Processing page {idx}...")
                processed_image = self.run_inference(image_tensor)

                # Post-process the image and keep it in-memory
                enhanced_image = self.post_process_image(processed_image)

                # Append the enhanced image to the list
            except Exception as e:
                logging.error(f"Error processing page {idx}: {e}")
        
        return enhanced_images # Return list of in-memory enhanced images

    def save_image(self, sr_image, output_path):
        """Save the result image to disk"""
        try:
            sr_image.save(output_path)
            print(f"Image saved as: {output_path}")
            self.monitor_resources("After saving the image")
        except Exception as e:
            logging.error(f"Error saving the image: {e}")
            raise e

    def display_image(self, sr_image):
        """Display the result image"""
        plt.imshow(sr_image)
        plt.axis('off')  # Turn off axes for clean display
        plt.show()
        print("Image has been displayed.")




