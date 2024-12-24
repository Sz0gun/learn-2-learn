import os
import sys

def main():
    """Entry point for Django's manage.py."""
    django_env = os.getenv('DJANGO_ENV', 'dev').lower()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{django_env}')
    
    if os.environ.get('RUN_MAIN') != 'true':
        print(f"Using Django environment: {django_env} (DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']})")

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Error starting Django: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()