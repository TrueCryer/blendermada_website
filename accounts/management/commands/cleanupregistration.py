from django.core.management.base import BaseCommand

from ...models import RegistrationProfile


class Command(BaseCommand):
    help = 'Delete expired users and registrations from the database'

    def handle(self, **options):
        RegistrationProfile.objects.delete_expired_users()
