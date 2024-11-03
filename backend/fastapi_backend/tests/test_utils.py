# backend/fastapi_backend/tests/test_utils.py
import pytest
import sys
import os

# Ensure the correct paths are added to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../common_components')))

# Now, try importing again
from common_components.utils.some_utils import some_function
from webenv.routers import github  # Use relative import based on your directory structure

def test_some_function():
    result = some_function()
    expected_value = "some_expected_value"
    assert result == expected_value
