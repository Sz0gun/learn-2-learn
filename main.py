import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # Set the default settings module for the 'django' program.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    try:
        # Execute the command line utility for the project
        execute_from_command_line(sys.argv)
    except Exception as exc:
        # Handle any exceptions that may occur
        raise SystemExit(f"Error occurred while running the Django application: {exc}")
