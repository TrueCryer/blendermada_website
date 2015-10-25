from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Upload, Scene


@receiver(pre_delete, sender=Upload)
def clean_uploaded_files(sender, instance, **kwargs):
    instance.uploaded_file.delete()
    instance.storage.delete()
    instance.image.delete()


@receiver(pre_delete, sender=Scene)
def clean_scene_files(sender, instance, **kwargs):
    instance.file.delete()
    instance.image.delete()
    instance.thumb_big.delete()
    instance.thumb_small.delete()
