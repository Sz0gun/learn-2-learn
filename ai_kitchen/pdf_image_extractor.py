import os
import torch
import gc
import asyncio
import concurrent.futures
from PIL import Image
import numpy as np
from google.colab import drive
from ESRGAN_Model_Colab import get_esrgan_model
from pdf2image import convert_from_path

drive.mount('/content/drive')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")


PDF_FILE_PATH = '/content/drive/MyDrive/BOOK.pdf'

class ImageEnhancerESRGAN:
    def __init__(self):
        # Load the ESRGAN model and device from the function in the notebook
        self.esrganer, self.device = get_esrgan_model()

    async def enhance_image(self, image):
        """
        Takes a PIL image object and returns the enhanced image asynchronously.
        """

        if self.esrganer is None:
            print (f"Model is not loaded. Enhancement skipped")
            return image

        image = image.convert('RGB')
        img_tensor = torch.from_numpy(np.array(image)).float().permute(2, 0, 1).unsqueeze(0).to(self.device)

        # ESRGAN enhancement
        try:
            with torch.no_grad():
                enhanced_tensor = self.esrganer.enhance(img_tensor)
            enhanced_image = Image.fromarray(enhanced_tensor.squeeze().cpu().numpy().astype('uint8'))
            return enhanced_image
        except Exception as e:
            print (f"Error during enhancement: {e}")
            return image
    
    def clear_gpu_memory(self):
        gc.collect()
        torch.cuda.empty_cache()


class ProcessPDF:

    """

    """

    def __init__(self, pdf_file_path, batch_size=4, dpi=150):
        self.pdf_file_path = pdf_file_path
        self.enhancer = ImageEnhancerESRGAN()
        self.batch_size = batch_size 
        self.dpi = dpi

    async def process_pdf(self, start_page=0, end_page=None):
        """Extracts and enhances images from PDF asynchronously."""

        try:
            # Convert PDF to images using pdf2image with reduced DPI for speed
            images = convert_from_path(self.pdf_file_path, dpi=self.dpi, first_page=start_page, last_page=end_page)
            enhanced_images = []

            # Use async and concurrent processing to enhance image
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                tasks = [
                    loop.run_in_executor(pool, self._process_batch, images[i:i + self.batch_size])
                    for i in range (0, len(images), self.batch_size)
                ]
                results = await asyncio.gather(*tasks)

                # Clear GPU memory after each batch
                for enhanced_batch in results:
                    enhanced_image.extend(enhanced_batch)
                    self.enhancer.clear_gpu_memory()
                
            return enhanced_images
        except Exception as e:
            print (f"Error processing PDF: {e}")
            return []

    def _process_batch(self, batch):
        """Enhances a batch of image synchronously"""
        enhanced_images = []

        for img in batch:
            enhanced_img = asyncio.run(self.enhancer.enhance_image(img))
            enhanced_images.append((img, enhanced_img))
        return enhanced_images

    def display_comparison(self, enhanced_images):
        import matplotlib.pyplot as plt

        for original, enhanced in enhanced_images:
        
            plt.subplot(1, 2, 1)
            plt.title("Original Image")
            plt.imshow(original)
            plt.axis('off')

            plt.suplot(1, 2, 2)
            plt.title("Enhanced Image")
            plt.imshow(enhanced)
            plt.axis('off')

            plt.show()


async def main():
    pdf_processor = ProcessPDF(PDF_FILE_PATH)
    enhanced_images = await pdf_processor.process_pdf(start_page=1, end_page=5)
    pdf_processor.display_comparison(enhanced_images)
if __name__ == "__main__":
    asyncio.run(main())