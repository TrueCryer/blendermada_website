from django.apps import AppConfig
from django.db.models.signals import post_save

from .receivers import update_downloads, update_rating


class MaterialsConfig(AppConfig):
    name = 'materials'

    def ready(self):
        post_save.connect(update_downloads, sender='materials.Statistic')
        post_save.connect(update_rating,    sender='materials.Vote')
