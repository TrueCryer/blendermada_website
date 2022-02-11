from html2text import html2text

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template import Template


from core.mail import send_mass_html_mail
from materials.models import Material


MAILING_TYPES = (
    ('adm', 'ADMINS'),
    ('mod', 'MODERATORS'),
    ('aut', 'AUTHORS'),
    ('sub', 'SUBSCRIBERS'),
    ('all', 'ALL'),
)


class Mail(models.Model):
    mailing_type = models.CharField(
        'Mailing type', max_length=3, choices=MAILING_TYPES)
    subject = models.CharField('Subject', max_length=255)
    message = models.TextField('Template')

    class Meta:
        verbose_name = 'Mail'
        verbose_name_plural = 'Mails'

    def __str__(self):
        return '{subject} for {type}'.format(subject=self.subject, type=self.get_mailing_type_display())

    def get_recipients(self):
        queryset = get_user_model().objects.filter(is_active=True)
        if self.mailing_type == 'adm':
            queryset = queryset.filter(is_superuser=True)
        elif self.mailing_type == 'mod':
            queryset = queryset.filter(is_staff=True)
        elif self.mailing_type == 'aut':
            queryset = queryset.filter(pk__in=set(
                Material.objects.values_list('user', flat=True)))
        elif self.mailing_type == 'sub':
            queryset = queryset.filter(profile__send_newsletters=True)
        elif self.mailing_type == 'all':
            pass
        else:
            queryset = []
        return queryset

    def send_mails(self):
        recipients = self.get_recipients()
        sended_mails = send_mass_html_mail(
            [(
                 Template(self.subject).render({'recipient': recipient}),
                 Template(self.message).render({'recipient': recipient}),
                 settings.DEFAULT_FROM_EMAIL,
                 [recipient.email],
             ) for recipient in recipients],
        )
        return sended_mails, len(recipients)
