from os import path

from django.conf import settings


UPLOADS_STORAGE_PATH = getattr(settings, 'UPLOADS_STORAGE_PATH', path.join(settings.MEDIA_ROOT, 'uploads'))

UPLOADS_SECRET_KEY = getattr(settings, 'UPLOADS_SECRET_KEY', 'secret')
