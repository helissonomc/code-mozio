"""
This command will make django wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Wait for database to be available"""

    def handle(self, *args, **options):
        """ Entrypoint for command. """
        self.stdout.write('Waiting for database...')
        db_conn = False
        while not db_conn:
            try:
                self.check(databases=['default'])
                db_conn = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
