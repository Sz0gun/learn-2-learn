import torch
import os
from realesrgan import RealESRGANer
import sys
import io
import zipfile
import pickle


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MODEL_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles', 'real_esergan')


# Custom unpickler to handle 'persistent_load'
class CPU_Unpickler(pickle.Unpickler):
    def persistent_load(self, pid):
        if isinstance(pid, tuple) and pid[0] == 'storage':
            storage_type = getattr(torch, pid[1].__name__)  # Get storage class from torch
            
            # Ensure the third element (size) is an integer
            if isinstance(pid[2], str):  # Check if it is a string
                size = int(pid[2])  # Convert to integer if necessary
            else:
                size = pid[2]  # Otherwise, keep it as is

            storage = storage_type._new_shared(size)  # Create new shared storage
            return storage
        else:
            print(f"Handling persistent load: {pid}")
            return super().persistent_load(pid)



def get_esrgan_model():
    """Function to load, extract, and return the ESRGAN model."""

    # Define the device (CPU or GPU)
    if not torch.cuda.is_available():
        model_device = 'cpu'
        print("CPU is available. Using CPU for processing.")
    else:
        model_device = 'cuda'
        print("GPU is available. Using GPU for processing.")

    # List all files in the folder
    try:
        files_in_folder = os.listdir(MODEL_FILE_PATH)
        print("Files in the folder:", files_in_folder)
    except FileNotFoundError as e:
        print(f"Extracted model folder not found: {e}")
        return None, None

    # Initialize variables to store file paths
    pth_file = None
    pkl_file = None

    # Find the .pth and .pkl files in the folder
    for file_name in files_in_folder:
        if file_name.endswith('.pth'):
            pth_file = os.path.join(MODEL_FILE_PATH, file_name)
            print(f"Found model file (pth): {pth_file}")
        elif file_name.endswith('.pkl'):
            pkl_file = os.path.join(MODEL_FILE_PATH, file_name)
            print(f"Found pickle file (pkl): {pkl_file}")

    try:
        model_file_path = pkl_file if pkl_file else pth_file

        if pkl_file:  # Use the custom unpickler if it's a pickle file
            with open(model_file_path, 'rb') as f:
                loadnet = CPU_Unpickler(f).load()
        else:
            loadnet = torch.load(model_file_path, map_location=torch.device(model_device))

        print(f"Successfully loaded model from: {model_file_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

    # Initialize and load the model weights
    try:
        model = RealESRGANer(
            scale=4,  # Correct scale for the model
            model_path=None,  # Not needed since weights are loaded manually
            dni_weight=0.8,
            device=model_device
        )
        print("ESERGANER")
        # Load the state dictionary into the model
        if 'params_ema' in loadnet:
            model.load_state_dict(loadnet['params_ema'], strict=False)
            print("Model state dict loaded successfully!")
        else:
            print("Key 'params_ema' not found in the loaded model.")
            return None, None

        model.half()  # Use half precision if supported
        model = model.to(model_device)
        print("ESRGAN model loaded and ready!")
        return model, model_device

    except Exception as e:
        print(f"Error initializing or loading the model: {e}")
        return None, None

# Call the function to get the model
get_result = get_esrgan_model()
print(get_result)


