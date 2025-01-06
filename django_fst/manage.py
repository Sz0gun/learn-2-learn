#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')  # Zmień 'core.settings' na ścieżkę do Twoich ustawień, jeśli różni się od domyślnej.
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# import os
# import sys

# def main():
#     """Entry point for Django's manage.py."""
#     django_env = os.getenv('DJANGO_ENV', 'dev').lower()
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{django_env}')
    
#     if os.environ.get('RUN_MAIN') != 'true':
#         print(f"Using Django environment: {django_env} (DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']})")

#     try:
#         from django.core.management import execute_from_command_line
#         execute_from_command_line(sys.argv)
#     except Exception as e:
#         print(f"Error starting Django: {e}")
#         sys.exit(1)

# if __name__ == '__main__':
#     main()