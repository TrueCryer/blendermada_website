from django.contrib import admin

from .models import Mail


class MailAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('mailing_type', 'subject', 'message')
        }),
    )
    actions = ['send_mails']
    def send_mails(self, request, queryset):
        for obj in queryset:
            sended, target = obj.send_mails()
            self.message_user(request, 'Sended {sended} mails from {target}.'.format(sended=sended, target=target))
    send_mails.short_description = "Send selected mails"


admin.site.register(Mail, MailAdmin)
