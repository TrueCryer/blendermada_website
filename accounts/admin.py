from django.contrib import admin

from .models import RegistrationProfile, ApiKey


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = 'Activate users'

    def resend_activation_email(self, request, queryset):
        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email()
    resend_activation_email.short_description = 'Re-send activation emails'


admin.site.register(RegistrationProfile, RegistrationAdmin)
admin.site.register(ApiKey)
