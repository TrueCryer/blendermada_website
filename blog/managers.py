from django.db.models import Manager


class PublicManager(Manager):
    """Returns published posts."""

    def published(self):
        return self.filter(status='p')
