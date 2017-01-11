from django.apps import AppConfig
from django.db.models.signals import pre_delete

from .receivers import remove_uploaded_files, remove_scene_files


class UploadsConfig(AppConfig):
    name = 'uploads'

    def ready(self):
        pre_delete.connect(remove_uploaded_files, sender='uploads.Upload')
        pre_delete.connect(remove_scene_files,    sender='uploads.Scene')
