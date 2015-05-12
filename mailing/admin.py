from django.contrib import admin

from .models import Setting, Mail


class MailAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('setting', 'mailing_type'), 'subject', 'message')
        }),
    )
    actions = ['send_mails']
    def send_mails(self, request, queryset):
        for obj in queryset:
            sended, target = obj.send_mails()
            self.message_user(request, 'Sended {sended} mails from {target}.'.format(sended=sended, target=target))
    send_mails.short_description = "Send selected mails"


class SettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('sender', ('host', 'port'), ('username', 'password'), 'use_ssl', 'use_tls', 'timeout')
        }),
    )


admin.site.register(Mail, MailAdmin)
admin.site.register(Setting, SettingAdmin)
