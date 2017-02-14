from django.core.management.base import BaseCommand

from ...models import Material 


class Command(BaseCommand):
    help = 'Updates downloads field for all materials'

    def handle(self, *args, **options):
        for mat in Material.objects.all():
            try:
                mat.update_downloads()
                message = "%s successfully updated. Number of downloads is %s"
            except:
                message = "%s not updated. Number of downloads is still %s"
            self.stdout.write(message % (mat.name, mat.downloads))
