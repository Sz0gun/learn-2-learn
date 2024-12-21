import os
import sys

def main():
    """Entry point for Django's manage.py."""
    # Ustawienie DJANGO_SETTINGS_MODULE na podstawie DJANGO_ENV
    django_env = os.getenv('DJANGO_ENV', 'prod').lower()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{django_env}')
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Error starting Django: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()