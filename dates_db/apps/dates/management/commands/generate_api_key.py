from django.core.management.base import BaseCommand, CommandError
from rest_framework_api_key.permissions import APIKey


class Command(BaseCommand):
    help = 'Creates API key.'

    def handle(self, *args, **options):
        api_key, key = APIKey.objects.create_key(name='default')
        self.stdout.write(self.style.SUCCESS(f'Generated API key: {key}'))
