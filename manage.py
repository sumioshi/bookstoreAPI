#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import locale
import django

print("Default encoding:", sys.getdefaultencoding())
print("Locale preferred encoding:", locale.getpreferredencoding())

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
    django.setup()

    # Adicione logs para verificar as variáveis de ambiente
    print(f"SQL_ENGINE: {os.getenv('SQL_ENGINE')}")
    print(f"SQL_DATABASE: {os.getenv('SQL_DATABASE')}")
    print(f"SQL_USER: {os.getenv('SQL_USER')}")
    print(f"SQL_PASSWORD: {os.getenv('SQL_PASSWORD')}")
    print(f"SQL_HOST: {os.getenv('SQL_HOST')}")
    print(f"SQL_PORT: {os.getenv('SQL_PORT')}")

    # Tentativa de conexão com o banco de dados
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()[0]
            print(f"Database connected: {one}")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
