#!/usr/bin/env python
import os
import sys

def main():
    """Główna funkcja zarządzania Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nie można zaimportować Django. Upewnij się, że jest zainstalowane i "
            "dostępne w Twoim PYTHONPATH oraz że aktywowałeś środowisko wirtualne."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
