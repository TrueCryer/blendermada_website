from django.contrib import admin

from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'send_notifications', 'send_newsletters')


admin.site.register(UserProfile, ProfileAdmin)
