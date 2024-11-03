# backend/fastapi_backend/tests/conftest.py
import sys
import os

def add_to_sys_path(relative_path):
    absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))
    if absolute_path not in sys.path:
        sys.path.insert(0, absolute_path)
        print(f"Added to sys.path: {absolute_path}")

# Adjust paths to make sure they are correct
add_to_sys_path('..')  # Points to fastapi_backend
add_to_sys_path('../../common_components')  # Points to common_components
add_to_sys_path('../webenv')  # Points to webenv folder
add_to_sys_path('../gameenv')  # Points to gameenv folder

print("Current sys.path:")
for path in sys.path:
    print(path)
