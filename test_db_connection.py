import os
import django
from django.db import connection
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        one = cursor.fetchone()[0]
        print(f"Database connected: {one}")
except Exception as e:
    print(f"Error connecting to the database: {e}")
