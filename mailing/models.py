from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mass_mail, send_mail
from django.db import models
from django.template import Context, Template
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string

from django.contrib.auth import get_user_model

from materials.models import Material


MAILING_TYPES = (
    ('adm', 'ADMINS'),
    ('mod', 'MODERATORS'),
    ('aut', 'AUTHORS'),
    ('sub', 'SUBSCRIBERS'),
    ('all', 'ALL'),
)


@python_2_unicode_compatible
class Setting(models.Model):
    host = models.CharField('Host', max_length=255)
    port = models.IntegerField('Port')
    username = models.CharField('Username', max_length=255)
    password = models.CharField('Password', max_length=255)
    use_tls = models.BooleanField('Use TLS', default=False)
    use_ssl = models.BooleanField('Use SSL', default=False)
    timeout = models.IntegerField('Timeout', default=30)
    sender = models.CharField('Sender', max_length=255)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return '{username}@{host}:{port}'.format(username=self.username, host=self.host, port=self.port)

    def get_connection(self, backend=None, fail_silently=False, **kwargs):
        klass = import_string(backend or settings.EMAIL_BACKEND)
        return klass(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=self.use_tls,
                use_ssl=self.use_ssl,
                timeout=self.timeout,
                fail_silently=fail_silently,
                **kwargs
            )


@python_2_unicode_compatible
class Mail(models.Model):
    mailing_type = models.CharField('Mailing type', max_length=3, choices=MAILING_TYPES)
    subject = models.CharField('Subject', max_length=255)
    message = models.TextField('Template')
    setting = models.ForeignKey(Setting)

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
            queryset = queryset.filter(pk__in=set(Material.objects.values_list('user', flat=True)))
        elif self.mailing_type == 'sub':
            queryset = queryset.filter(profile__send_newsletters=True)
        elif self.mailing_type == 'all':
            pass
        else:
            queryset = []
        return queryset

    def send_mails(self):
        recipients = self.get_recipients()
        sended_mails = send_mass_mail(
            [(
                 Template(self.subject).render(Context({'recipient': recipient})),
                 Template(self.message).render(Context({'recipient': recipient})),
                 self.setting.sender,
                 [recipient.email],
             ) for recipient in recipients],
            connection=self.setting.get_connection(),
        )
        return sended_mails, len(recipients)
