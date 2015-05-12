from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Statistic, Vote


@receiver(post_save, sender=Statistic)
def update_downloads(sender, **kwargs):
    kwargs.get('instance').material.update_downloads()


@receiver(post_save, sender=Vote)
def update_rating(sender, **kwargs):
    kwargs.get('instance').material.update_rating()
