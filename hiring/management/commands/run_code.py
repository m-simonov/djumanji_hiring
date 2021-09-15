from django.core.management import BaseCommand

import data as mock


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Hello')
