from hashlib import md5

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.settings import COUNTRIES


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile',
                                on_delete=models.CASCADE)
    send_newsletters = models.BooleanField('Send newsletters', default=False)
    send_notifications = models.BooleanField(
        'Send notifications', default=False)
    country = models.CharField(
        'Country', max_length=2, choices=COUNTRIES, default='RU')
    show_fullname = models.BooleanField(
        'Show full name on site', default=False)
    show_email = models.BooleanField('Show e-mail on site', default=False)
    about = models.TextField('About', blank=True)
    website = models.CharField('Website', max_length=255, blank=True)
    deviantart = models.CharField('Deviantart', max_length=255, blank=True)
    facebook = models.CharField('Facebook', max_length=255, blank=True)
    twitter = models.CharField('Twitter', max_length=255, blank=True)
    gplus = models.CharField('Google+', max_length=255, blank=True)

    def __str__(self):
        return 'Account for {}'.format(self.user)

    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={
            'slug': self.user.username,
        })

    def get_materials_url(self):
        return reverse('profiles:materials', kwargs={
            'slug': self.user.username,
        })

    def get_activities_url(self):
        return reverse('profiles:activities', kwargs={
            'slug': self.user.username,
        })

    def get_email_hash(self):
        m = md5(self.user.email.strip().lower().encode('utf-8'))
        return m.hexdigest()

    def get_last_materials(self):
        return self.user.materials.published().select_related('category')[:4]

    def get_overall_materials(self):
        return self.user.materials.count()

    def get_overall_downloads(self):
        return self.user.materials.aggregate(models.Sum('downloads'))['downloads__sum']
