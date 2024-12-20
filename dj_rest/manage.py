# dj_rest/manage.py

import os
import sys

def main():
    """Główna funkcja zarządzania Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
                            "Cannot import Django. Please make sure it is installed and "
                            "available in your PYTHONPATH and that you have activated the virtual environment."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
