from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorites')
    material = models.ForeignKey('materials.Material', related_name='favorites')
    date = models.DateTimeField('Date', auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.material)
