from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Upload


class Command(BaseCommand):
    help = 'Reset \'rendering\' flat to obsolete uploads'

    def handle(self, *args, **options):
        for upload in Upload.objects.filter(status='r'):
            delta = timezone.now() - upload.render_started
            if delta.seconds > 5*60*60:
                upload.status = 'w'
                upload.save()
