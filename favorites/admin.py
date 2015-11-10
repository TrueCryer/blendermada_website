from __future__ import unicode_literals

from django.contrib import admin

from .models import Favorite


admin.site.register(Favorite)