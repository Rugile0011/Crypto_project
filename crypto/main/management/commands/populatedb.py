from django.core.management.base import BaseCommand
from main.scripts import run_script
import subprocess


class Command(BaseCommand):
    def add_arguments(self, parser):
        """   """
        parser.add_argument('symbol', type=str)
        parser.add_argument('market', type=str)

    def handle(self, **options):
        """   """

    run_script(options['symbol'], options['market'])
