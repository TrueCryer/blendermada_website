from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ...models import RegistrationProfile


class Command(BaseCommand):
    help = 'Delete expired user registrations from the database'

    def handle(self, **options):
        RegistrationProfile.objects.delete_expired_users()
