"""
DEPENDECIES
!pip uninstall -y torch torchvision
!pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
!pip install git+https://github.com/xinntao/Real-ESRGAN.git
!pip install basicsr==1.4.2
!pip install facexlib gfpgan
!git clone https://github.com/Sz0gun/learn-2-learn.git

"""

import torch
import psutil
from realesrgan import RealESRGANer
from PIL import Image
import numpy as np
import time
import os
import matplotlib.pyplot as plt

class RealESRGANProcessor:
    def __init__(self, model_path, device='cuda', scale=4, dni_weight=0.8):
        """Initialize the RealESRGANProcessor class"""
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")

        # Monitor resources before model initialization
        self.monitor_resources("Before model initialization")

        # Load the RealESRGAN model
        self.model = RealESRGANer(
            scale=scale, 
            model_path=model_path, 
            dni_weight=dni_weight, 
            device=self.device
        )
        self.model.load_weights()
        self.model.to(self.device)

        # Monitor resources after model initialization
        self.monitor_resources("After model initialization")
        print("RealESRGAN model loaded and ready!")

    def monitor_resources(self, message):
        """Function to monitor system resources"""
        memory = psutil.virtual_memory()
        print(f"=== Resource Monitoring ({message}) ===")
        print(f"Total RAM: {memory.total / (1024 ** 3):.2f} GB")
        print(f"Available RAM: {memory.available / (1024 ** 3):.2f} GB")
        print(f"Used RAM: {memory.used / (1024 ** 3):.2f} GB")
        print(f"Memory usage percentage: {memory.percent}%")
        if torch.cuda.is_available():
            print(f"GPU memory usage: {torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB")
            print(f"Available GPU memory: {torch.cuda.memory_reserved() / (1024 ** 3):.2f} GB")

    def pre_process_image(self, image_path):
        """Method for preprocessing the input image before inference"""
        print("Preprocessing input image...")
        self.monitor_resources("Before image preprocessing")
        
        image = Image.open(image_path).convert('RGB')
        image = np.array(image)
        
        # Convert to tensor
        image_tensor = torch.from_numpy(image).float() / 255.0
        image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)  # Change dimensions to (1, C, H, W)
        image_tensor = image_tensor.to(self.device)

        self.monitor_resources("After image preprocessing")
        return image_tensor

    def run_inference(self, image_tensor):
        """Perform inference on the image using the model"""
        print("Running model inference...")
        self.monitor_resources("Before inference")
        
        start_time = time.time()
        with torch.no_grad():
            sr_image = self.model.enhance(image_tensor)
        
        end_time = time.time()
        print(f"Inference completed in {end_time - start_time:.2f} seconds.")
        self.monitor_resources("After inference")
        
        return sr_image

    def post_process_image(self, sr_image):
        """Return the processed image after inference"""
        print("Post-processing the result image...")
        self.monitor_resources("Before post-processing result image")

        # Convert tensor to image
        sr_image = sr_image.squeeze().permute(1, 2, 0).cpu().numpy() * 255.0
        sr_image = sr_image.clip(0, 255).astype(np.uint8)
        sr_image = Image.fromarray(sr_image)

        self.monitor_resources("After post-processing the image")
        return sr_image

    def save_image(self, sr_image, output_path):
        """Manually save the result image to disk"""
        sr_image.save(output_path)
        print(f"Image saved as: {output_path}")
        self.monitor_resources("After saving the image")

    def display_image(self, sr_image):
        """Manually display the result image"""
        plt.imshow(sr_image)
        plt.axis('off')  # Turn off axes for clean display
        plt.show()
        print("Image has been displayed.")

    def process_image(self, image_path):
        """Complete pipeline: preprocess, run inference, and post-process image"""
        print("Starting the complete image processing pipeline...")

        # Step 1: Pre-process the image
        image_tensor = self.pre_process_image(image_path)
        
        # Step 2: Run inference
        sr_image = self.run_inference(image_tensor)

        # Step 3: Post-process the image
        processed_image = self.post_process_image(sr_image)

        return processed_image





