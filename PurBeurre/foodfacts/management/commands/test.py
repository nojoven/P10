import os
from django.core.management import BaseCommand


class Command(BaseCommand):
    """This command becomes available from manage.py"""

    help = "Executes project tests."

    def handle(self, *args, **options):
        """This will understand 'test' as 'pytest -v -rf' """
        os.system("pytest -o log_cli=TRUE -v -rf")
