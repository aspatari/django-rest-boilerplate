from django.conf import settings
from django.db import ProgrammingError
from django.db.backends.postgresql.base import DatabaseWrapper


def database_init_signal(signal, sender: DatabaseWrapper, connection: DatabaseWrapper, **kwargs):
    """ On database connection create Database """
    database_name: str = f"{settings.DATABASES['default']['NAME']}"

    cursor = connection.cursor()

    try:
        cursor.execute(f'CREATE DATABASE "{database_name}"')
    except ProgrammingError:
        print("Database already exist")
