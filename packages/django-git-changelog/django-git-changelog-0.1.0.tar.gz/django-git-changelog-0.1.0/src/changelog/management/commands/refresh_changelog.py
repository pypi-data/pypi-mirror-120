from django.core.management.base import BaseCommand, CommandError
from changelog.models import Changelog


class Command(BaseCommand):
    help = 'Refresh all Git entries in the Django Changelog Database'

    def handle(self, *args, **options):
        Changelog.run_actions()
